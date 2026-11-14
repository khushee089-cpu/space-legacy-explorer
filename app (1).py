import streamlit as st
import numpy as np
import plotly.graph_objects as go
from modules.navigation import render_sidebar
from modules.components import load_css, render_footer
from data.data_loader import load_equipment_data, get_summary_stats
from modules.explorer import feature_image


def add_box(fig, center, size, color, name):
    """Add a simple solid cuboid to the Plotly 3D scene."""
    cx, cy, cz = center
    sx, sy, sz = size
    vertices = [
        (cx-sx/2, cy-sy/2, cz-sz/2), (cx+sx/2, cy-sy/2, cz-sz/2),
        (cx+sx/2, cy+sy/2, cz-sz/2), (cx-sx/2, cy+sy/2, cz-sz/2),
        (cx-sx/2, cy-sy/2, cz+sz/2), (cx+sx/2, cy-sy/2, cz+sz/2),
        (cx+sx/2, cy+sy/2, cz+sz/2), (cx-sx/2, cy+sy/2, cz+sz/2),
    ]
    x, y, z = zip(*vertices)
    i = [0, 0, 4, 4, 0, 1, 2, 3, 5, 6, 7, 4]
    j = [1, 2, 5, 6, 1, 2, 3, 0, 4, 5, 6, 7]
    k = [2, 3, 6, 7, 5, 6, 7, 4, 1, 2, 3, 0]
    fig.add_trace(go.Mesh3d(
        x=x, y=y, z=z, i=i, j=j, k=k, color=color,
        name=name, flatshading=True, hovertemplate=f"{name}<extra></extra>"
    ))


def add_wheel(fig, x0, y0, z0, radius=0.42, width=0.22):
    """Add a dark cylindrical rover wheel whose axle runs along the Y axis."""
    theta = np.linspace(0, 2 * np.pi, 36)
    yy = np.array([y0 - width / 2, y0 + width / 2])
    T, Y = np.meshgrid(theta, yy)
    X = x0 + radius * np.cos(T)
    Z = z0 + radius * np.sin(T)
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, showscale=False, colorscale=[[0, "#252d38"], [1, "#687584"]],
        cmin=0, cmax=1, name="Rover wheel",
        hovertemplate="Six-wheel mobility system<extra></extra>"
    ))
    # Raised wheel hub on the outward-facing side
    outer_y = y0 + (width / 2 + 0.012) * (1 if y0 >= 0 else -1)
    fig.add_trace(go.Scatter3d(
        x=[x0], y=[outer_y], z=[z0], mode="markers",
        marker=dict(size=8, color="#c5ced8", line=dict(color="#596575", width=1)),
        name="Wheel hub", hoverinfo="skip", showlegend=False
    ))


def build_mars_rover_figure():
    """Create an illustrative, interactive rover model using Plotly geometry."""
    fig = go.Figure()

    # Main chassis and upper equipment deck
    add_box(fig, (0, 0, 1.35), (2.45, 1.45, 0.62), "#cbd3dc", "Rover chassis")
    add_box(fig, (0, 0, 1.72), (1.65, 1.05, 0.14), "#dca94e", "Equipment deck")

    # Six wheels: three on each side
    for side in (-1, 1):
        for xpos in (-0.88, 0, 0.88):
            add_wheel(fig, xpos, side * 0.86, 0.62)

    # Camera mast and camera head
    add_box(fig, (0.18, 0, 2.23), (0.12, 0.12, 0.95), "#7c8998", "Camera mast")
    add_box(fig, (0.18, 0, 2.78), (0.68, 0.34, 0.30), "#e0e5eb", "Camera head")
    add_box(fig, (0.18, -0.18, 2.78), (0.20, 0.035, 0.16), "#263f5b", "Camera lens")

    # Robotic arm and science instrument
    add_box(fig, (-0.86, -0.10, 1.88), (0.82, 0.13, 0.13), "#aeb8c4", "Robotic arm")
    add_box(fig, (-1.27, -0.10, 1.68), (0.16, 0.16, 0.34), "#d7dde4", "Science tool")

    # Solar panel and antenna support
    add_box(fig, (0.98, 0.02, 1.93), (0.72, 0.10, 0.46), "#245b91", "Solar panel")
    add_box(fig, (0.98, 0.02, 2.20), (0.10, 0.10, 0.34), "#8b98a8", "Antenna support")

    fig.update_layout(
        height=590,
        margin=dict(l=0, r=0, t=38, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e8edf3"),
        showlegend=False,
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, range=[-2.0, 2.0]),
            yaxis=dict(visible=False, range=[-1.65, 1.65]),
            zaxis=dict(visible=False, range=[0, 3.25]),
            aspectmode="data",
            camera=dict(eye=dict(x=2.2, y=2.3, z=1.55)),
            dragmode="orbit"
        ),
        title=dict(text="Interactive Mars Rover · 3D model", x=0.02, y=0.98)
    )
    return fig

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

st.markdown("### Explore a Mars rover in 3D")
st.write("Inspect an illustrative rover model. Drag to orbit through 360°, scroll to zoom, and use the modebar controls for additional view options.")
with st.container():
    st.plotly_chart(
        build_mars_rover_figure(),
        use_container_width=True,
        config={"scrollZoom": True, "displaylogo": False, "responsive": True}
    )
st.caption("Educational illustration, not an exact engineering replica of a specific NASA rover. The six-wheel layout, camera mast, robotic arm and solar panel are simplified visual features.")

st.markdown("### Mission control")
st.write("Browse the source-linked equipment archive, compare records in the dashboard, follow mission chronology, and explore the science and legacy behind each mission.")
st.page_link("pages/4_Mission_Dashboard.py", label="Open Mission Dashboard", use_container_width=True)
st.page_link("pages/9_Planetary_Experience.py", label="Explore the illustrative planetary globe", use_container_width=True)
st.caption("Dates, statuses, images and coordinates are shown as recorded in the bundled dataset. Consult each record’s official source and verification notes.")
render_footer()
