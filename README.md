# ChennaiGTFS

**Chennai's transit network as open, machine-readable GTFS** — MTC buses, CMRL Metro, and Southern Railway suburban — maintained by [UngalSoththu](https://github.com/ungalsoththu) (உங்கள் சொத்து).

![Version](https://img.shields.io/badge/version-0.2.0-blue) ![License](https://img.shields.io/badge/license-ODbL--PDDL-green) ![Status](https://img.shields.io/badge/status-active-brightgreen)

## Downloads

| Feed | File | Contents |
|------|------|----------|
| **Chennai Unified** | [chennai-unified-gtfs.zip](data/chennai-unified-gtfs.zip) | MTC + CMRL + SRR, ID-prefixed, 1 agency-safe merge (v0.2.0) |
| MTC buses | [mtc-gtfs.zip](data/mtc-gtfs.zip) | 4,611 routes, 5.6k stops, real timetables |
| CMRL Metro | [cmrl-gtfs.zip](data/cmrl-gtfs.zip) | 28 routes, real timetable, shapes, zone fares (see caveat) |
| Suburban rail | [srr-gtfs.zip](data/srr-gtfs.zip) | 763 services, 708 stations, pathways, Beach–Tambaram + Avadi–Arakkonam |

## Feed contents (v0.2.0)

| System | Routes | Stops/stations | Trips | Stop times | Notes |
|--------|--------|----------------|-------|------------|-------|
| MTC buses | 4,611 | 5,580 | 47,047 | 1,360,443 | Timetables from MTC app scrape; straight-line shapes |
| CMRL Metro | 28 | 254 (40 stations + entrance/platform nodes) | 625 | 12,503 | Real departure times, 4.2k shape points, zone fares, transfers |
| SRR suburban | 763 | 708 | 763 | 16,135 | First-ever public suburban GTFS for Chennai; 2,076 station pathways |
| **Unified** | **5,402** | **6,542** | **48,435** | **1.39M** | 3 agencies, 12 services, 4 calendar exceptions |

IDs are prefixed per system in the unified feed: `MTC-`, `CMRL-`, `SRR-`.

## Data sources

| System | Source | Collected |
|--------|--------|-----------|
| MTC | MTC official app (route/timetable scrape) | 2026-04 (weekly updates until 2026-04-27) |
| CMRL | [CUMTA Transit Data portal](https://test.cumta.org) (`CMRL gtfs.zip`) | 2026-10-04 |
| SRR | [CUMTA Transit Data portal](https://test.cumta.org) (`Southern Railways.zip`) | 2026-10-04 |

**On CUMTA's portal:** CUMTA quietly publishes GTFS through a test subdomain with an encrypted API and no announcement — we mirrored the feeds here for preservation and access. The portal carries no explicit license; source files remain © their agencies (CMRL / Southern Railway). This repo's compilation is published under ODbL/PDDL with attribution.

### Caveats

- **CMRL calendar is stale** — CUMTA's CMRL feed calendar ends 2021-12-31 and its fare chart is dated 22.02.2021. Treat as a historical/structural dataset (geometry, stations, zones, pathways are still valid), not a live schedule.
- **MTC times are real, CUMTA's are not** — CUMTA's `static_mtc_gtfs_data.zip` (30 MB, 4,030 routes / 7,128 stops) stamps 4,721 trips with a placeholder `00:00:15` departure; we keep our app-scraped MTC feed as the schedule source of record. [Their zip](https://test.cumta.org/static_mtc_gtfs_data.zip) is worth grabbing for the larger stop catalogue.
- **SRR is one trip per service** — Southern Railway's feed models each of 763 suburban services as a single daily trip pattern (calendar-driven), not per-train timetables.

## What's inside

```
data/
├── chennai-unified-gtfs.zip   ← all three systems merged
├── mtc-gtfs.zip               ← MTC only
├── cmrl-gtfs.zip              ← CMRL only (CUMTA-derived)
├── srr-gtfs.zip               ← suburban rail only (CUMTA-derived)
├── mtc/ cmrl/ srr/ unified/   ← same feeds, unpacked
└── *.txt                      ← unified feed, loose files
scripts/
└── harmonize_v02.py           ← reproducible merge (v0.1 → v0.2)
```

### Unified feed structure

- `agency.txt` — 3 agencies: MTC (id 69), CMRL, SR
- `calendar.txt` + `calendar_dates.txt` — 12 merged services, prefixed
- `routes.txt`, `trips.txt`, `stop_times.txt` — all schedules, prefixed IDs
- `shapes.txt` — CMRL track geometry
- `transfers.txt` — CMRL inter-station transfers
- `pathways.txt` — SRR station pathways (entrances ↔ platforms, 2,076 rows)
- `fare_attributes.txt` + `fare_rules.txt` — CMRL zone-based fares

## Consumers: use GTFS in your code

```python
# Python: parse GTFS with gtfs-kit
from gtfs_kit import feed
f = feed.read_feed("data/chennai-unified-gtfs.zip", dist_units="km")
f.compute_trips_stats()
```

```r
# R: analyze with tidytransit
library(tidytransit)
gtfs <- read_gtfs("https://github.com/ungalsoththu/ChennaiGTFS/raw/main/data/chennai-unified-gtfs.zip")
```

### Routing / trip planning

- [OpenTripPlanner](https://www.opentripplanner.org/) — feed the unified zip in as `router-config` GTFS input
- [gtfs-rt-validator](https://github.com/MobilityData/gtfs-validator) — validate any feed in this repo

### Feed registries

- [Mobility Database](https://database.mobilitydata.org/) — registered as `mdb-3360` (Chennai Transport Corporation)
- [TransitLand](https://transit.land/feeds) — indexed

---

## Why GTFS matters for Chennai

**Chennai has 3 major transit systems, and until October 2026 none published open GTFS.**

| Use case | Without GTFS | With GTFS |
|----------|--------------|-----------|
| Trip planner | Manual search | Automated routing |
| Accessibility (pathways) | ❌ | ✅ SRR pathways included |
| Intermodal (bus ↔ metro ↔ suburban) | Guess | Compute via transfers |
| Research / journalism | Scrape or survey | Clean dataset |

### What v0.2.0 changes

1. **Suburban rail gap closed** — the biggest known gap ("no suburban rail") is filled with CUMTA's SRR feed, covering Beach–Tambaram, Avadi–Arakkonam corridors and MRTS.
2. **CMRL upgraded** from frequency-band estimates to CUMTA's real timetable with track geometry and zone fares.
3. **Unified feed properly merged** — all IDs prefixed, 3 agencies, referential-validated.

## Remaining gaps

1. **MTC shapes** — still straight-line; CUMTA's MTC zip has a larger stop catalogue but placeholder times.
2. **CMRL live schedule** — source calendar expired 2021; needs CMRL to publish current timetables.
3. **GTFS-Realtime** — none of the three agencies publish vehicle positions or trip updates.
4. **MTC fare data** — no fare_attributes for buses yet.

## Contributing

Found a wrong stop, missing route, or stale schedule? [Open an issue](https://github.com/ungalsoththu/ChennaiGTFS/issues) with route number / station name / expected vs actual + source.

To rebuild the unified feed after editing per-system data:

```bash
python3 scripts/harmonize_v02.py
```

## Related

- [Ithu Ungal Soththu](https://ungalsoththu.zo.space) — Chennai transit accountability
- [CUMTA Transit Data portal](https://test.cumta.org) — the (quiet) official source we mirror
- [Mobility Database catalog](https://github.com/MobilityData/mobility-database-catalogs) — global GTFS registry

---

## License

Data compiled in this repo: [ODbL](https://opendatacommons.org/licenses/odbl/) / [PDDL](https://opendatacommons.org/licenses/pddl/) — attribute "UngalSoththu / ChennaiGTFS", keep derivatives open.

Mirrored source files (CMRL, SRR): © their respective agencies (CMRL, Southern Railway), retrieved via CUMTA's public Transit Data portal; mirrored here for preservation, research, and open access.

Powered by [Zo](https://zo.computer).
