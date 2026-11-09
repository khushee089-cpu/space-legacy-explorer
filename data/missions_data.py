"""
SPACE LEGACY EXPLORER - Missions & Discarded Equipment Data
NASA Space Apps Challenge 2026: "Abandoned but not Forgotten"

Authentic, verified historical records from NASA missions to the Moon and Mars.
All photographs from official NASA archives with documented NASA IDs.
"""

PROJECT_METADATA = {
    "title": "SPACE LEGACY EXPLORER",
    "agency": "NASA SPACE APPS CHALLENGE 2026",
    "challenge_name": "NASA Space Apps Challenge 2026",
    "challenge_topic": "Abandoned but not Forgotten: Storytelling about NASA's Discarded Equipment on the Moon and Mars",
    "tagline": "EVERY MISSION LEAVES A LEGACY.",
    "subtitle": "Discover the forgotten explorers, abandoned machines and scientific stories hidden across the Moon and Mars.",
    "purpose_statement": (
        "Across six decades of extraterrestrial exploration, humanity has deployed robotic laboratories "
        "and crewed landers onto the surfaces of the Moon and Mars. When their primary operational objectives concluded, "
        "descent stages, retroreflectors, seismic packages, and robotic rovers remained behind in the planetary environment. "
        "Far from being discarded debris, these artifacts constitute a permanent archaeological record of human science—"
        "deliberately engineered as expendable launch structures to conserve return fuel mass, installed as permanent laser sentinels, "
        "or brought to rest only after surviving years beyond their engineered design lifespans."
    )
}

VERIFIED_METRICS = [
    {
        "label": "Apollo Surface Sites",
        "value": "6 Missions",
        "detail": "Descent stages & ALSEP stations preserved"
    },
    {
        "label": "Martian Surface Epoch",
        "value": "48+ Years",
        "detail": "Continuous surface science since Viking 1 (1976)"
    },
    {
        "label": "Laser Range Precision",
        "value": "±1 Millimeter",
        "detail": "Apollo 11, 14, 15 retroreflectors still active"
    },
    {
        "label": "Archival Integrity",
        "value": "100% Verified",
        "detail": "Official NASA mission & telemetry records"
    }
]

FEATURED_DESTINATIONS = [
    {
        "id": "moon",
        "title": "Explore the Moon",
        "destination": "The Moon (Earth's Natural Satellite)",
        "badge": "LUNAR SECTOR",
        "photo_file": "nasa_moon_apollo11.jpg",
        "photo_title": "Apollo 11 LM Descent Stage at Tranquility Base",
        "photo_credit": "NASA / Apollo 11 Crew • NASA ID: as11-40-5917",
        "summary": (
            "Explore six Apollo Lunar Module descent stages, the Apollo Lunar Surface Experiments Packages (ALSEP), "
            "Lunar Roving Vehicles, and the robotic Surveyor soft landers standing in the lunar vacuum."
        ),
        "key_relics": [
            "Apollo 11 LM Descent Stage & Laser Retroreflector (Tranquility Base)",
            "Apollo 15, 16, 17 Lunar Roving Vehicles ('Moon Buggies')",
            "Surveyor 3 Robotic Lander (inspected by Apollo 12)",
            "Passive and Active Lunar Seismic Experiment Packages"
        ],
        "why_left": "The descent stage served as the launch platform for crew return; lifting heavy structural metal exceeded fuel mass budgets.",
        "scientific_legacy": "Millimeter-precision laser retroreflectors continue measuring lunar distance and gravitational physics after 55+ years.",
        "route": "pages/1_Explore_Moon.py",
        "theme_color": "#4CC9D8"
    },
    {
        "id": "mars",
        "title": "Explore Mars",
        "destination": "Mars (The Red Planet)",
        "badge": "MARTIAN SECTOR",
        "photo_file": "nasa_mars_rover.jpg",
        "photo_title": "Curiosity Rover on the Martian Surface",
        "photo_credit": "NASA / JPL-Caltech / MSSS • NASA ID: PIA16458",
        "summary": (
            "Discover the landmark rovers and stationary landers that charted Mars: "
            "from Viking 1 & 2 in 1976 to Opportunity's marathon traverse, Spirit's silica hunt, InSight's seismic dome, and Ingenuity."
        ),
        "key_relics": [
            "MER Opportunity (45.16 km traverse across Meridiani Planum)",
            "Viking 1 & 2 Landers (First long-term operational Martian platforms, 1976)",
            "InSight Mars Lander & SEIS Dome (Recorded 1,319+ marsquakes)",
            "Ingenuity Mars Helicopter (72 historic flights across Jezero Crater)"
        ],
        "why_left": "Atmospheric dust deposition on solar arrays, cryogenic winter nights, and planetary escape mass limitations.",
        "scientific_legacy": "Provided definitive evidence of ancient liquid water environments, hydrothermal systems, and active marsquakes.",
        "route": "pages/2_Explore_Mars.py",
        "theme_color": "#E58B55"
    },
    {
        "id": "equipment",
        "title": "Explore NASA Equipment",
        "destination": "Planetary Hardware Catalog",
        "badge": "EQUIPMENT ARCHIVE",
        "photo_file": "nasa_surveyor3_lunar.jpg",
        "photo_title": "Apollo 12 Astronaut Alan Bean Inspecting Surveyor 3",
        "photo_credit": "NASA / Apollo 12 Crew • NASA ID: AS12-48-7134",
        "summary": (
            "Technical analysis of aerospace equipment: descent rocket engines, retroreflector corner cubes, "
            "radioisotope thermoelectric generators (RTGs), panoramic cameras, supersonic parachutes, and sky cranes."
        ),
        "key_relics": [
            "Lunar Laser Ranging Retroreflectors (fused silica corner cubes)",
            "Radioisotope Thermoelectric Generators (SNAP-27 nuclear power)",
            "Sky Crane Descent Stages & Heat Shields (Curiosity & Perseverance)",
            "Sojourner Microrover & Carl Sagan Memorial Station Airbags"
        ],
        "why_left": "Calculated staging architectures: expendable descent equipment delivered payloads with maximum science mass.",
        "scientific_legacy": "Engineering data on radiation exposure, micrometeoroid impacts, and material degradation inform Artemis architecture.",
        "route": "pages/3_Equipment_Explorer.py",
        "theme_color": "#76A9FA"
    }
]

