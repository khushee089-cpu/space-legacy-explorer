"""Shared dataset-backed Streamlit pages."""
import re
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from data.data_loader import load_equipment_data,get_summary_stats,validate_data
from modules.components import IMAGES_DIR
@st.cache_data(show_spinner=False)
def data():return load_equipment_data()
def header(k,t,d):
 st.markdown(f'<div class="eyebrow">{k}</div>',unsafe_allow_html=True);st.title(t);st.write(d)
@st.cache_data(ttl=3600,show_spinner=False)
def fetch(url):
 try:
  import requests
  r=requests.get(url,timeout=4);r.raise_for_status()
  return r.content if r.headers.get("content-type","").startswith("image/") and len(r.content)<12000000 else None
 except Exception:return None
def photo(x):
 b=fetch(str(x.get("image_url","")))
 if b:st.image(b,caption=f"Image source listed on record · {x.equipment_name}")
 else:
  if x.planet=="Moon":st.image(str(IMAGES_DIR/"nasa_moon_apollo11.jpg"),caption="NASA lunar archive photo fallback · see record source.")
  else:st.image(str(IMAGES_DIR/"mars_celestial.svg"),caption="Illustrative Mars graphic fallback · NASA photo unavailable offline.")
def detail(x):
 st.markdown(f"#### {x.equipment_name}");st.caption(f"{x.mission_name} · {x.agency} · {x.planet} · {x.current_status}")
 a,b=st.columns([1,1.6])
 with a:photo(x)
 with b:
  st.markdown(f"**Purpose**  \n{x.mission_objective}")
  st.markdown(f"**Description**  \n{x.get('equipment_description') or x.mission_type}")
  st.markdown(f"**What happened / contribution**  \n{x.scientific_contribution}")
  st.markdown(f"**Status**  \n{x.current_status}")
  st.markdown(f"**Location**  \n{x.location_name} · {x.location_coordinates}")
  st.markdown(f"**Dates**  \nLaunch: {x.launch_date} · Landing: {x.landing_date} · End: {x.mission_end_date}")
  st.markdown(f"**Why it remained**  \n{x.get('why_left') or 'No separately verified explanation in this record.'}")
  st.markdown(f"**Verification note**  \n{x.verification_notes}")
  if str(x.official_source).startswith("http"):st.markdown(f"[Open listed official source]({x.official_source})")
def feature_image(title, subtitle, image_url, source_url, image_credit, fallback_file=None, fallback_credit="Illustrative fallback", alt=""):
    """Responsive source-credited image banner with an embedded offline fallback."""
    import base64, html
    fallback_src = ""
    if fallback_file:
        fallback_path = IMAGES_DIR / fallback_file
        if fallback_path.exists():
            mime = "image/svg+xml" if fallback_path.suffix.lower() == ".svg" else "image/jpeg"
            encoded = base64.b64encode(fallback_path.read_bytes()).decode("ascii")
            fallback_src = f"data:{mime};base64,{encoded}"
    safe_title = html.escape(str(title))
    safe_subtitle = html.escape(str(subtitle))
    safe_alt = html.escape(str(alt or title), quote=True)
    safe_credit = html.escape(str(image_credit))
    safe_fallback_credit = html.escape(str(fallback_credit))
    safe_source = html.escape(str(source_url), quote=True)
    safe_image = html.escape(str(image_url), quote=True)
    fallback_attr = html.escape(fallback_src, quote=True)
    markup = f"""
    <style>
      html,body{{margin:0;background:transparent;font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
      .feature{{height:clamp(350px,53vw,540px);max-height:540px;min-height:350px;position:relative;overflow:hidden;border:1px solid #d8e1eb;border-radius:18px;background:#e9edf2;background-image:linear-gradient(90deg,rgba(17,28,43,.50),rgba(17,28,43,.08)),url('{fallback_src}');background-size:cover;background-position:center}}
      .feature img{{width:100%;height:100%;object-fit:cover;display:block;object-position:center 48%}}
      .shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(17,28,43,.78) 0%,rgba(17,28,43,.38) 46%,rgba(17,28,43,.05) 100%),linear-gradient(0deg,rgba(17,28,43,.46),transparent 34%)}}
      .copy{{position:absolute;left:clamp(22px,5vw,64px);top:50%;transform:translateY(-50%);max-width:650px;color:#f1f5f9}}
      .kicker{{font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#d9e4ed!important;margin-bottom:16px}}
      .feature-title{{display:block;font-size:clamp(32px,5vw,58px);line-height:1.04;letter-spacing:-.04em;margin:0 0 14px;color:#F1F5F9!important;font-weight:700;text-shadow:0 2px 12px rgba(0,0,0,.45)}}
      .feature .sub{{font-size:clamp(15px,1.6vw,19px);line-height:1.55;color:#e2e8f0!important;margin:0;max-width:570px}}
      .credit{{position:absolute;right:16px;bottom:14px;padding:8px 11px;border-radius:8px;background:rgba(16,29,50,.72);color:#e2e8f0!important;font-size:11px;line-height:1.45;max-width:65%}}
      .credit a{{color:#b7e8ed!important;text-decoration:none}}.credit a:hover{{text-decoration:underline}}
      @media(max-width:600px){{.feature{{height:410px;min-height:410px}}.copy{{top:auto;bottom:55px;transform:none;right:20px}}.credit{{left:12px;right:12px;bottom:10px;max-width:none;font-size:10px}}}}
    </style>
    <section class="feature" aria-label="{safe_title}">
      <img src="{safe_image}" alt="{safe_alt}" loading="eager" onerror="this.style.display='none'">
      <div class="shade"><div class="copy"><div class="kicker">Space Legacy Explorer · Field archive</div><div class="feature-title" role="heading" aria-level="2" style="color:#F1F5F9 !important">{safe_title}</div><p class="sub" style="color:#E2E8F0 !important;text-shadow:0 1px 8px rgba(0,0,0,.35)">{safe_subtitle}</p></div><div class="credit"><span>{safe_credit}</span> · <a href="{safe_source}" target="_blank" rel="noopener">NASA source ↗</a></div></div>
    </section>
    """
    st.html(markup)

