import streamlit as st
from modules.components import load_css, render_footer
from modules.navigation import render_sidebar
from modules.explorer import render_catalog, feature_image, data

st.set_page_config(page_title="Explore Moon | Space Legacy Explorer", page_icon="🛰️", layout="wide")
load_css()
render_sidebar()
feature_image(
    "THE LUNAR ARCHIVE",
    "Experiments, machines and human exploration across the Apollo and robotic missions to the Moon.",
    "https://images-assets.nasa.gov/image/as11-40-5931/as11-40-5931~medium.jpg",
    "https://images.nasa.gov/details/as11-40-5931",
    "Apollo 11 astronaut deploys EASEP · NASA/JSC · AS11-40-5931",
    "nasa_moon_apollo11.jpg",
    "Local Apollo 11 archive photo · NASA/JSC",
    "Apollo 11 astronaut deploying lunar surface experiments"
)
moon_records = data().query("planet == 'Moon'")
missions = moon_records.mission_name.nunique()
st.markdown(f"""
<section class="destination-intro moon-intro">
  <div class="intro-copy"><span class="intro-kicker">LUNAR FIELD NOTES · ARCHIVE VIEW</span>
  <h2>Footprints, instruments<br>and machines that stayed.</h2>
  <p>Explore the hardware that carried human and robotic science across the lunar surface. Each record separates confirmed mission history from details still awaiting verification.</p></div>
  <div class="intro-stats"><div><strong>{len(moon_records)}</strong><span>catalog records</span></div><div><strong>{missions}</strong><span>missions represented</span></div><div><strong>Moon</strong><span>destination archive</span></div></div>
</section>
""", unsafe_allow_html=True)
st.markdown("### Explore the lunar archive")
st.write("Search Apollo surface experiments, ALSEP instruments, lunar rovers, Surveyor spacecraft and other equipment. Surface hardware is distinguished from spacecraft, with source links and verification notes included in each record.")
render_catalog("Lunar equipment archive", "Moon")
render_footer()
