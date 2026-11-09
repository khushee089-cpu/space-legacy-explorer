import streamlit as st
from modules.components import load_css,render_footer
from modules.navigation import render_sidebar
from modules.explorer import render_quiz
st.set_page_config(page_title="Quiz | Space Legacy Explorer",page_icon="🛰️",layout="wide")
load_css();render_sidebar();render_quiz();render_footer()
