#!/usr/bin/env python3
"""Validate data/tools/*.yaml and build the static site into public/.

Usage:
    python scripts/build_site.py            # validate + build public/
    python scripts/build_site.py --check    # validate only (CI on merge requests)
    python scripts/build_site.py --artifact FILE  # also emit a body-only preview page
"""
import argparse
import csv
import datetime
import json
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "data" / "tools"
TEMPLATE = ROOT / "site" / "template.html"
STATIC = ROOT / "site" / "static"
PUBLIC = ROOT / "public"

CLASSES = {
    "Simulator", "Emulator", "Testbed", "In-orbit platform", "Dataset / data",
    "Measurement", "Implementation", "Library", "Visualizer", "Research platform",
    "Meta-resource", "Commercial / service", "Unresolved", "Other",
}
DOMAINS = {
    "LEO", "Deep space / DTN", "IoT", "NTN-5G", "GEO / DVB", "Optical",
    "Orbital compute", "Ground segment", "Orbits / astro", "Security",
    "Transport", "Other",
}
MAINTENANCE = {"active", "low", "inactive", "planned", "unknown"}
REAL_STACK = {"yes", "no", "partial", "na"}
SOURCES = {"dagstuhl", "sweep", "community"}
REQUIRED = ["name", "class", "subtype", "domains", "url"]

# yaml key -> key expected by the site's JavaScript
JS_KEYS = {
    "name": "name", "class": "cls", "class_detail": "clsRaw", "subtype": "sub",
    "domains": "dom", "domain_detail": "domRaw", "dynamics": "dyn",
    "layers": "layers", "real_stack": "real", "real_stack_detail": "realRaw",
    "scale": "scale", "inputs": "inp", "outputs": "out", "language": "lang",
    "license": "lic", "maintenance": "maint", "maintenance_detail": "maintRaw",
    "last_activity": "last", "url": "url", "publication": "pub",
    "contact": "contact", "notes": "notes", "source": "src",
    "added": "added", "verified": "verified",
}
CSV_COLUMNS = [k for k in JS_KEYS if k != "domains"]


def load_tools():
    errors, tools = [], []
    files = sorted(TOOLS_DIR.glob("*.yaml"))
    if not files:
        errors.append(f"no YAML files found in {TOOLS_DIR}")
    names = {}
    for f in files:
        try:
            rec = yaml.safe_load(f.read_text())
        except yaml.YAMLError as e:
            errors.append(f"{f.name}: YAML parse error: {e}")
            continue
        if not isinstance(rec, dict):
            errors.append(f"{f.name}: expected a mapping")
            continue
        for k in REQUIRED:
            if not rec.get(k):
                errors.append(f"{f.name}: missing required field '{k}'")
        if rec.get("class") and rec["class"] not in CLASSES:
            errors.append(f"{f.name}: unknown class '{rec['class']}'")
        doms = rec.get("domains") or []
        if not isinstance(doms, list):
            errors.append(f"{f.name}: 'domains' must be a list")
        else:
            for d in doms:
                if d not in DOMAINS:
                    errors.append(f"{f.name}: unknown domain '{d}'")
        for field, allowed in [("maintenance", MAINTENANCE),
                               ("real_stack", REAL_STACK), ("source", SOURCES)]:
            v = rec.get(field)
            if v is not None and str(v) not in allowed:
                errors.append(f"{f.name}: '{field}' must be one of {sorted(allowed)}, got '{v}'")
        n = rec.get("name")
        if n in names:
            errors.append(f"{f.name}: duplicate tool name '{n}' (also in {names[n]})")
        names[n] = f.name
        unknown = set(rec) - set(JS_KEYS) - {"added"}
        if unknown:
            errors.append(f"{f.name}: unknown fields {sorted(unknown)}")
        tools.append(rec)
    return tools, errors


def to_js(rec):
    out = {}
    for yk, jk in JS_KEYS.items():
        v = rec.get(yk)
        if v is None:
            continue
        out[jk] = v if yk == "domains" else str(v)
    out.setdefault("clsRaw", out.get("cls", ""))
    out.setdefault("domRaw", "; ".join(out.get("dom", [])))
    out.setdefault("real", "na")
    out.setdefault("maint", "unknown")
    out.setdefault("last", "")
    out.setdefault("src", "community")
    for k in ("contact", "pub", "notes", "sub", "lang", "lic"):
        out.setdefault(k, "")
    return out


def fill_placeholders(text, cfg, n_tools):
    return (text
            .replace("__MAINTAINER_EMAIL__", cfg["maintainer_email"])
            .replace("__REPO_URL__", cfg["repo_url"])
            .replace("__BUILD_DATE__", datetime.date.today().isoformat()))


def head_html(cfg, n_tools):
    title = cfg["site_title"]
    desc = cfg.get("description", "").replace("{n}", str(n_tools))
    pages = cfg.get("pages_url", "").rstrip("/") + "/"
    og_img = pages + "static/og.png"
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{pages}">
<link rel="icon" type="image/svg+xml" href="static/favicon.svg">
<meta name="theme-color" content="#F6F7F9" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F131B" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{title}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{pages}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_img}">
"""


def build(tools, cfg, artifact_out=None):
    rows = [to_js(r) for r in sorted(tools, key=lambda r: r["name"].lower())]
    data_js = json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")
    body = fill_placeholders(TEMPLATE.read_text(), cfg, len(rows))
    body = body.replace("const DATA = /*__DATA__*/[];", f"const DATA = {data_js};")

    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / "data").mkdir(exist_ok=True)
    if STATIC.is_dir():
        shutil.copytree(STATIC, PUBLIC / "static", dirs_exist_ok=True)
    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n"
            + head_html(cfg, len(rows))
            + "</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    (PUBLIC / "index.html").write_text(page)

    (PUBLIC / "data" / "tools.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=1))
    with (PUBLIC / "data" / "tools.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(CSV_COLUMNS + ["domains"])
        for r in sorted(tools, key=lambda r: r["name"].lower()):
            w.writerow([r.get(c, "") for c in CSV_COLUMNS] +
                       ["; ".join(r.get("domains") or [])])

    if artifact_out:
        Path(artifact_out).write_text(
            f"<title>{cfg['site_title']}</title>\n" + body)
    print(f"built public/ with {len(rows)} tools")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("--artifact", help="also write a body-only preview page to this path")
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    tools, errors = load_tools()
    if errors:
        print(f"{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(1)
    print(f"{len(tools)} tool records validated")
    if not args.check:
        build(tools, cfg, artifact_out=args.artifact)


if __name__ == "__main__":
    main()
