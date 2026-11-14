import streamlit as st
from modules.navigation import render_sidebar
from modules.components import load_css, render_footer
from data.data_loader import load_equipment_data, get_summary_stats
from modules.explorer import feature_image

st.set_page_config(page_title="Space Legacy Explorer | NASA Space Apps 2026", page_icon="🛰️", layout="wide", initial_sidebar_state="expanded")
load_css()
render_sidebar()
d = load_equipment_data()
s = get_summary_stats(d)
feature_image(
    "EVERY MISSION LEAVES A LEGACY.",
    "Discover the forgotten explorers, abandoned machines and scientific stories hidden across the Moon and Mars.",
    "https://images-assets.nasa.gov/image/as11-40-5917/as11-40-5917~medium.jpg",
    "https://images.nasa.gov/details/as11-40-5917",
    "Apollo 11 lunar surface · NASA/JSC · AS11-40-5917",
    "nasa_moon_apollo11.jpg",
    "Local Apollo 11 archive photo · NASA/JSC",
    "Apollo 11 lunar surface and Lunar Module"
)
st.markdown("<div class='eyebrow' style='margin-top:1.5rem'>NASA SPACE APPS CHALLENGE 2026 · DIGITAL MUSEUM</div>", unsafe_allow_html=True)
st.caption(f"Source-linked catalog: figures reflect {s['total_records']} records currently in the dataset. Coverage is partial; records have not been independently re-verified in real time.")
st.markdown("### A field archive of human exploration")
st.write("Every surface mission leaves more than hardware behind. Explore the instruments, landers and rovers that helped us understand two neighboring worlds—and the records that preserve their stories.")
st.markdown("### Archive at a glance")
for c, label, value in zip(st.columns(4), ["Catalog records", "Moon records", "Mars records", "Active records"], [s["total_records"], s["moon_count"], s["mars_count"], s["active_count"]]):
    c.metric(label, value)
st.markdown("### Choose a destination")
for c, page, label, detail, planet_class in zip(st.columns(2), ["pages/1_Explore_Moon.py", "pages/2_Explore_Mars.py"], ["Explore the Moon", "Explore Mars"], ["Apollo surface experiments, rovers, landers and lunar instruments.", "Viking landers, Pathfinder and the rover missions of the Red Planet."], ["moon", "mars"]):
    with c:
        icon = "☾" if planet_class == "moon" else "♂"
        st.markdown(f"<div class='destination-card {planet_class}'><div class='destination-icon'>{icon}</div><div class='destination-kicker'>FIELD ARCHIVE · {planet_class.upper()}</div><h3>{label}</h3><p>{detail}</p></div>", unsafe_allow_html=True)
        st.page_link(page, label=f"Open {label}", icon="🌙" if planet_class == "moon" else "🔴", use_container_width=True)
st.markdown("### Mission control")
st.write("Browse the source-linked equipment archive, compare records in the dashboard, follow mission chronology, and explore the science and legacy behind each mission.")
st.page_link("pages/4_Mission_Dashboard.py", label="Open Mission Dashboard", use_container_width=True)
st.page_link("pages/9_Planetary_Experience.py", label="Explore the illustrative planetary globe", use_container_width=True)
st.caption("Dates, statuses, images and coordinates are shown as recorded in the bundled dataset. Consult each record’s official source and verification notes.")
render_footer()