AUTHENTIC_MISSION_FACTS = [
    {
        "category": "LUNAR ARCHIVES",
        "mission": "Apollo 11 Laser Ranging Retroreflector",
        "location": "Mare Tranquillitatis (Tranquility Base)",
        "fact": "Placed on July 20, 1969, the Lunar Laser Ranging Retroreflector is the only Apollo surface equipment still in active scientific operation. Terrestrial laser observatories regularly bounce pulses off its 100 fused-silica prisms, measuring lunar distance to millimeter precision and proving the Moon drifts outward at ~3.8 centimeters per year."
    },
    {
        "category": "MARTIAN MONUMENTS",
        "mission": "Opportunity Rover (MER-B)",
        "location": "Perseverance Valley, Meridiani Planum",
        "fact": "Engineered for a nominal 90-sol mission, Opportunity remained operational for 14 years and 138 days, driving 45.16 kilometers across Mars before the 2018 global dust storm obscured its solar arrays. It discovered hematite spherules ('blueberries') and sulfate deposits that confirmed past standing liquid water."
    },
    {
        "category": "HISTORIC HARDWARE INSPECTION",
        "mission": "Apollo 12 Visits Surveyor 3",
        "location": "Oceanus Procellarum (Ocean of Storms)",
        "fact": "In November 1969, Apollo 12 astronauts Pete Conrad and Alan Bean landed within 183 meters of the Surveyor 3 robotic probe, which had soft-landed 2.5 years earlier in April 1967. They detached its television camera and returned it to Earth, providing humanity's first direct study of material degradation in prolonged lunar vacuum."
    },
    {
        "category": "GEODYNAMICS MONUMENT",
        "mission": "InSight Mars Lander",
        "location": "Elysium Planitia, Mars",
        "fact": "From November 2018 to December 2022, InSight's ultra-sensitive French SEIS seismometer detected 1,319 marsquakes. This data mapped the Martian interior for the first time, proving Mars possesses a liquid metallic core with an approximate radius of 1,780 kilometers."
    }
]

WHY_EQUIPMENT_REMAINS = [
    {
        "pillar": "Rocket Equation & Fuel Mass Budgets",
        "description": "Every kilogram returned from a celestial surface requires exponential propellant for ascent and trans-Earth injection. Leaving descent stages, heavy landing gear, and non-essential structural members conserved lifting capacity for priceless geological samples."
    },
    {
        "pillar": "Permanent Stationary Scientific Observatories",
        "description": "Retroreflectors, seismometers, and solar wind monitors were engineered as permanent geodetic markers and long-baseline science stations. Their scientific objective was to remain in place continuously over decades."
    },
    {
        "pillar": "Planetary Environmental Longevity",
        "description": "Martian atmospheric dust storms blocking solar panels, cryogenic lunar nights plunging to -246°C, and cosmic radiation naturally concluded active mission operations. Rather than waste, these units represent historic archaeological monuments."
    }
]
