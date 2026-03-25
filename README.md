[![Web](https://img.shields.io/badge/Ithu%20Ungal%20Soththu-1E8CBE)](https://ithuungalsoththu.vercel.app/)
[![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/UngalSoththu)](https://x.com/UngalSoththu)
[![Build Status](https://github.com/ungalsoththu/ChennaiGTFS/actions/workflows/gtfs-validation.yml/badge.svg)](https://github.com/ungalsoththu/ChennaiGTFS/actions/workflows/gtfs-validation.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Chennai GTFS

Open GTFS feeds for **Chennai public transit** — MTC buses and CMRL metro. This repository provides standardized, static GTFS (General Transit Feed Specification) data for trip planners, transit apps, and research.

## About Ithu Ungal Soththu

**Ithu Ungal Soththu** is a powerful Tamil phrase from a Vadivelu comedy scene in the 2002 Tamil film *Bagavathi*. It has become a rallying cry for accountability in Chennai's public services.

## Repository Structure

```
data/
├── mtc/                    # MTC Bus GTFS source files
│   ├── agency.txt
│   ├── routes.txt          # 4,000+ bus routes
│   ├── stops.txt           # 4,000+ bus stops  
│   ├── trips.txt
│   ├── stop_times.txt
│   ├── calendar.txt
│   └── feed_info.txt
├── cmrl/                   # CMRL Metro GTFS source files
│   ├── agency.txt
│   ├── routes.txt          # 3 metro routes
│   ├── stops.txt           # 44 metro stations
│   ├── trips.txt
│   ├── stop_times.txt
│   ├── calendar.txt
│   ├── frequencies.txt     # Headway-based scheduling
│   ├── shapes.txt          # Station-to-station geometry
│   └── feed_info.txt
├── unified/                # Combined MTC + CMRL GTFS
│   └── *.txt               # Merged feed for multi-modal apps
├── mtc-gtfs.zip            # MTC Bus GTFS (8.7 MB)
├── cmrl-gtfs.zip           # CMRL Metro GTFS (4.8 KB)
└── chennai-unified-gtfs.zip # Combined GTFS (8.7 MB)
```

## Data Coverage

| Agency | Type | Routes | Stops | Schedule Type |
|--------|------|--------|-------|---------------|
| **MTC** | Bus | 4,000+ | 4,000+ | Stop-by-stop times |
| **CMRL** | Metro | 3 | 44 | Frequency-based (headways) |
| **Combined** | Multi-modal | 4,003+ | 4,044+ | Mixed |

### CMRL Metro Lines

| Line | Stations | Length | Terminals |
|------|----------|--------|-----------|
| **Blue Line** | 26 | 29.7 km | Wimco Nagar Depot ↔ Airport |
| **Green Line** | 18 | 24.3 km | MGR Central ↔ St. Thomas Mount |
| **Inter-Corridor** | 5 | 16.4 km | MGR Central ↔ Airport |

## Using the Feeds

### Direct Download

| Feed | Download | Size |
|------|----------|------|
| MTC Bus | [`mtc-gtfs.zip`](data/mtc-gtfs.zip) | 8.7 MB |
| CMRL Metro | [`cmrl-gtfs.zip`](data/cmrl-gtfs.zip) | 4.8 KB |
| Unified | [`chennai-unified-gtfs.zip`](data/chennai-unified-gtfs.zip) | 8.7 MB |

### GTFS Tools

- **Python**: [`gtfs-kit`](https://github.com/mrcagney/gtfs_kit), [`partridge`](https://github.com/remix/partridge)
- **JavaScript**: [`gtfs`](https://github.com/ BlinkTagInc/gtfs)
- **Validation**: [MobilityData GTFS Validator](https://github.com/MobilityData/gtfs-validator)

### Example: Load with Python

```python
import pandas as pd

# Load MTC stops
stops = pd.read_csv('data/mtc/stops.txt')
print(f"Total MTC stops: {len(stops)}")

# Load CMRL routes  
routes = pd.read_csv('data/cmrl/routes.txt')
print(f"CMRL lines: {routes['route_short_name'].tolist()}")
```

## Data Sources

| Agency | Source |
|--------|--------|
| **MTC** | [mtcbus.tn.gov.in](https://mtcbus.tn.gov.in/) — Route lists and timetables |
| **CMRL** | [chennaimetrorail.org](https://chennaimetrorail.org/) — Station order and headways |
| **Stations** | Wikipedia + OSM `node[railway=station]` for verified coordinates |

## CMRL Notes

CMRL publishes **frequency-based schedules** (headways), not per-station arrival times. The GTFS uses `frequencies.txt` with `exact_times=0` to represent this. Example headways:

- Weekday peak: 5-7 minutes
- Weekend: 7-10 minutes

OSM way geometry for Chennai Metro is currently unreliable, so shapes use straight-line station-to-station connections.

## Contributing

1. **Report issues**: Open a GitHub issue for data inaccuracies
2. **Submit updates**: Pull requests with official source citations
3. **Validate**: Test with GTFS validation tools before submitting

## License

MIT License — See [LICENSE](LICENSE)

## Links

- [MTC Official](https://mtcbus.tn.gov.in/)
- [CMRL Official](https://chennaimetrorail.org/)
- [GTFS Reference](https://gtfs.org/reference/static/)
- [Ithu Ungal Soththu](https://ithuungalsoththu.vercel.app/)
