"""Regenerate the feed_organisms block of organisms.yaml from live BRC feeds.

Collects every Organism (scientificName + NCBITaxID) in the BRC data feeds,
checks each taxid against NCBI Taxonomy (E-utilities), and writes one entry
per current taxid, named by NCBI. A feed spelling is kept as a synonym only
when it agrees with NCBI: it is an NCBI name for that taxon, or it contains
the NCBI scientific name (e.g. "maize (Zea mays)"). No name may map to two
taxa; curated entries and ambiguous_names in the hand-edited part of the
file take precedence. Everything left out is listed in a report.

Usage:
    uv run python scripts/update_organisms_from_feeds.py [--report PATH] [FEED_URL ...]

Set NCBI_API_KEY to raise the NCBI rate limit.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ORGANISMS_PATH = ROOT / "src" / "brc_schema" / "transform" / "organisms.yaml"
MARKER = "# --- BEGIN GENERATED: feed_organisms ---"

# Feeds imported by bioenergy.org (api/app/config/datafeeds.json).
DEFAULT_FEEDS = [
    "https://bioenergy.org/JBEI/jbei.json",
    "https://cabbitools.igb.illinois.edu/brc/cabbi.json",
    "https://bioenergy-research-centers.github.io/brc_data_feeds/cbi.json",
    "https://fair-data.glbrc.org/glbrc.json",
]
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 200
JUNK_NAMES = {"", "none", "na", "n/a", "null", "unknown"}


def norm(name):
    return " ".join(str(name).replace("×", "x").split()).casefold()


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "brc-schema"})
    with urllib.request.urlopen(request, timeout=300) as response:
        return json.load(response)


def collect_feed_organisms(feed_urls):
    """Return {(name, taxid): set(feed labels)} for every Organism in the feeds."""
    found = defaultdict(set)

    def walk(obj, feed):
        if isinstance(obj, dict):
            taxid = obj.get("NCBITaxID")
            if isinstance(taxid, int):
                found[(obj.get("scientificName"), taxid)].add(feed)
            for value in obj.values():
                walk(value, feed)
        elif isinstance(obj, list):
            for value in obj:
                walk(value, feed)

    for url in feed_urls:
        feed = Path(urllib.parse.urlparse(url).path).stem
        data = fetch_json(url)
        datasets = data.get("datasets", data) if isinstance(data, dict) else data
        walk(datasets, feed)
        print(f"{feed}: {len(datasets)} datasets", file=sys.stderr)
    return found


def fetch_ncbi(taxids):
    """Return {requested taxid: record} from NCBI efetch.

    A record has taxid (current), name, rank, and names (all NCBI names).
    Merged taxids map to the record of the taxon they were merged into.
    """
    api_key = os.environ.get("NCBI_API_KEY")
    records = {}
    taxids = sorted(taxids)
    for start in range(0, len(taxids), BATCH):
        batch = taxids[start:start + BATCH]
        params = {"db": "taxonomy", "id": ",".join(map(str, batch))}
        if api_key:
            params["api_key"] = api_key
        body = urllib.parse.urlencode(params).encode()
        with urllib.request.urlopen(EFETCH, data=body, timeout=300) as response:
            root = ET.parse(response).getroot()
        for taxon in root.findall("Taxon"):
            record = {
                "taxid": int(taxon.findtext("TaxId")),
                "name": taxon.findtext("ScientificName"),
                "rank": taxon.findtext("Rank"),
                "names": {taxon.findtext("ScientificName")},
            }
            other = taxon.find("OtherNames")
            if other is not None:
                for child in other:
                    if child.tag in {"Synonym", "GenbankCommonName", "CommonName",
                                     "EquivalentName", "GenbankSynonym"} and child.text:
                        record["names"].add(child.text)
            records[record["taxid"]] = record
            aka = taxon.find("AkaTaxIds")
            if aka is not None:
                for old in aka.findall("TaxId"):
                    records[int(old.text)] = record
        time.sleep(0.12 if api_key else 0.4)
    return records


def load_curated():
    """Return (curated names -> taxid, curated taxids, ambiguous names, head text).

    Feed entries for curated taxids are still written, so that feed spellings
    become synonyms; the transform keeps the curated scientific name.
    """
    text = ORGANISMS_PATH.read_text(encoding="utf-8")
    head = text.split(MARKER)[0].rstrip() + "\n"
    data = yaml.safe_load(head) or {}
    names = {}
    for entry in data.get("organisms") or []:
        for name in [entry["scientific_name"], *(entry.get("synonyms") or [])]:
            names[norm(name)] = int(entry["ncbi_taxid"])
    ambiguous = {norm(name) for name in data.get("ambiguous_names") or []}
    return names, set(names.values()), ambiguous, head


def agrees(feed_name, record):
    key = norm(feed_name)
    if key in {norm(name) for name in record["names"]}:
        return True
    return norm(record["name"]) in key


def build(found, ncbi, curated_names, curated_taxids, ambiguous):
    entries = {}
    report = defaultdict(list)
    for (feed_name, taxid), feeds in sorted(found.items(), key=lambda item: item[0][1]):
        record = ncbi.get(taxid)
        where = ",".join(sorted(feeds))
        if record is None:
            report["taxid not found in NCBI"].append(f"{taxid} {feed_name!r} [{where}]")
            continue
        if record["taxid"] != taxid:
            report["merged taxid (entry uses current id)"].append(
                f"{taxid} -> {record['taxid']} {record['name']!r} [{where}]")
        current = record["taxid"]
        entry = entries.setdefault(current, {
            "scientific_name": record["name"],
            "ncbi_taxid": current,
            "rank": record["rank"],
            "synonyms": set(),
            "feeds": set(),
        })
        entry["feeds"].update(feeds)
        if feed_name is None or norm(feed_name) in JUNK_NAMES:
            continue
        if norm(feed_name) == norm(record["name"]):
            continue
        if agrees(feed_name, record):
            entry["synonyms"].add(" ".join(feed_name.split()))
        else:
            report["feed name disagrees with NCBI name (not kept)"].append(
                f"{taxid} feed {feed_name!r} vs NCBI {record['name']!r} [{where}]")

    # Every name must map to one taxon, and curated names win.
    by_name = defaultdict(set)
    for taxid, entry in entries.items():
        by_name[norm(entry["scientific_name"])].add(taxid)
    for taxid, entry in list(entries.items()):
        key = norm(entry["scientific_name"])
        if curated_names.get(key, taxid) != taxid or key in ambiguous:
            report["NCBI name already curated or ambiguous (entry dropped)"].append(
                f"{taxid} {entry['scientific_name']!r}")
            del entries[taxid]
        elif len(by_name[key]) > 1:
            report["NCBI name shared by several taxids (entry dropped)"].append(
                f"{taxid} {entry['scientific_name']!r}")
            del entries[taxid]

    claims = defaultdict(set)
    for taxid, entry in entries.items():
        for synonym in entry["synonyms"]:
            claims[norm(synonym)].add(taxid)
    names = {norm(entry["scientific_name"]) for entry in entries.values()} | set(curated_names)
    for taxid, entry in entries.items():
        keep = set()
        for synonym in entry["synonyms"]:
            key = norm(synonym)
            if curated_names.get(key) == taxid:
                continue
            if key in curated_names or key in ambiguous:
                reason = "synonym curated for another taxid or ambiguous (not kept)"
            elif key in names:
                reason = "synonym is another entry's name (not kept)"
            elif len(claims[key]) > 1:
                reason = "synonym claimed by several taxids (not kept)"
            else:
                keep.add(synonym)
                continue
            report[reason].append(f"{taxid} {synonym!r}")
        entry["synonyms"] = keep
    return entries, report


def render(entries, feed_urls):
    items = []
    for taxid in sorted(entries, key=lambda t: entries[t]["scientific_name"].casefold()):
        entry = entries[taxid]
        item = {
            "scientific_name": entry["scientific_name"],
            "ncbi_taxid": taxid,
            "rank": entry["rank"],
        }
        if entry["synonyms"]:
            item["synonyms"] = sorted(entry["synonyms"], key=str.casefold)
        item["feeds"] = sorted(entry["feeds"])
        items.append(item)
    lines = [
        MARKER,
        "# Generated by scripts/update_organisms_from_feeds.py. Do not edit by hand;",
        "# add corrections to `organisms` or `ambiguous_names` above and rerun.",
        f"# Source feeds: {', '.join(feed_urls)}",
        f"# Generated {time.strftime('%Y-%m-%d')} with names and taxids checked against NCBI Taxonomy.",
        "",
    ]
    body = yaml.safe_dump({"feed_organisms": items}, sort_keys=False, allow_unicode=True, width=100)
    return "\n".join(lines) + body


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("feeds", nargs="*", default=DEFAULT_FEEDS)
    parser.add_argument("--report", type=Path, help="write the review report here")
    args = parser.parse_args()

    found = collect_feed_organisms(args.feeds)
    ncbi = fetch_ncbi({taxid for _, taxid in found})
    curated_names, curated_taxids, ambiguous, head = load_curated()
    entries, report = build(found, ncbi, curated_names, curated_taxids, ambiguous)

    ORGANISMS_PATH.write_text(head + "\n" + render(entries, args.feeds), encoding="utf-8")
    print(f"Wrote {len(entries)} feed organisms to {ORGANISMS_PATH.relative_to(ROOT)}", file=sys.stderr)

    lines = []
    for section, items in sorted(report.items()):
        lines.append(f"## {section} ({len(items)})")
        lines.extend(f"- {item}" for item in items)
        lines.append("")
    text = "\n".join(lines)
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