def render_catalog(title="Equipment Explorer",planet=None):
 d=data();header("EQUIPMENT ARCHIVE",title,"Search by equipment, mission, destination, category or status. Expand a record for purpose, history, contribution, location and references.")
 if planet:d=d[d.planet.eq(planet)]
 a,b,c=st.columns([2,1,1]);q=a.text_input("Search equipment",placeholder="ALSEP, rover, Surveyor…")
 ps=["All"]+sorted(d.planet.dropna().unique());p=b.selectbox("Planet",ps,index=ps.index(planet) if planet in ps else 0)
 if p!="All":d=d[d.planet.eq(p)]
 cs=["All"]+sorted(d.equipment_category.dropna().unique());cat=c.selectbox("Category",cs)
 if cat!="All":d=d[d.equipment_category.eq(cat)]
 a,b=st.columns(2);ms=["All"]+sorted(d.mission_name.dropna().unique());m=a.selectbox("Mission",ms);ss=["All"]+sorted(d.current_status.dropna().unique());s=b.selectbox("Status",ss)
 if m!="All":d=d[d.mission_name.eq(m)]
 if s!="All":d=d[d.current_status.eq(s)]
 q=q.strip().casefold()
 if q:
  mask=pd.Series(False,index=d.index)
  for col in ["equipment_name","mission_name","scientific_contribution","equipment_category","mission_objective"]:mask|=d[col].fillna("").astype(str).str.casefold().str.contains(re.escape(q),regex=True)
  d=d[mask]
 st.caption(f"{len(d)} matches · only bundled records."); 
 for _,x in d.iterrows():
  with st.expander(f"{x.equipment_name} · {x.mission_name} · {x.current_status}"):detail(x)
def pxmod():
 try:
  import plotly.express as px;return px
 except ImportError:return None
def theme(f):
 f.update_layout(template="plotly_white",paper_bgcolor="#F7F9FC",plot_bgcolor="#FFFFFF",font_color="#334155",colorway=["#16899A","#C66B3A","#7C93AA"]);return f
