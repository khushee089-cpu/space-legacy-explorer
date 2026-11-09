"""
UI Components Module for Space Legacy Explorer.
NASA Scientific Dashboard Design System.
Handles modular rendering of the hero section, navigation cards with genuine NASA photographs,
mission purpose statement, authentic spotlight telemetry, and scientific footer.
"""

import base64
from pathlib import Path
import textwrap
import streamlit as st
from data.missions_data import (
    PROJECT_METADATA,
    FEATURED_DESTINATIONS,
    AUTHENTIC_MISSION_FACTS,
    WHY_EQUIPMENT_REMAINS,
    VERIFIED_METRICS,
)

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_FILE = BASE_DIR / "assets" / "css" / "style.css"
IMAGES_DIR = BASE_DIR / "assets" / "images"


def load_css() -> None:
    """Read and inject the separate CSS styling into the Streamlit application via st.html."""
    if CSS_FILE.exists():
        with open(CSS_FILE, "r", encoding="utf-8") as f:
            css_code = f.read()
        st.html(f"<style>{css_code}</style>")
    else:
        st.warning("Custom CSS file not found at assets/css/style.css")


def get_image_base64(filename: str) -> str:
    """Read an image file from assets/images and return as base64 data URI."""
    image_path = IMAGES_DIR / filename
    if image_path.exists():
        data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
        ext = image_path.suffix.lower().replace(".", "")
        mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
        return f"data:image/{mime};base64,{data}"
    return ""


def get_svg_content(filename: str) -> str:
    """Read an SVG image file from assets/images and return raw SVG string."""
    svg_path = IMAGES_DIR / filename
    if svg_path.exists():
        with open(svg_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


# Clean, minimal SVG icons (NASA scientific style, no emojis)
ICONS = {
    "satellite": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M13 7 9 3 5 7l4 4"/><path d="m17 11 4 4-4 4-4-4"/>'
        '<path d="m8 12 4 4"/><path d="m16 8-4-4"/><path d="M9 21a6 6 0 0 0-6-6"/>'
        '</svg>'
    ),
    "moon": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'
        '</svg>'
    ),
    "mars": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="8"/><path d="M18 6l4-4m0 0h-4m4 0v4"/>'
        '</svg>'
    ),
    "hardware": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="m9 9 6 6m0-6-6 6"/>'
        '</svg>'
    ),
    "compass": (
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
        '</svg>'
    )
}


def render_hero() -> None:
    """
    Renders the clean NASA scientific dashboard hero header:
    - Main heading: 'EVERY MISSION LEAVES A LEGACY.'
    - Subtitle: 'Discover the forgotten explorers, abandoned machines and scientific stories hidden across the Moon and Mars.'
    - Verified scientific metrics strip (No unverified distances).
    """
    metrics_html = "".join([
        f"""
        <div class="metric-card">
          <div class="metric-val">{m['value']}</div>
          <div class="metric-lbl">{m['label']}</div>
          <div class="metric-detail">{m['detail']}</div>
        </div>
        """
        for m in VERIFIED_METRICS
    ])

    hero_html = textwrap.dedent(f"""
    <div class="nasa-hero-panel">
      <div class="nasa-meta-row">
        <div class="nasa-program-badge">
          <span class="nasa-badge-dot"></span>
          <span>{PROJECT_METADATA['agency']}</span>
        </div>
        <div class="nasa-challenge-tag">
          {PROJECT_METADATA['challenge_topic']}
        </div>
      </div>
      
      <h1 class="hero-main-title">{PROJECT_METADATA['tagline']}</h1>
      
      <p class="hero-main-subtitle">
        {PROJECT_METADATA['subtitle']}
      </p>
      
      <div class="metrics-strip">
        {metrics_html}
      </div>
    </div>
    """)
    st.html(hero_html)


