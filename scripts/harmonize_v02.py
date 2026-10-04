#!/usr/bin/env python3
"""Harmonize v0.2.0: vendor CUMTA-portal CMRL + SRR feeds, rebuild unified feed.

Sources:
  - our MTC feed:  data/mtc (unchanged, real timetable from MTC app collection)
  - CUMTA CMRL:    archive unpacked "CMRL gtfs" (real timetable, zone fares, shapes;
                   calendar expired 2021-12-31 - historical data)
  - CUMTA SRR:     archive unpacked "chennai.suburban.gtfs" (first public suburban GTFS)

Unified feed merges all three with MTC- / CMRL- / SRR- id prefixes.
"""
import csv
import os
import shutil
import zipfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
ARCHIVE = "/home/workspace/UngalSoththu/data/cumta-transit-data-2026-10-04/static/gtfs-unpacked"


def find_dir(root, marker):
    for r, d, files in os.walk(root):
        if marker in files:
            return r
    raise FileNotFoundError(marker)


def load(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return [r for r in rows if any((v or "").strip() for v in r.values())]


def save(path, rows, fieldnames):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def vendor(src_dir, dst_dir, extra_feed_info=None):
    os.makedirs(dst_dir, exist_ok=True)
    for f in os.listdir(dst_dir):
        os.remove(os.path.join(dst_dir, f))
    names = []
    for fn in sorted(os.listdir(src_dir)):
        if not fn.endswith(".txt"):
            continue
        rows = load(os.path.join(src_dir, fn))
        fieldnames = list(rows[0].keys()) if rows else None
        if fn == "feed_info.txt" and not rows and extra_feed_info:
            rows, fieldnames = [extra_feed_info], list(extra_feed_info.keys())
        if rows:
            save(os.path.join(dst_dir, fn), rows, fieldnames)
            names.append(fn)
    return names


def vendor_cmrl():
    src = find_dir(os.path.join(ARCHIVE, "cmrl"), "fare_rules.txt")
    info = {
        "feed_publisher_name": "Chennai Metro Rail Limited (via CUMTA Transit Data portal)",
        "feed_publisher_url": "https://chennaimetrorail.org/",
        "feed_lang": "en",
        "feed_version": "cumta-portal-20261004",
        "feed_contact_email": "chennaimetrorail@cmrl.in",
    }
    return vendor(src, os.path.join(DATA, "cmrl"), info)


def vendor_srr():
    src = find_dir(os.path.join(ARCHIVE, "southern_railways"), "pathways.txt")
    return vendor(src, os.path.join(DATA, "srr"))


def merge_unified():
    out = os.path.join(DATA, "unified")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    P = {"mtc": "MTC-", "cmrl": "CMRL-", "srr": "SRR-"}

    def pf(sysname, table, field):
        return lambda v: (P[sysname] + v) if v and v.strip() else v

    agencies, calendars, cal_dates = [], [], []
    routes, trips, stop_times, stops = [], [], [], []
    shapes, transfers, pathways = [], [], []
    fare_attrs, fare_rules = [], []

    srcs = {
        "mtc": os.path.join(DATA, "mtc"),
        "cmrl": os.path.join(DATA, "cmrl"),
        "srr": os.path.join(DATA, "srr"),
    }
    for sysname, sdir in srcs.items():
        pre = P[sysname]
        stopmap = {r["stop_id"]: pre + r["stop_id"] for r in load(os.path.join(sdir, "stops.txt"))}
        routemap = {r["route_id"]: pre + r["route_id"] for r in load(os.path.join(sdir, "routes.txt"))}
        servmap = {}

        ag = load(os.path.join(sdir, "agency.txt"))
        agencies += ag
        cal_p = os.path.join(sdir, "calendar.txt")
        if os.path.exists(cal_p):
            for r in load(cal_p):
                new = pre + r["service_id"]
                servmap[r["service_id"]] = new
                r["service_id"] = new
                calendars.append(r)
        cd_p = os.path.join(sdir, "calendar_dates.txt")
        if os.path.exists(cd_p):
            for r in load(cd_p):
                r["service_id"] = servmap.get(r["service_id"], pre + r["service_id"])
                cal_dates.append(r)
        rt = load(os.path.join(sdir, "routes.txt"))
        for r in rt:
            r["route_id"] = routemap[r["route_id"]]
        routes += rt
        tr = load(os.path.join(sdir, "trips.txt"))
        tripmap = {}
        for r in tr:
            old = r["trip_id"]
            new = pre + old
            tripmap[old] = new
            r["trip_id"] = new
            r["route_id"] = routemap[r["route_id"]]
            r["service_id"] = servmap.get(r["service_id"], pre + r["service_id"])
            if r.get("shape_id", "").strip():
                r["shape_id"] = pre + r["shape_id"]
        trips += tr
        st = load(os.path.join(sdir, "stop_times.txt"))
        for r in st:
            r["trip_id"] = tripmap[r["trip_id"]]
            r["stop_id"] = stopmap[r["stop_id"]]
        stop_times += st
        sp = load(os.path.join(sdir, "stops.txt"))
        for r in sp:
            r["stop_id"] = stopmap[r["stop_id"]]
            if r.get("parent_station", "").strip():
                r["parent_station"] = stopmap.get(r["parent_station"], r["parent_station"])
            if r.get("zone_id", "").strip():
                r["zone_id"] = pre + r["zone_id"]
        stops += sp
        sh_p = os.path.join(sdir, "shapes.txt")
        if os.path.exists(sh_p):
            rows = load(sh_p)
            for r in rows:
                r["shape_id"] = pre + r["shape_id"]
            shapes += rows
        tf_p = os.path.join(sdir, "transfers.txt")
        if os.path.exists(tf_p):
            rows = load(tf_p)
            for r in rows:
                r["from_stop_id"] = stopmap.get(r["from_stop_id"], r["from_stop_id"])
                r["to_stop_id"] = stopmap.get(r["to_stop_id"], r["to_stop_id"])
                if r.get("from_route_id", "").strip():
                    r["from_route_id"] = routemap.get(r["from_route_id"], r["from_route_id"])
                if r.get("to_route_id", "").strip():
                    r["to_route_id"] = routemap.get(r["to_route_id"], r["to_route_id"])
            transfers += rows
        pw_p = os.path.join(sdir, "pathways.txt")
        if os.path.exists(pw_p):
            kept, broken = [], 0
            for r in load(pw_p):
                if r["from_stop_id"] not in stopmap or r["to_stop_id"] not in stopmap:
                    broken += 1
                    continue
                r["pathway_id"] = pre + r["pathway_id"]
                r["from_stop_id"] = stopmap[r["from_stop_id"]]
                r["to_stop_id"] = stopmap[r["to_stop_id"]]
                kept.append(r)
            if broken:
                print(f"  {sysname}: dropped {broken} pathway rows referencing missing stops (source defect)")
            pathways += kept
        fa_p = os.path.join(sdir, "fare_attributes.txt")
        if os.path.exists(fa_p):
            fare_attrs += [dict(r, fare_id=pre + r["fare_id"]) for r in load(fa_p)]
        fr_p = os.path.join(sdir, "fare_rules.txt")
        if os.path.exists(fr_p):
            kept, bad = [], 0
            for r in load(fr_p):
                zones = [r.get(z, "").strip() for z in ("origin_id", "destination_id", "contains_id")]
                if any(zones) and any(z and (pre + z) not in {r["zone_id"] for r in sp if r.get("zone_id", "").strip()} for z in zones):
                    bad += 1
                    continue
                r["fare_id"] = pre + r["fare_id"]
                if r.get("route_id", "").strip():
                    r["route_id"] = routemap.get(r["route_id"], r["route_id"])
                for z in ("origin_id", "destination_id", "contains_id"):
                    if r.get(z, "").strip():
                        r[z] = pre + r[z]
                kept.append(r)
            if bad:
                print(f"  {sysname}: dropped {bad} fare_rules rows referencing zones absent from stops.txt (source defect)")
            fare_rules += kept

    # drop duplicate agency rows on agency_id, keep first
    seen, ag_uniq = set(), []
    for a in agencies:
        if a["agency_id"] not in seen:
            seen.add(a["agency_id"])
            ag_uniq.append(a)

    feed_info = {
        "feed_publisher_name": "Ithu Ungal Soththu",
        "feed_publisher_url": "https://github.com/ungalsoththu/ChennaiGTFS",
        "feed_lang": "en",
        "feed_start_date": "",
        "feed_end_date": "",
        "feed_version": "0.2.0",
        "feed_contact_email": "ithuungalsoththu.tn@gmail.com",
        "feed_contact_url": "https://github.com/ungalsoththu/ChennaiGTFS",
    }

    datasets = {
        "agency.txt": ag_uniq,
        "calendar.txt": calendars,
        "calendar_dates.txt": cal_dates,
        "routes.txt": routes,
        "trips.txt": trips,
        "stop_times.txt": stop_times,
        "stops.txt": stops,
        "shapes.txt": shapes,
        "transfers.txt": transfers,
        "pathways.txt": pathways,
        "fare_attributes.txt": fare_attrs,
        "fare_rules.txt": fare_rules,
        "feed_info.txt": [feed_info],
    }
    def union_headers(rows):
        hdr, seen = [], set()
        for r in rows:
            for k in r.keys():
                if k not in seen:
                    seen.add(k)
                    hdr.append(k)
        return hdr

    for fn, rows in datasets.items():
        if rows:
            save(os.path.join(out, fn), rows, union_headers(rows))

    validate(out)
    return {fn: len(rows) for fn, rows in datasets.items() if rows}


def validate(feed_dir):
    stops = {r["stop_id"] for r in load(os.path.join(feed_dir, "stops.txt"))}
    routes = {r["route_id"] for r in load(os.path.join(feed_dir, "routes.txt"))}
    trips = {r["trip_id"]: r for r in load(os.path.join(feed_dir, "trips.txt"))}
    services = {r["service_id"] for r in load(os.path.join(feed_dir, "calendar.txt"))}
    errors = []
    for r in trips.values():
        if r["route_id"] not in routes:
            errors.append(f"trip {r['trip_id']} -> missing route {r['route_id']}")
        if r["service_id"] not in services:
            errors.append(f"trip {r['trip_id']} -> missing service {r['service_id']}")
    for r in load(os.path.join(feed_dir, "stop_times.txt")):
        if r["trip_id"] not in trips:
            errors.append(f"stop_times -> missing trip {r['trip_id']}")
            break
        if r["stop_id"] not in stops:
            errors.append(f"stop_times -> missing stop {r['stop_id']}")
            break
    for r in load(os.path.join(feed_dir, "pathways.txt")):
        for f in ("from_stop_id", "to_stop_id"):
            if r[f] not in stops:
                errors.append(f"pathway {r['pathway_id']} -> missing stop {r[f]}")
    for r in load(os.path.join(feed_dir, "fare_rules.txt")):
        for f in ("origin_id", "destination_id"):
            if r.get(f, "").strip() and r[f] not in stops:
                # zone ids live on stops; check zone set instead
                pass
    zones = {r["zone_id"] for r in load(os.path.join(feed_dir, "stops.txt")) if r.get("zone_id", "").strip()}
    for r in load(os.path.join(feed_dir, "fare_rules.txt")):
        for f in ("origin_id", "destination_id"):
            if r.get(f, "").strip() and r[f] not in zones:
                errors.append(f"fare_rule {r['fare_id']} -> missing zone {r[f]}")
    if errors:
        raise SystemExit("VALIDATION FAILED:\n" + "\n".join(errors[:20]))
    print(f"validation OK: {len(stops)} stops, {len(routes)} routes, {len(trips)} trips, {len(services)} services")


def zipdir(src_dir, zip_path):
    if os.path.exists(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fn in sorted(os.listdir(src_dir)):
            if fn.endswith(".txt"):
                z.write(os.path.join(src_dir, fn), fn)


def main():
    print("vendor CMRL <-", vendor_cmrl())
    print("vendor SRR  <-", vendor_srr())
    counts = merge_unified()
    print("unified counts:", counts)
    for d, zp in [
        ("cmrl", "cmrl-gtfs.zip"),
        ("srr", "srr-gtfs.zip"),
        ("unified", "chennai-unified-gtfs.zip"),
    ]:
        zipdir(os.path.join(DATA, d), os.path.join(DATA, zp))
        print("zip:", zp, os.path.getsize(os.path.join(DATA, zp)), "bytes")
    # mirror unified loose files at data/ root (existing repo convention)
    for fn in os.listdir(os.path.join(DATA, "unified")):
        shutil.copyfile(os.path.join(DATA, "unified", fn), os.path.join(DATA, fn))
    print("loose unified files refreshed")


if __name__ == "__main__":
    main()
