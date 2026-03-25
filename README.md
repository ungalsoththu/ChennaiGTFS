# ChennaiGTFS — Open Transit Data for Chennai

[![Ithu Ungal Soththu](https://img.shields.io/badge/Powered%20by-Ithu%20Ungal%20Soththu-maroon?style=flat-square)](https://ungalsoththu.zo.space)
[![GitHub last commit](https://img.shields.io/github/last-commit/ungalsoththu/ChennaiGTFS?style=flat-square)](https://github.com/ungalsoththu/ChennaiGTFS)
[![License: PDDL](https://img.shields.io/badge/License-PDDL-brightgreen?style=flat-square)](https://opendatacommons.org/licenses/pddl/)

> **Mission**: Build and maintain open [GTFS](https://gtfs.org) feeds for every public transit operator in Chennai — MTC buses, CMRL Metro, Southern Railway suburban, MRTS — so any app can consume unified Chennai transit data.

---

## What's GTFS?

The **General Transit Feed Specification (GTFS)** is an open data format for public transportation schedules and associated geographic information. Developed by Google in 2005 for Google Transit, it has become the global standard — used by over **10,000 transit operators** in **100+ countries**.

GTFS answers: What routes exist? Where are the stops? What time do vehicles arrive? How much does the fare cost? It is the foundation that allows trip planners, mobile apps, and data analysts to work with transit data without custom integrations for each operator.

---

## Repository Structure

```
ChennaiGTFS/
├── README.md
├── LICENSE
├── data/
│   ├── mtc/                     # MTC bus GTFS (agency-specific)
│   │   ├── agency.txt
│   │   ├── routes.txt
│   │   ├── stops.txt
│   │   ├── trips.txt
│   │   ├── stop_times.txt
│   │   ├── calendar.txt
│   │   ├── calendar_dates.txt   # Special service dates
│   │   ├── frequencies.txt      # Headway-based timing
│   │   ├── shapes.txt           # Route geometry (straight-line)
│   │   ├── routesExtended.txt   # Extended route info
│   │   └── feed_info.txt
│   ├── cmrl/                    # CMRL Metro GTFS (agency-specific)
│   │   ├── agency.txt
│   │   ├── routes.txt
│   │   ├── stops.txt
│   │   ├── trips.txt
│   │   ├── stop_times.txt
│   │   ├── calendar.txt
│   │   ├── frequencies.txt
│   │   ├── shapes.txt
│   │   └── feed_info.txt
│   ├── mtc-gtfs.zip            # MTC bus feed bundle
│   ├── cmrl-gtfs.zip           # CMRL metro feed bundle
│   ├── chennai-unified-gtfs.zip # MTC + CMRL combined (see unified/)
│   └── unified/                 # Combined feed (WIP — add suburban rail + MRTS)
│       ├── agency.txt           # Both MTC + CMRL agencies
│       ├── routes.txt
│       ├── stops.txt
│       ├── trips.txt
│       ├── stop_times.txt
│       ├── calendar.txt
│       ├── feed_info.txt
│       └── chennai-unified-gtfs.zip
```

---

## Download

| Feed | File | Size |
|------|------|------|
| MTC Buses | `data/mtc-gtfs.zip` | ~9 MB |
| CMRL Metro | `data/cmrl-gtfs.zip` | ~5 KB |
| **Unified (both)** | `data/chennai-unified-gtfs.zip` | ~9 MB |

> **⚠️ Note**: `cmrl-gtfs.zip` is ~5 KB because CMRL publishes frequency-based schedules (headway, not exact times). The unified feed embeds CMRL's full GTFS which is compact.

---

## How to Consume GTFS Feeds

GTFS feeds are consumed by **trip planners**, **mobile apps**, **mapping tools**, and **analytics platforms**. Download a `.zip`, unzip, and point your tool at the files.

### Consumer Apps & Platforms

| App / Platform | Type | How it uses GTFS |
|---|---|---|
| **Google Maps** | Trip planner | Schedules + routing for Chennai transit |
| **OpenTripPlanner (OTP)** | Open-source router | Build your own multimodal trip planner |
| **OpenStreetMap (OSM)** | Map data | GTFS feeds improve transit stop accuracy |
| **Transit App** | Mobile (iOS/Android) | Real-time arrivals from GTFS schedule |
| **Namma Yatri** | Indian trip planner | Bengaluru has GTFS; Chennai GTFS enables integration |
| **Tummoc** | Indian Mobility-as-a-Service | Bengaluru GTFS pilot; ready for Chennai |
| **NavICy** | Indian navigation | Open-source routing platform |
| **gtfs-via-websocket** | Real-time overlay | Visualize GTFS schedules on a map |
| **TransitLand** | Global transit registry | Discovers and indexes GTFS feeds |
| **Transit Screen** | Agency dashboards | Monitor service frequency and coverage |

### Quick Start: Build a Trip Planner with OpenTripPlanner

```bash
# 1. Download feeds
curl -LO https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/chennai-unified-gtfs.zip
unzip chennai-unified-gtfs.zip -d /opt/gtfs/chennai

# 2. Download OSM map
curl -LO https://download.openstreetmap.fr extracts/asia/india/tamil-nadu-latest.osm.pbf

# 3. Build OTP graph
java -jar otp-2.x.x.jar --build /opt/otp/chennai-graph --gtfs /opt/gtfs/chennai/*.txt --osm /opt/gtfs/tamil-nadu.osm.pbf

# 4. Start OTP server
java -jar otp-2.x.x.jar --load --serve /opt/otp/chennai-graph
# → Trip planner at http://localhost:8080
```

### Quick Start: Python Analysis

```python
import gtfs_kit

feed = gtfs_kit.Feed.from_file("chennai-unified-gtfs.zip")
feed.validate()                      # Check data quality
feed.compute_species()              # Route and stop statistics
feed.build_stops_times_drop_off()   # Stop-level analysis
```

```R
library(tidytransit)
read_gtfs("chennai-unified-gtfs.zip") |> 
  get_stops() |>                    # List all stops
  plot_stops()                      # Map stops
```

---

## GTFS Ecosystem

### Tools that Use GTFS

**Trip Planners**
- [OpenTripPlanner](https://www.opentripplanner.org/) — Open-source multimodal router (Java)
- [OpenTransit](https://github.com/OpenTransitTools/transit-stack) — Python-based trip planner
- [Morpheus](https://github.com/reedfields/morpheus) — Lightweight GTFS router

**Analysis & Visualization**
- [gtfs-kit](https://github.com/mrcaglayeas/gtfs-kit) — Python GTFS analysis
- [tidytransit](https://github.com/r-abc/tidytransit) — R package for GTFS analysis
- [Transit Screen](https://transitscreen.com/) — Agency dashboards
- [TransitLand](https://www.transit.land/) — Global GTFS registry + map
- [TUMI GTFS Analyzer](https://坟) — Transit coverage and quality analysis

**Validation**
- [GTFS Validator](https://github.com/MobilityData/gtfs-validator) — Official MobilityData validator
- [Schedule Inspector](https://github.com/public-transport/gtfs-inspector) — Human-readable GTFS viewer

**OpenStreetMap Integration**
- [OSM2GTFS](https://github.com/gmajnavarkalva/osm2gtfs) — Generate GTFS from OSM data
- [Stop_locations](https://github.com/osmlab/stop_locations) — Align GTFS stops with OSM

**Mobile Apps**
- [Transito](https://github.com的味道/Transito) — FOSS Android app, GTFS-native
- [MaaS App](https://github.com public-transport/gtfs-via-websocket) — GTFS + real-time overlay
- [OneBusAway](https://github.com/OneBusAway/onebusaway) — Open-source transit info platform

---

## India GTFS Landscape (Gap Analysis)

*As of March 2026*

| City | Operator | GTFS Status | Official? | Notes |
|------|----------|-------------|-----------|-------|
| **Chennai** | MTC Buses | ✅ Active | Unofficial | 728 routes, 2000+ stops. Feed in this repo (source: MTC ITS). |
| **Chennai** | CMRL Metro | ✅ Built | Unofficial | 44 stations, frequency-based schedules. Built from CMRL timetable PDF. |
| **Chennai** | Suburban Rail | ❌ Missing | — | No official GTFS. Needs scraping from southernrailway.in. |
| **Chennai** | MRTS | ❌ Missing | — | No official GTFS. Contact: /r/chennai |
| **Delhi** | DMRC Metro | ✅ Official | Yes | [otd.delhi.gov.in](https://otd.delhi.gov.in/data/staticDMRC/). 262 stations. |
| **Delhi** | DIMTS Bus | ✅ Official | Yes | GTFS + GTFS-RT available. |
| **Bengaluru** | BMRCL Namma Metro | ✅ Official | Yes | Adopted GTFS in 2024 via IUDX. Google Maps live. |
| **Bengaluru** | BMTC | ✅ Official | Yes | GTFS published 2024. ~7,500 bus stops. |
| **Hyderabad** | HMRL Metro | ✅ Official | Yes | Published Nov 2024. 118 stations, 6,958 weekly trips. Google Maps live. |
| **Mumbai** | Maha Metro | ❌ Missing | — | No official GTFS. Schedule PDFs only. |
| **Mumbai** | BEST Bus | 🟡 In Progress | Partial | BEST adopting GTFS as of May 2025. |
| **Kolkata** | ERTL Metro | ✅ Official | Yes | East-West Metro has GTFS. |
| **Pune** | PMPML | ❌ Missing | — | No official GTFS. |
| **Kochi** | KMRL Metro | 🟡 Partial | Yes | Limited GTFS. |

### Key Observations

1. **Hyderabad and Bengaluru metros lead** — Both published official GTFS in 2024 with Google Maps integration. Hyderabad HMRL went further with GTFS-RT for live train positions.

2. **Chennai is the largest city without official transit GTFS** — This repo fills the gap for MTC buses and CMRL metro using public data.

3. **Suburban rail is the biggest gap** — No Indian city has published GTFS for its suburban/regional rail network (Indian Railways). This is a structural issue: railway schedules are centrally managed, data is fragmented across zones, and no single authority is accountable for open transit data.

4. **BMTC is the largest bus fleet on GTFS in India** — 7,500+ stops, 1,000+ routes. MTC is comparable in scale.

5. **Mumbai is notably underserved** — Despite being India's largest city by metro network length, Maha Mumbai Metro has no published GTFS.

---

## Roadmap

- [ ] **MTC GTFS**: Add actual route geometry (polylines from OSM, not straight lines)
- [ ] **CMRL GTFS**: Improve shapes with station-level coordinates from CMRL station pages
- [ ] **Suburban Rail GTFS**: Scrap
---

## Contributing

This repo is maintained by the [Ithu Ungal Soththu](https://ungalsoththu.zo.space) accountability project. Contributions welcome:

- **Report data errors** — Open an issue with the route/trip/stop that's incorrect
- **Improve coordinates** — Station coordinates sourced from Wikipedia/OSM may have slight errors
- **Add suburban rail** — Help scrape schedule data from [southernrailway.in](https://sr.indianrailways.gov.in/)
- **Add MRTS** — Help compile MRTS timetable from [chennaiport.in](https://chennaiport.in/)

GTFS data follows the [Open Data Commons Public Domain Dedication & License (PDDL)](https://opendatacommons.org/licenses/pddl/).

---

## Data Sources

| Agency | Source | Method |
|--------|--------|--------|
| MTC Buses | [mtcbusits.in](https://mtcbusits.in) | ITS API + data extraction |
| CMRL Metro | [chennaimetrorail.org](https://chennaimetrorail.org/wp-content/uploads/) | Timetable PDF parsing |
| CMRL Metro | [Wikipedia: Chennai Metro](https://en.wikipedia.org/wiki/List_of_Chennai_Metro_stations) | Station coordinates |
| CMRL Metro | OSM Overpass API | Station node data |

---

## References

- [GTFS Specification](https://developers.google.com/transit/gtfs) — Official reference
- [GTFS.org](https://gtfs.org) — Community hub
- [MobilityData awesome-transit](https://github.com/MobilityData/awesome-transit) — Full tool listing
- [TransitLand Feed Registry](https://www.transit.land/feeds) — Search Indian GTFS feeds
- [MobilityDatabase](https://mobilitydatabase.org/) — Global GTFS catalog
- [Delhi Open Transit Data](https://otd.delhi.gov.in/) — Reference implementation for India
- [India Urban Data Exchange (IUDX)](https://iudx.org.in/) — Platform Bengaluru used for GTFS publishing
- [TUMI GTFS Analyzer](https:// transform.github.io/gtfs-b棍n/) — Transit quality assessment

---

*Last updated: 2026-03-25 | [Submit an issue](https://github.com/ungalsoththu/ChennaiGTFS/issues) | [ChennaiGTFS on GitHub](https://github.com/ungalsoththu/ChennaiGTFS)*