def render_navigation_cards() -> None:
    """
    Renders three balanced, professional cards with genuine NASA photographs,
    clear attribution, verified facts, and direct navigation buttons.
    """
    st.html(textwrap.dedent("""
    <div class="section-headline">
      <div class="section-title-text">Expedition Sectors & Artifact Archives</div>
    </div>
    """))

    cols = st.columns(3, gap="large")

    badge_class_map = {
        "moon": "",
        "mars": "mars-badge",
        "equipment": "equip-badge",
    }

    subloc_class_map = {
        "moon": "",
        "mars": "mars-color",
        "equipment": "equip-color",
    }

    note_class_map = {
        "moon": "",
        "mars": "mars-note",
        "equipment": "equip-note",
    }

    card_class_map = {
        "moon": "",
        "mars": "mars",
        "equipment": "",
    }

    for idx, dest in enumerate(FEATURED_DESTINATIONS):
        with cols[idx]:
            img_b64 = get_image_base64(dest["photo_file"])
            relics_html = "".join([f"<li>{r}</li>" for r in dest["key_relics"]])

            card_html = textwrap.dedent(f"""
            <div class="scientific-card {card_class_map.get(dest['id'], '')}">
              <div>
                <div class="card-header-line">
                  <span class="card-badge {badge_class_map.get(dest['id'], '')}">{dest['badge']}</span>
                  <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-muted);">REF-{idx+1:02d}</span>
                </div>
                
                <div class="photo-frame">
                  <img src="{img_b64}" alt="{dest['photo_title']}" />
                  <div class="photo-attribution-overlay">
                    <strong>{dest['photo_title']}</strong><br />
                    <span>{dest['photo_credit']}</span>
                  </div>
                </div>
                
                <h3 class="card-h3">{dest['title']}</h3>
                <div class="card-subloc {subloc_class_map.get(dest['id'], '')}">{dest['destination']}</div>
                <div class="card-summary-p">{dest['summary']}</div>
                
                <ul class="relic-list-items">
                  {relics_html}
                </ul>
              </div>
              
              <div>
                <div class="card-footer-note {note_class_map.get(dest['id'], '')}">
                  <strong>Engineering Reason:</strong> {dest['why_left']}
                </div>
              </div>
            </div>
            """)
            st.html(card_html)

            btn_key = f"btn_explore_{dest['id']}"
            if st.button(f"OPEN {dest['title'].upper()}", key=btn_key):
                try:
                    st.switch_page(dest["route"])
                except Exception:
                    st.info(f"Target sector: {dest['title']}")


def render_purpose_section() -> None:
    """
    Renders the scientific context panel explaining why equipment remains
    and the core pillars of planetary exploration preservation.
    """
    pillars_html = "".join([
        f"""
        <div class="pillar-box">
          <div class="pillar-box-title">{p['pillar']}</div>
          <p class="pillar-box-desc">{p['description']}</p>
        </div>
        """
        for p in WHY_EQUIPMENT_REMAINS
    ])

    purpose_html = textwrap.dedent(f"""
    <div class="purpose-panel">
      <div class="purpose-kicker">SCIENTIFIC & HISTORICAL CONTEXT</div>
      <h2 class="purpose-title-h2">Abandoned But Never Forgotten</h2>
      
      <p class="purpose-lead-text">
        {PROJECT_METADATA['purpose_statement']}
      </p>
      
      <div class="pillars-container">
        {pillars_html}
      </div>
    </div>
    """)
    st.html(purpose_html)


def render_historical_spotlight() -> None:
    """
    Renders verified authentic facts about real NASA equipment left on celestial bodies.
    No fictional or placeholder data.
    """
    st.html(textwrap.dedent("""
    <div class="section-headline" style="margin-top: 3.5rem;">
      <div class="section-title-text">Verified Mission Artifacts • Archival Records</div>
    </div>
    """))

    cols = st.columns(2, gap="medium")

    for idx, item in enumerate(AUTHENTIC_MISSION_FACTS):
        col_idx = idx % 2
        with cols[col_idx]:
            spotlight_html = textwrap.dedent(f"""
            <div class="spotlight-card-dashboard">
              <div class="spotlight-tag-line">{item['category']} • {item['location']}</div>
              <div class="spotlight-heading">{item['mission']}</div>
              <p class="spotlight-body">{item['fact']}</p>
            </div>
            """)
            st.html(spotlight_html)


def render_footer() -> None:
    """Renders the scientific dashboard footer with NASA public domain citation."""
    footer_html = textwrap.dedent(f"""
    <div class="nasa-footer-strip">
      <div class="footer-main-label">{PROJECT_METADATA['title']} • {PROJECT_METADATA['agency']}</div>
      <p class="footer-attribution-p">
        Challenge: "{PROJECT_METADATA['challenge_topic']}".<br />
        All imagery and mission records courtesy of NASA, Jet Propulsion Laboratory (JPL-Caltech), and the Johnson Space Center.
      </p>
      <div class="footer-source-badge">
        NASA PUBLIC DOMAIN SCIENCE ARCHIVE • OPEN DATA INITIATIVE
      </div>
    </div>
    """)
    st.html(footer_html)