def render_dashboard():
 d_all=data();header("MISSION CONTROL","Mission Dashboard","A source-linked archive desk for Moon and Mars missions. This view summarizes catalog records; it does not show live spacecraft telemetry.")
 st.markdown("<div class='dashboard-note'><strong>ARCHIVE MODE</strong> · Figures below are calculated from the bundled equipment dataset. Mission dates and statuses follow each record’s source notes.</div>",unsafe_allow_html=True)
 f1,f2=st.columns([1,1])
 planet=f1.selectbox("Destination",["All","Moon","Mars"],key="dash_planet")
 cats=["All"]+sorted(d_all.equipment_category.dropna().unique().tolist())
 category=f2.selectbox("Equipment category",cats,key="dash_category")
 d=d_all.copy()
 if planet!="All":d=d[d.planet.eq(planet)]
 if category!="All":d=d[d.equipment_category.eq(category)]
 if d.empty:
  st.info("No equipment records match these filters.");return
 stats=get_summary_stats(d)
 moon_count=int(d.planet.eq("Moon").sum());mars_count=int(d.planet.eq("Mars").sum())
 active_count=int(d.current_status.fillna("").str.casefold().str.startswith("active").sum())
 inactive_count=int(d.current_status.fillna("").str.casefold().str.startswith("inactive").sum())
 mission_count=int(d.mission_name.nunique())
 st.markdown("#### Archive snapshot")
 for c,label,value in zip(st.columns(5),["Equipment records","Missions represented","Moon records","Mars records","Active status*"],[len(d),mission_count,moon_count,mars_count,active_count]):c.metric(label,value)
 st.caption(f"*Status labels describe {active_count} active and {inactive_count} inactive equipment records in the current filter. Dataset coverage is partial; unknown records are not counted as active or inactive.")

 st.markdown("#### Mission operations desk")
 all_missions=sorted(d.mission_name.dropna().unique().tolist())
 default_index=all_missions.index("Apollo 11") if "Apollo 11" in all_missions else 0
 spotlight=st.selectbox("Mission spotlight",all_missions,index=default_index,key="dash_spotlight") if all_missions else None
 left,center,right=st.columns([1.12,1,1])
 if spotlight:
  g=d[d.mission_name.eq(spotlight)];mission=g.iloc[0]
  with left,st.container(border=True):
   st.markdown("**MISSION BRIEF**")
   st.markdown(f"### {spotlight}")
   st.caption(f"{mission.agency} · {mission.planet} · {len(g)} catalog record(s)")
   st.markdown(f"**Launch:** {mission.launch_date}  ·  **Landing:** {mission.landing_date}")
   st.markdown(f"**Objective:** {mission.mission_objective}")
   photo(g.iloc[0])
   if str(mission.official_source).startswith("http"):st.markdown(f"[Open official mission source]({mission.official_source})")
 else:
  with left,st.container(border=True):st.info("No mission record available for this filter.")
 px=pxmod()
 status=d.current_status.fillna("Unknown").replace("","Unknown").value_counts().rename_axis("Status").reset_index(name="Records")
 category_counts=d.groupby(["equipment_category","planet"],dropna=False).size().reset_index(name="Records").rename(columns={"equipment_category":"Category","planet":"Planet"})
 with center,st.container(border=True):
  st.markdown("**EQUIPMENT STATUS**")
  if not status.empty:
   px=pxmod()
   if px:
    fig=px.pie(status,names="Status",values="Records",hole=.58,color_discrete_sequence=["#16899A","#C66B3A","#7C93AA","#ABC7CF"])
    fig.update_layout(showlegend=True,legend_title_text="",margin=dict(t=12,b=10,l=8,r=8),height=290)
    st.plotly_chart(theme(fig),use_container_width=True)
   else:st.bar_chart(status.set_index("Status"),color="#16899A",height=290)
   st.caption("Equipment status as recorded; records may need current source checks.")
 with right,st.container(border=True):
  st.markdown("**MISSION RECORD**")
  if spotlight:
   st.metric("Equipment in spotlight",len(g))
   status_counts=g.current_status.fillna("Unknown").replace("","Unknown").value_counts()
   st.markdown("**Recorded equipment status**")
   for label,count in status_counts.items():st.markdown(f"{label} · **{count}**")
   st.markdown("**Related equipment**")
   for name in g.equipment_name.tolist()[:6]:st.markdown(f"• {name}")
   if len(g)>6:st.caption(f"And {len(g)-6} more records in this mission.")
  else:st.caption("Choose a mission to view its equipment records.")

 st.markdown("#### Mission coverage and chronology")
 chart_left,chart_right=st.columns(2)
 with chart_left:
  st.markdown("**Equipment records by mission**")
  mission_counts=d.groupby(["mission_name","planet"]).size().rename("Records").reset_index()
  if px:
   fig=px.bar(mission_counts,x="Records",y="mission_name",color="planet",orientation="h",color_discrete_map={"Moon":"#8C9AA8","Mars":"#C66B3A"})
   fig.update_layout(yaxis_title="",xaxis_title="Catalog records",height=max(300,min(650,30*len(mission_counts)+100)),margin=dict(t=18,b=15,l=8,r=10))
   st.plotly_chart(theme(fig),use_container_width=True)
  else:st.bar_chart(mission_counts.set_index("mission_name")["Records"],color="#16899A",height=390)
 with chart_right:
  st.markdown("**Launch decade distribution**")
  years=pd.to_datetime(d.launch_date,errors="coerce").dt.year.dropna()
  if len(years):
   decades=((years//10)*10).astype(int).astype(str)+"s";decade_counts=decades.value_counts().sort_index().rename_axis("Decade").reset_index(name="Records")
   if px:
    fig=px.bar(decade_counts,x="Decade",y="Records",color="Records",color_continuous_scale=["#D9EAEC","#16899A"])
    fig.update_layout(coloraxis_showscale=False,height=340,margin=dict(t=18,b=15,l=8,r=10))
    st.plotly_chart(theme(fig),use_container_width=True)
   else:st.bar_chart(decade_counts.set_index("Decade"),color="#16899A",height=340)
  else:st.info("No launch dates are available for this filter.")
  st.markdown("**Equipment category mix**")
  if px:
   fig=px.bar(category_counts,x="Category",y="Records",color="Planet",barmode="group",color_discrete_map={"Moon":"#8C9AA8","Mars":"#C66B3A"})
   fig.update_layout(height=330,margin=dict(t=18,b=15,l=8,r=8),xaxis_title="")
   st.plotly_chart(theme(fig),use_container_width=True)
  else:
   category_pivot=category_counts.pivot_table(index="Category",columns="Planet",values="Records",aggfunc="sum",fill_value=0)
   planet_colors={"Mars":"#16899A","Moon":"#C66B3A"}
   st.bar_chart(category_pivot,color=[planet_colors.get(str(name),"#7C93AA") for name in category_pivot.columns],height=330)

 st.markdown("#### Archive dispatches")
 st.caption("Selected source-linked equipment records · historical archive, not a live news feed.")
 latest=d.sort_values("launch_date",ascending=False,na_position="last").drop_duplicates("mission_name").head(4)
 cols=st.columns(min(4,max(1,len(latest))))
 for c,(_,row) in zip(cols,latest.iterrows()):
  with c,st.container(border=True):
   st.caption(f"{row.planet.upper()} · {row.launch_date}")
   st.markdown(f"**{row.mission_name}**")
   st.write(row.mission_objective)
   if str(row.official_source).startswith("http"):st.markdown(f"[Record source ↗]({row.official_source})")

def render_timeline():
 d=data();header("MISSION HISTORY","Mission Timeline","Launch-to-landing ranges for distinct missions with parseable dates; this is not mission operating duration.")
 p=st.selectbox("Destination",["All","Moon","Mars"]);v=d if p=="All" else d[d.planet.eq(p)]
 m=v.sort_values("launch_date").drop_duplicates("mission_name").copy();m["start"]=pd.to_datetime(m.launch_date,errors="coerce");m["finish"]=pd.to_datetime(m.landing_date,errors="coerce");m=m.dropna(subset=["start","finish"]);px=pxmod()
 if px and len(m):
  fig=px.timeline(m,x_start="start",x_end="finish",y="mission_name",color="planet",hover_data=["agency","launch_date","landing_date"]);fig.update_yaxes(autorange="reversed");st.plotly_chart(theme(fig),use_container_width=True)
 elif len(m):
  st.dataframe(m[["mission_name","planet","launch_date","landing_date"]],hide_index=True,use_container_width=True)
 names=m.mission_name.tolist()
 if names:
  n=st.selectbox("Mission details",names);g=v[v.mission_name.eq(n)];x=g.iloc[0]
  st.subheader(n);st.write(f"**Agency:** {x.agency} · **Launch:** {x.launch_date} · **Landing:** {x.landing_date} · **End:** {x.mission_end_date}");st.write(f"**Objective:** {x.mission_objective}");st.write("**Equipment:** "+", ".join(g.equipment_name.tolist()))
  if str(x.official_source).startswith("http"):st.markdown(f"[Listed source]({x.official_source})")
 else:st.info("No parseable dates.")
def render_science():
 d=data();header("SCIENCE & DISCOVERY","Science behind the stories","Objectives and contributions recorded for catalog equipment.")
 for p in ["Moon","Mars"]:
  rows=d[d.planet.eq(p)][["mission_name","mission_objective","scientific_contribution"]].drop_duplicates()
  with st.expander(f"{p}: objectives ({len(rows)} records)",expanded=p=="Moon"):
   for _,x in rows.iterrows():st.markdown(f"**{x.mission_name}** — {x.mission_objective}");st.caption(str(x.scientific_contribution))
 px=pxmod()
 if px:
  a,b=st.columns(2)
  with a:st.plotly_chart(theme(px.histogram(d,x="equipment_category",color="planet",title="Equipment categories")),use_container_width=True)
  with b:st.plotly_chart(theme(px.histogram(d,x="current_status",color="planet",title="Recorded status")),use_container_width=True)
 else:
  st.bar_chart(d.groupby("equipment_category").size(),use_container_width=True,color="#16899A")
  st.bar_chart(d.groupby("current_status").size(),use_container_width=True,color="#16899A")
 q=validate_data(d);st.markdown("### Dataset quality");st.write(f"{q['total_records']} rows · {len(q['duplicate_ids'])} duplicate IDs · {q['missing_sources']} missing sources · {len(q['invalid_sources'])} malformed source URLs · {len(q['invalid_dates'])} malformed dates · {len(q['invalid_date_order'])} date-order issues.");st.caption("Structural checks do not independently verify historical claims.")
def render_legacy():
 d=data();header("FIELD STORIES","The Legacy Room","Source-linked stories from this equipment archive.")
 for i in ["MOON-003","MOON-005","MOON-006","MARS-004","MARS-006","MARS-008","MARS-009"]:
  g=d[d.equipment_id.eq(i)]
  if g.empty:continue
  x=g.iloc[0]
  with st.container(border=True):
   st.markdown(f"### {x.equipment_name}");st.caption(f"{x.mission_name} · {x.planet} · {x.current_status}");a,b=st.columns([1,2])
   with a:photo(x)
   with b:
    st.markdown(f"**Mission:** {x.mission_objective}");st.markdown(f"**Contribution:** {x.scientific_contribution}");st.markdown(f"**Status:** {x.current_status}. {x.verification_notes}");st.markdown("**Why it remained:** "+str(x.get("why_left") or "No separately verified explanation."))
    if str(x.official_source).startswith("http"):st.markdown(f"[Read source]({x.official_source})")
def render_quiz():
 qs=[("Which Apollo mission returned parts of Surveyor 3?",["Apollo 11","Apollo 12","Apollo 14","Apollo 17"],1,"Apollo 12 astronauts returned parts including the TV camera."),("What was ALSEP designed to do?",["Return soil automatically","Run long-term lunar experiments","Navigate Mars","Carry astronauts to orbit"],1,"ALSEP packages collected geophysical and environmental measurements."),("What reflects laser pulses for lunar ranging?",["Heat shield","Retroreflector","Seismometer","Parachute"],1,"Apollo retroreflectors return laser pulses."),("Sojourner belonged to which mission?",["Mars Pathfinder","Viking 1","InSight","Mars 2020"],0,"Sojourner was deployed by Mars Pathfinder in 1997."),("What was InSight’s focus?",["Study Mars interior","Search canals","Return samples","Map Moon"],0,"InSight studied Mars’ interior and seismic activity."),("What did the Lunar Roving Vehicle do?",["Extend astronaut traverses","Launch from Moon","Return samples","Drill mantle"],0,"The LRV extended Apollo 15, 16 and 17 surface traverses."),("Which rover landed in Jezero in 2021?",["Spirit","Curiosity","Perseverance","Opportunity"],2,"Perseverance landed in Jezero Crater in February 2021.")]
 header("KNOWLEDGE CHECK","Quiz: machines and missions","Seven questions with explanations after each answer.")
 if st.session_state.get("quiz_done"):
  st.success(f"Score: {st.session_state.quiz_score}/{len(qs)}")
  if st.button("Restart quiz",type="primary"):
   for k in list(st.session_state):
    if k.startswith("quiz_"):del st.session_state[k]
   st.rerun()
  return
 for i,(q,opts,ans,why) in enumerate(qs):
  with st.container(border=True):
   st.markdown(f"**{i+1}. {q}**");c=st.radio("Choose",opts,key=f"quiz_answer_{i}",index=None,label_visibility="collapsed")
   if st.button("Check answer",key=f"quiz_check_{i}"):st.session_state[f"quiz_checked_{i}"]=True
   if st.session_state.get(f"quiz_checked_{i}"):
    if c is None:st.warning("Select an answer.")
    elif opts.index(c)==ans:st.session_state[f"quiz_correct_{i}"]=True;st.success("Correct. "+why)
    else:st.session_state[f"quiz_correct_{i}"]=False;st.error("Not quite. "+why)
 if st.button("Finish quiz",type="primary"):
  if not all(st.session_state.get(f"quiz_checked_{i}") and st.session_state.get(f"quiz_answer_{i}") is not None for i in range(len(qs))):st.warning("Answer and check each question.")
  else:st.session_state.quiz_score=sum(bool(st.session_state.get(f"quiz_correct_{i}")) for i in range(len(qs)));st.session_state.quiz_done=True;st.rerun()
def render_planetary_experience():
 header("PLANETARY EXPERIENCE","Surface globe","Illustrative globes, not exact terrain or historical equipment models.")
 p=st.selectbox("Choose a world",["Moon","Mars"]);color="#b8c2cf" if p=="Moon" else "#bd6543"
 html=f"""<html><head><style>body{{margin:0;background:#F7F9FC;color:#334155;font:15px Arial}}#r{{height:400px;display:grid;place-items:center;position:relative;overflow:hidden}}.g{{width:min(55vw,310px);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 33% 30%,#91a3b5,#55677b 40%,#17243a 75%);box-shadow:inset -32px -12px 45px #08111dcc;animation:s 22s linear infinite}}@keyframes s{{to{{transform:rotate(360deg)}}}}#label{{position:absolute;bottom:18px;left:20px;color:#64748B}}canvas{{position:absolute;inset:0}}</style></head><body><div id="r"><div class="g"></div><div id="label">Illustrative {p} · drag to rotate · scroll to zoom</div></div><script type="module">import * as T from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';let r=document.querySelector('#r');try{{let s=new T.Scene(),c=new T.PerspectiveCamera(38,r.clientWidth/r.clientHeight,.1,100);c.position.z=4;let w=new T.WebGLRenderer({{alpha:true,antialias:true}});w.setSize(r.clientWidth,r.clientHeight);r.appendChild(w.domElement);let o=new T.Mesh(new T.SphereGeometry(1,48,48),new T.MeshStandardMaterial({{color:'{color}',roughness:.9}}));s.add(o,new T.HemisphereLight(0xdcecff,0x243247,2));let l=new T.DirectionalLight(0xffffff,2);l.position.set(-3,2,4);s.add(l);let d=false,x=0,y=0;w.domElement.onpointerdown=e=>{{d=true;x=e.clientX;y=e.clientY}};onpointerup=()=>d=false;w.domElement.onpointermove=e=>{{if(d){{o.rotation.y+=(e.clientX-x)*.01;o.rotation.x+=(e.clientY-y)*.01;x=e.clientX;y=e.clientY}}}};w.domElement.onwheel=e=>c.position.z=Math.max(2,Math.min(7,c.position.z+e.deltaY*.004));function f(){{requestAnimationFrame(f);w.render(s,c)}}f()}}catch(e){{}}</script></body></html>"""
 components.html(html,height=410,scrolling=False);st.caption("Three.js loads from jsDelivr. CSS globe remains as fallback; all globes are illustrative.")
 d=data();x=d[(d.planet.eq(p))&d.location_coordinates.fillna("").str.contains(r"\d")]
 st.markdown("### Records with coordinate text")
 if len(x):st.dataframe(x[["equipment_name","mission_name","location_name","location_coordinates","official_source"]],hide_index=True,use_container_width=True);st.caption("Coordinates displayed as recorded, not geocoded.")
 else:st.info("No coordinate strings listed.")
