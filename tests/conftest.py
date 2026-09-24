"""Shared pytest fixtures."""

import pytest

from brc_schema.util import taxonomy

# A small stand-in for NCBITaxon: curie -> (label, exact synonyms, broad synonyms).
FAKE_NCBITAXON = {
    "NCBITaxon:3689": ("Populus", ["poplar", "poplars"], []),
    "NCBITaxon:3694": ("Populus trichocarpa", ["black cottonwood"], []),
    "NCBITaxon:38727": ("Panicum virgatum", ["switchgrass"], []),
    "NCBITaxon:4557": ("Sorghum", [], []),
    "NCBITaxon:4558": ("Sorghum bicolor", ["sorghum"], []),
    "NCBITaxon:4577": ("Zea mays", ["maize"], []),
    "NCBITaxon:381124": ("Zea mays subsp. mays", ["maize", "corn"], []),
    "NCBITaxon:541": ("Zymomonas", [], []),
    "NCBITaxon:542": ("Zymomonas mobilis", [], []),
    # Tardigrades: absent from organisms.yaml, so only the lookup knows them.
    "NCBITaxon:286681": ("Ramazzottius", [], []),
    "NCBITaxon:947166": ("Ramazzottius varieornatus", [], []),
    "NCBITaxon:11676": ("Human immunodeficiency virus 1", [], ["HIV"]),
}


class FakeTaxonAdapter:
    """Answers like the OLS adapter: exact, case-insensitive, no synonym types."""

    def __init__(self):
        self.taxa = dict(FAKE_NCBITAXON)

    def basic_search(self, name, config=None):
        wanted = name.casefold()
        for curie, (label, exact, broad) in self.taxa.items():
            if any(wanted == value.casefold() for value in [label, *exact, *broad]):
                yield curie

    def label(self, curie):
        entry = self.taxa.get(curie)
        return entry[0] if entry else None


@pytest.fixture(autouse=True)
def offline_taxonomy(monkeypatch):
    """Keep every test off the network by routing lookups to a fake adapter."""
    adapter = FakeTaxonAdapter()
    monkeypatch.setattr(taxonomy, "_get_adapter", lambda: adapter)
    taxonomy.configure()
    yield adapter
    taxonomy.configure()
