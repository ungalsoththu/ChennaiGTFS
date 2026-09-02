# Chennai One feeds

A second, independently collected set of GTFS feeds for the same city, covering
all three modes — MTC buses, CMRL Metro and, for the first time, **Southern
Railway's Chennai suburban network**.

These sit beside the feeds already in `data/`; nothing there is modified. See
[Why these are separate files](#why-these-are-separate-files) for why they are
not merged into them.

| Feed | Routes | Trips/day | Stops | Shape points | ZIP |
|------|-------:|----------:|------:|-------------:|-----|
| [`mtc/`](mtc) — MTC buses | 1,026 | 50,497 | 3,271 | 968,045 | [`chennai-one-mtc-gtfs.zip`](../chennai-one-mtc-gtfs.zip) |
| [`cmrl/`](cmrl) — CMRL Metro | 3 | 822 | 41 | 1,120 | [`chennai-one-cmrl-gtfs.zip`](../chennai-one-cmrl-gtfs.zip) |
| [`suburban/`](suburban) — Southern Railway suburban + MRTS | 599 | 612 | 105 | 137,922 | [`chennai-one-suburban-gtfs.zip`](../chennai-one-suburban-gtfs.zip) |

## What these add

Against the limitations this repo already documents:

| Gap noted in the root README | In these feeds |
|---|---|
| "No suburban rail — this is the biggest gap" | 599 routes with exact times and track-matched geometry |
| "MTC shapes: straight-line per route" | 968,045 points map-matched to the road network |
| "CMRL schedules: frequency bands, not exact departure times" | 822 trips with per-station arrival and departure times |
| "CMRL shapes: straight-line, track geometry unavailable" | 1,120 points snapped to the metro alignment |

MTC trips also carry a `service_tier` column (ORDINARY, EXECUTIVE, EXPRESS, AC,
SPECIAL, NON_AC) — the board type the operator runs the trip under. It is an
extra column, ignored by any standard GTFS reader.

## Source and method

Collected from the **Chennai One** app, the CUMTA-backed multimodal app that
carries all three operators, so bus, metro and suburban schedules come from one
consistent source. Timetables are per stop, so each trip's times are the
operator's own, not interpolated.

- **Stops** are deduplicated. One physical stop appears in the source many times
  under near-identical names and slightly different coordinates — Kilambakkam
  terminus alone has 12 records spread over ~110 m. Records are clustered by
  normalised name within 200 m, then by shared distinctive token within 75 m,
  then unconditionally within 5 m. That takes 9,422 MTC records to 3,271 stops.
- **Bus shapes** are produced by routing each working's whole stop sequence in a
  single OSRM call against the OSM road network and keeping the returned
  polyline. Routing stop-pair by stop-pair and re-stitching is what produces the
  looping geometry seen in other Chennai feeds.
- **Rail shapes** are produced by Dijkstra routing over OSM rail geometry, with
  separate graphs per mode so Metro cannot leak onto suburban track.
- **Shape geometry is simplified** with Douglas-Peucker at 1 m, below the
  positional accuracy of the centrelines the routes were matched against. This
  drops 54% of bus vertices without moving a line off its road.
- **Times are unwrapped across midnight** — a trip leaving at 22:25 and arriving
  after midnight counts on past 24:00:00 rather than resetting to 00:xx.
- **Trips are attributed by trip id.** A trip appears in the timetable of every
  route whose stops it passes — one suburban train shows up under 558 route
  entries — and its id names the route that runs it. Keying on (route, trip id)
  instead multiplies 52,000 real trips into 973,000.
- Routes with nothing scheduled on them, trips with fewer than two stop times,
  and stops nothing calls at are dropped rather than published broken.
- **Placeholder stations are dropped.** CMRL files its Phase-2 construction
  stations under names like `[TEST]-0417` — ten of them along the Poonamallee
  alignment, with real coordinates and a full timetable. They are not stations
  anyone can board at, and publishing them would put an unbuilt line in the feed
  as though it were in service.

## Why these are separate files

The two collections are not mergeable row for row:

|  | this repo's `data/mtc` | `chennai-one/mtc` |
|---|---|---|
| route rows | 4,611 | 1,026 services over 4,072 workings |
| distinct `route_short_name` | 2,305 (`101 CT1`, `101 CT11`, … counted separately) | 1,026 |
| stops | 5,580 | 3,271 deduplicated |
| stop names in common | 1,390 | 1,390 |

The route ids come from different collections, so there is no key to join on and
grafting these shapes onto the existing route ids would be guesswork. Publishing
them side by side lets both be used and compared. If you would rather these
replace or merge into the primary feeds, say so on the PR and we will do that
work.

## Licence

Published under ODbL, the same licence as the rest of this repo.
