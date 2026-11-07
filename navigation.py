"""Mission Control sidebar."""
import streamlit as st
from urllib.parse import urlparse
import re
PAGES=[("Home","app.py"),("Explore Moon","pages/1_Explore_Moon.py"),("Explore Mars","pages/2_Explore_Mars.py"),("Equipment Explorer","pages/3_Equipment_Explorer.py"),("Mission Dashboard","pages/4_Mission_Dashboard.py"),("Mission Timeline","pages/5_Mission_Timeline.py"),("Science & Discovery","pages/6_Science_Discovery.py"),("The Legacy Room","pages/7_Legacy_Room.py"),("Quiz","pages/8_Quiz.py")]
def render_sidebar():
 current=urlparse(st.context.url).path.rstrip("/").rsplit("/",1)[-1]
 normalize=lambda value:re.sub(r"[^a-z0-9]","",value.casefold())
 current=normalize(current or "Home")
 with st.sidebar:
  st.markdown('<div class="sidebar-brand"><span>NASA · SPACE APPS 2026</span><strong>MISSION CONTROL</strong><small>SPACE LEGACY EXPLORER</small></div>',unsafe_allow_html=True)
  for name,path in PAGES:
   if normalize(name.removeprefix("The "))==current:
    with st.container(key="active_sidebar_link"):
     st.page_link(path,label=name,use_container_width=True)
   else:st.page_link(path,label=name,use_container_width=True)
  st.divider();st.caption("Source-linked archive · check references and record notes.")
