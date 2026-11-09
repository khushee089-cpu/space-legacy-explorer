import streamlit as st
from modules.components import load_css,render_footer
from modules.navigation import render_sidebar
from modules.explorer import render_planetary_experience
st.set_page_config(page_title="Planetary Experience | Space Legacy Explorer",page_icon="🛰️",layout="wide")
load_css();render_sidebar();render_planetary_experience();render_footer()
