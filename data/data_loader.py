"""
data_loader.py
==============
Loads, validates and summarises the NASA equipment dataset for Space Legacy Explorer.

Usage
-----
    from data.data_loader import load_equipment_data, validate_data, get_summary_stats

    df  = load_equipment_data()
    rpt = validate_data(df)
    stats = get_summary_stats(df)
"""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CSV_PATH = Path(__file__).parent / "nasa_equipment_dataset.csv"

REQUIRED_COLUMNS = [
    "equipment_id",
    "equipment_name",
    "planet",
    "mission_name",
    "agency",
    "mission_type",
    "launch_date",
    "landing_date",
    "mission_end_date",
    "equipment_category",
    "mission_objective",
    "scientific_contribution",
    "current_status",
    "location_name",
    "location_coordinates",
    "image_url",
    "official_source",
    "verification_notes",
]

ALLOWED_PLANETS = {"Moon", "Mars"}

ALLOWED_STATUSES_PARTIAL = [
    "Active",
    "Inactive",
    "Unknown",
]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def load_equipment_data(csv_path: Path | str | None = None) -> pd.DataFrame:
    """Load the NASA equipment dataset from CSV.

    Parameters
    ----------
    csv_path:
        Optional override path to the CSV file. Defaults to the bundled dataset.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with stripped string columns.

    Raises
    ------
    FileNotFoundError
        If the CSV file does not exist at the resolved path.
    ValueError
        If required columns are missing from the file.
    """
    path = Path(csv_path) if csv_path else CSV_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Run the data collection step or provide a valid path."
        )

    df = pd.read_csv(path, dtype=str)

    # Strip whitespace from all string cells
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Dataset is missing required columns: {missing_cols}. "
            "Check the CSV file or update REQUIRED_COLUMNS in data_loader.py."
        )

    logger.info("Loaded %d records from %s", len(df), path)
    return df


def validate_data(df: pd.DataFrame) -> dict:
    """Run data-quality checks and return a structured report.

    Checks performed
    ----------------
    1. Duplicate ``equipment_id`` values.
    2. Missing values per required column.
    3. ``planet`` values outside the allowed set.
    4. ``current_status`` values that do not start with an allowed keyword.
    5. Rows with no ``official_source`` URL.

    Parameters
    ----------
    df:
        DataFrame returned by :func:`load_equipment_data`.

    Returns
    -------
    dict with keys:
        - ``total_records`` (int)
        - ``duplicate_ids`` (list[str])
        - ``missing_values`` (dict[str, int])  — column → count of NaN/empty
        - ``invalid_planets`` (list[str])
        - ``invalid_statuses`` (list[str])
        - ``missing_sources`` (int)
        - ``passed`` (bool)  — True only when no issues found
    """
    report: dict = {
        "total_records": len(df),
        "duplicate_ids": [],
        "missing_values": {},
        "invalid_planets": [],
        "invalid_statuses": [],
        "missing_sources": 0,
        "invalid_sources": [],
        "invalid_dates": [],
        "invalid_date_order": [],
        "passed": True,
    }

    # 1. Duplicate equipment_id
    dup_mask = df.duplicated(subset=["equipment_id"], keep=False)
    if dup_mask.any():
        report["duplicate_ids"] = df.loc[dup_mask, "equipment_id"].tolist()
        report["passed"] = False

    # 2. Missing values in required columns
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            report["missing_values"][col] = -1  # column entirely absent
            report["passed"] = False
            continue

        empty_count = int(df[col].isna().sum() + (df[col] == "").sum())
        if empty_count > 0:
            report["missing_values"][col] = empty_count
            # Don't fail on optional blanks but surface the info

    # 3. Invalid planet values
    bad_planets = df.loc[~df["planet"].isin(ALLOWED_PLANETS), "equipment_id"].tolist()
    if bad_planets:
        report["invalid_planets"] = bad_planets
        report["passed"] = False

    # 4. Invalid current_status (must start with one of the allowed keywords)
    def _status_valid(val: str) -> bool:
        val = str(val).strip()
        return any(val.startswith(kw) for kw in ALLOWED_STATUSES_PARTIAL)

    bad_status = df.loc[~df["current_status"].apply(_status_valid), "equipment_id"].tolist()
    if bad_status:
        report["invalid_statuses"] = bad_status
        report["passed"] = False

    # 5. Missing official_source
    missing_src = int(
        df["official_source"].isna().sum() + (df["official_source"] == "").sum()
    )
    report["missing_sources"] = missing_src
    if missing_src > 0:
        report["passed"] = False

    # URLs and mission chronology are structural checks; blank/unknown dates remain allowed.
    from urllib.parse import urlparse
    for _, row in df.iterrows():
        equipment_id = str(row.get("equipment_id", "Unknown"))
        source = str(row.get("official_source", "")).strip()
        parsed = urlparse(source)
        if source and (parsed.scheme not in {"http", "https"} or not parsed.netloc):
            report["invalid_sources"].append(equipment_id)
        parsed_dates = {}
        for field in ("launch_date", "landing_date", "mission_end_date"):
            value = str(row.get(field, "")).strip()
            if not value or value.casefold() in {"unknown", "not verified", "still active"}:
                continue
            stamp = pd.to_datetime(value, errors="coerce")
            if pd.isna(stamp):
                report["invalid_dates"].append({"equipment_id": equipment_id, "field": field, "value": value})
            else:
                parsed_dates[field] = stamp
        launch, landing, end = parsed_dates.get("launch_date"), parsed_dates.get("landing_date"), parsed_dates.get("mission_end_date")
        if launch is not None and landing is not None and landing < launch:
            report["invalid_date_order"].append(equipment_id)
        if landing is not None and end is not None and end < landing:
            report["invalid_date_order"].append(equipment_id)
    if report["invalid_sources"] or report["invalid_dates"] or report["invalid_date_order"]:
        report["passed"] = False

    return report


