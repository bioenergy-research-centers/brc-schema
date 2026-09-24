"""Tests for the feed vocabulary generator script."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "update_organisms_from_feeds.py"
_spec = importlib.util.spec_from_file_location("update_organisms_from_feeds", SCRIPT)
update = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(update)


def _record(name, *names, rank="species"):
    return {"taxid": 1, "name": name, "rank": rank, "names": {name, *names}}


@pytest.mark.parametrize(
    "feed_name, record",
    [
        ("Zea mays", _record("Zea mays")),
        ("maize", _record("Zea mays", "maize")),
        ("maize (Zea mays)", _record("Zea mays")),
        ("Pseudomonas putida KT2440", _record("Pseudomonas putida")),
        ("[Candida] boidinii strain X", _record("[Candida] boidinii")),
        ("Bacillus sp.", _record("Bacillus", rank="genus")),
        ("Saccharum spp. hybrid", _record("Saccharum", rank="genus")),
        ("Lamiaceae family", _record("Lamiaceae", rank="family")),
    ],
)
def test_agrees_accepts_names_for_the_taxon(feed_name, record):
    assert update.agrees(feed_name, record)


@pytest.mark.parametrize(
    "feed_name, record",
    [
        ("Panicum virgatum", _record("Pan", rank="genus")),
        ("Zea mays", _record("Zea", rank="genus")),
        ("maize (Zea mays)", _record("Zea", rank="genus")),
        ("Sorghum biocolor BTx623", _record("Sorghum bicolor")),
        ("switchgrass (Panicum virgatum L.)", _record("Propioniferax innocua")),
    ],
)
def test_agrees_rejects_partial_words_and_other_taxa(feed_name, record):
    assert not update.agrees(feed_name, record)
