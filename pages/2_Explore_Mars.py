import streamlit as st
from modules.components import load_css, render_footer
from modules.navigation import render_sidebar
from modules.explorer import render_catalog, feature_image, data

st.set_page_config(page_title="Explore Mars | Space Legacy Explorer", page_icon="🛰️", layout="wide")
load_css()
render_sidebar()
feature_image(
    "THE RED PLANET ARCHIVE",
    "Follow the landers, rovers and scientific instruments that turned Mars into a place we could explore up close.",
    "https://images-assets.nasa.gov/image/PIA20284/PIA20284~medium.jpg",
    "https://images.nasa.gov/details/PIA20284",
    "Curiosity rover at Namib Dune · NASA/JPL-Caltech/MSSS · PIA20284",
    "mars_celestial.svg",
    "Illustrative Mars graphic · NASA image unavailable",
    "NASA Curiosity rover panorama at Namib Dune on Mars"
)
mars_records = data().query("planet == 'Mars'")
missions = mars_records.mission_name.nunique()
st.markdown(f"""
<section class="destination-intro mars-intro">
  <div class="intro-copy"><span class="intro-kicker">MARTIAN FIELD NOTES · ARCHIVE VIEW</span>
  <h2>Robotic explorers<br>on the Red Planet.</h2>
  <p>Follow the landers, rovers and instruments that turned Mars into a world we could study in place. Mission status and history follow the source-linked records in this archive.</p></div>
  <div class="intro-stats"><div><strong>{len(mars_records)}</strong><span>catalog records</span></div><div><strong>{missions}</strong><span>missions represented</span></div><div><strong>Mars</strong><span>destination archive</span></div></div>
</section>
""", unsafe_allow_html=True)
st.markdown("### Explore the Martian archive")
st.write("Browse Viking, Pathfinder and Sojourner through Spirit, Opportunity, Curiosity and Perseverance. Each equipment record includes its purpose, known contribution, status and source references; current mission status may require a fresh source check.")
render_catalog("Martian equipment archive", "Mars")
render_footer()