def get_summary_stats(df: pd.DataFrame) -> dict:
    """Return aggregate statistics for the dataset.

    Parameters
    ----------
    df:
        DataFrame returned by :func:`load_equipment_data`.

    Returns
    -------
    dict with keys:
        - ``total_records`` (int)
        - ``by_planet`` (dict[str, int])
        - ``by_status_group`` (dict[str, int])  — Active / Inactive / Unknown
        - ``by_category`` (dict[str, int])
        - ``by_agency`` (dict[str, int])
        - ``moon_count`` (int)
        - ``mars_count`` (int)
        - ``active_count`` (int)
        - ``inactive_count`` (int)
        - ``unknown_count`` (int)
    """

    def _group_status(val: str) -> str:
        val = str(val).strip()
        if val.startswith("Active"):
            return "Active"
        if val.startswith("Inactive"):
            return "Inactive"
        return "Unknown"

    df = df.copy()
    df["_status_group"] = df["current_status"].apply(_group_status)

    by_planet = df["planet"].value_counts().to_dict()
    by_status = df["_status_group"].value_counts().to_dict()
    by_category = df["equipment_category"].value_counts().to_dict()
    by_agency = df["agency"].value_counts().to_dict()

    return {
        "total_records": len(df),
        "by_planet": by_planet,
        "by_status_group": by_status,
        "by_category": by_category,
        "by_agency": by_agency,
        "moon_count": by_planet.get("Moon", 0),
        "mars_count": by_planet.get("Mars", 0),
        "active_count": by_status.get("Active", 0),
        "inactive_count": by_status.get("Inactive", 0),
        "unknown_count": by_status.get("Unknown", 0),
    }


def filter_by_planet(df: pd.DataFrame, planet: str) -> pd.DataFrame:
    """Return rows for a specific planet (case-sensitive: 'Moon' or 'Mars')."""
    return df[df["planet"] == planet].reset_index(drop=True)


def filter_by_status(df: pd.DataFrame, status_keyword: str) -> pd.DataFrame:
    """Return rows where current_status starts with *status_keyword*.

    Examples
    --------
    >>> active = filter_by_status(df, "Active")
    >>> inactive = filter_by_status(df, "Inactive")
    """
    mask = df["current_status"].str.startswith(status_keyword, na=False)
    return df[mask].reset_index(drop=True)


def search_equipment(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """Case-insensitive substring search across name, mission and contribution columns."""
    q = query.lower()
    mask = (
        df["equipment_name"].str.lower().str.contains(q, na=False)
        | df["mission_name"].str.lower().str.contains(q, na=False)
        | df["scientific_contribution"].str.lower().str.contains(q, na=False)
        | df["equipment_category"].str.lower().str.contains(q, na=False)
    )
    return df[mask].reset_index(drop=True)


# ---------------------------------------------------------------------------
# CLI helper — run directly to validate the dataset
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    # Force UTF-8 output on Windows terminals
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")

    print("\n" + "=" * 60)
    print("  SPACE LEGACY EXPLORER - Dataset Validator")
    print("=" * 60)

    try:
        df = load_equipment_data()
    except (FileNotFoundError, ValueError) as exc:
        print(f"\n[ERROR] LOAD ERROR: {exc}")
        raise SystemExit(1)

    print(f"\n[OK]  Loaded {len(df)} records from {CSV_PATH.name}\n")

    # Validation report
    report = validate_data(df)
    print("--- Validation Report ---")
    print(f"  Total records     : {report['total_records']}")
    print(f"  Duplicate IDs     : {report['duplicate_ids'] or 'None'}")
    print(f"  Missing sources   : {report['missing_sources']}")
    print(f"  Invalid planets   : {report['invalid_planets'] or 'None'}")
    print(f"  Invalid statuses  : {report['invalid_statuses'] or 'None'}")

    if report["missing_values"]:
        print("  Columns with blanks:")
        for col, cnt in report["missing_values"].items():
            print(f"    {col}: {cnt} blank(s)")
    else:
        print("  Missing values    : None")

    status_label = "PASSED" if report["passed"] else "has WARNINGS - review above"
    print(f"\n[{'OK' if report['passed'] else 'WARN'}]  Validation {status_label}")

    # Summary statistics
    stats = get_summary_stats(df)
    print("\n--- Summary Statistics ---")
    print(f"  Total items       : {stats['total_records']}")
    print(f"  Moon equipment    : {stats['moon_count']}")
    print(f"  Mars equipment    : {stats['mars_count']}")
    print(f"  Active items      : {stats['active_count']}")
    print(f"  Inactive items    : {stats['inactive_count']}")
    print(f"  Unknown status    : {stats['unknown_count']}")
    print("\n  By category:")
    for cat, cnt in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        print(f"    {cat:<40} {cnt}")
    print("\n  By agency:")
    for agency, cnt in sorted(stats["by_agency"].items(), key=lambda x: -x[1]):
        print(f"    {agency:<10} {cnt}")
    print("=" * 60 + "\n")
