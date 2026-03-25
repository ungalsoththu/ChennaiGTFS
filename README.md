# ChennaiGTFS — Open Transit Data for Chennai

![GTFS](https://img.shields.io/badge/GTFS-v2-blue) ![Transit Systems](https://img.shields.io/badge/Systems-2-green) ![License: ODbL](https://img.shields.io/badge/License-ODbL--PDDL-red)

Open [GTFS (General Transit Feed Specification)](https://developers.google.com/transit/gtfs) feeds for Chennai's public transit systems — collected and maintained by **UngalSoththu** as part of the [Ithu Ungal Soththu](https://ungalsoththu.zo.space) accountability project.

> **Goal**: Make Chennai's transit data as open and accessible as Bengaluru, Hyderabad, and Delhi.

---

## What's in this repo

| Feed | Location | Contents |
|------|----------|----------|
| **MTC Buses** | `data/mtc/` | 728 routes, 2000+ stops |
| **CMRL Metro** | `data/cmrl/` | 44 stations, Blue + Green Lines |
| **Unified** | `data/unified/` | MTC + CMRL combined |

### Quick download

| Feed | ZIP file |
|------|----------|
| MTC Buses | [`data/mtc-gtfs.zip`](data/mtc-gtfs.zip) |
| CMRL Metro | [`data/cmrl-gtfs.zip`](data/cmrl-gtfs.zip) |
| Unified | [`data/chennai-unified-gtfs.zip`](data/chennai-unified-gtfs.zip) |

---

## Data sources

| System | Source | Collection |
|--------|--------|------------|
| MTC Buses | MTC mobile app | Collected by UngalSoththu |
| CMRL Metro | CMRL website (timetable + fare PDF) | Scraped by UngalSoththu |

### Limitations

- **MTC shapes**: Straight-line per route. Actual road paths require OSM road matching.
- **CMRL schedules**: Published as frequency bands (headway in minutes), not exact departure times. GTFS built using `frequencies.txt`.
- **CMRL shapes**: Straight-line station-to-station. Actual track geometry unavailable.
- **MTC data**: Unofficial — collected via app inspection.

---

## How to consume GTFS feeds

### Apps and platforms that use GTFS

| App / Platform | Platform | Notes |
|----------------|----------|-------|
| [Google Maps](https://maps.google.com) | All | Search transit, get schedules |
| [OneBusAway](https://onebusaway.org) | All | Real-time arrival predictions |
| [Transit](https://transitapp.com) | iOS/Android | Live departures |
| [CityMapper](https://citymapper.com/chennai) | All | Multimodal routing |
| [Namma Yatri](https://nammayatri.in) | Bengaluru | India's own MaaS platform |
| [Tummoc](https://tummoc.com) | All | Multi-city ticketing + routing |
| [OpenTripPlanner](https://www.opentripplanner.org) | Self-host | Build your own router |
| [gtfs-rt-validator` | CLI | Validate GTFS quality |

### Developers: Use GTFS in your code

```python
# Python: Parse GTFS with gtfs-kit
from gtfs_kit import feed
f = feed.Feed.from_path("chennai-unified-gtfs.zip")
f.routes  # Route list
f.stop_times  # All stop times
f.compute_stats()  # Network statistics

# R: Analyze with tidytransit
library(tidytransit)
gtfs <- read_gtfs("chennai-unified-gtfs.zip")
head(gtfs$routes)
```

### Visualization and routing

```bash
# Build a trip planner with OpenTripPlanner
git clone https://github.com/opentripplanner/otp-setup
./otp-build-and-run.sh --download --url https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/chennai-unified-gtfs.zip
```

### Submit to Google Maps

Transit agencies submit feeds via [Transit Partner Portal](https://transit.google.com/settings). Unofficial feeds can be submitted via [Google Maps Public Transit Feedback](https://support.google.com/maps/answer/2835194).

### Register in transit data registries

- [TransitLand](https://transit.land/feeds): Search and register feeds
- [Mobility Database](https://database.mobilitydata.org/): Official GTFS registry

---

## Why GTFS matters for Chennai

**Chennai has 2 major transit systems but no official open data.**

### The problem

- MTC runs 3.5 million passengers/day across 700+ routes
- CMRL runs 100+ stations across 2 lines
- Neither publishes open schedule data
- No unified, machine-readable view of Chennai's transit network

### What GTFS enables

| Use case | Without GTFS | With GTFS |
|----------|--------------|-----------|
| Trip planner | Manual search | Automated routing |
| Accessibility apps | Proprietary data | Open standard |
| Research / journalism | Scrape or survey | Clean dataset |
| Intermodal connections | Guess | Compute |
| Feed to Google Maps | ❌ | ✅ |
| MaaS apps (Namma Yatri, Tummoc) | ❌ | ✅ |

---

## India GTFS landscape

| City | System | GTFS Status | Official? | Feed Source |
|------|--------|-------------|----------|-------------|
| **Hyderabad** | Hyderabad Metro (L&T) | ✅ Available | Yes | [HMRL official](https://hmrl.telangana.gov.in) |
| **Bengaluru** | BMTC + BMRCL | ✅ Available | Yes | [IUDX Mobility Platform](https://iudx.org.in) |
| **Delhi** | DMRC + DIMTS | ✅ Available | Yes | [Open Transit Delhi](https://otd.delhi.gov.in) |
| **Kolkata** | East-West Metro | ✅ Available | Yes | Rail Metro official |
| **Mumbai** | MMRDA Metro + BEST | ❌ No feed | — | — |
| **Pune** | PMPML | 🟡 Limited | Partial | Unofficial efforts |
| **Kochi** | Kochi Metro | 🟡 Limited | Partial | Unofficial |
| **Chennai** | MTC + CMRL | 🟡 This repo | Unofficial | Collected here |
| **All cities** | Indian Railways (Suburban) | ❌ None | — | Not published anywhere |

### Key insight

Hyderabad and Bengaluru publish **official GTFS**. Chennai's civic tech community is filling the gap with this repo. The Hyderabad HMRL GTFS published Nov 2024 shows what's possible when metro authorities engage with open data standards.

---

## Project status

| System | Routes / Stations | Shapes | Schedules | Notes |
|--------|-------------------|--------|-----------|-------|
| MTC Buses | 728 routes | ⚠️ Straight-line | ✅ Timetable | Collected via MTC app |
| CMRL Blue Line | 26 stations | ⚠️ Straight-line | ✅ Headway-based | Frequency-only data |
| CMRL Green Line | 18 stations | ⚠️ Straight-line | ✅ Headway-based | Frequency-only data |

### Known gaps

1. **No suburban rail** — Chennai's Southern Railway suburban system (MRTS + main line) has zero GTFS data. This is the biggest gap.
2. **No exact CMRL departure times** — CMRL publishes only headways, not precise schedules.
3. **Straight-line shapes** — Actual road/track geometry not modeled.
4. **No real-time** — GTFS is static (schedule only). GTFS-RT requires operator cooperation.

---

## How to contribute

Found an error? Open an issue or PR.

### Improve data quality

```bash
# Clone the repo
git clone https://github.com/ungalsoththu/ChennaiGTFS.git
cd ChennaiGTFS

# Edit station coordinates, route names, or schedules
# Test your GTFS
python3 -c "from gtfs_kit import feed; f = feed.Feed.from_path('data/cmrl-gtfs.zip'); print(f.compute_stats())"
```

### Report a data issue

Open an issue with:
- Route number or station name
- Expected vs actual data
- Source that shows correct information

---

## Related projects

- [Ithu Ungal Soththu](https://ungalsoththu.zo.space) — Chennai MTC accountability project
- [MTC Watchdog Grievance Scout](/?t=automations) — Automated MTC complaint monitoring
- [TransitLand](https://transit.land) — Global GTFS registry (ChennaiGTFS feeds already indexed)
- [OpenTripPlanner](https://www.opentripplanner.org/) — Open-source multimodal router

---

## License

All data in this repo is published under [ODbL (Open Database License)](https://opendatacommons.org/licenses/odbl/).

**You are free to:**
- Share: copy and redistribute the material
- Use: commercial and non-commercial purposes

**You must:**
- Attribute: credit "UngalSoththu / Ithu Ungal Soththu"
- Keep derivatives open: if you remix or build on this data, publish under ODbL

---

<p align="center">
  <a href="https://ungalsoththu.zo.space">
    <img src="https://img.shields.io/badge/Powered%20by-Zo%20Computer-7B3FE4?style=for-the-badge&logo=zoom&logoColor=white" alt="Powered by Zo Computer" />
  </a>
</p>
