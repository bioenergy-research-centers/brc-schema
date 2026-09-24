"""Tests for mapping OSTI keywords and related identifiers to BRC species."""

import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin
from linkml.validator.report import Severity

from brc_schema.cli import main
from brc_schema.transform import (
    _load_organism_index,
    _parse_taxon_identifier,
    build_brc_has_related_ids,
    build_brc_species,
    build_osti_related_identifiers,
)
from brc_schema.util import taxonomy

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "src" / "brc_schema" / "schema" / "brc_schema.yaml"


def _url(value, type_="URL"):
    return {"type": type_, "relation": "IsDocumentedBy", "value": value}


@pytest.mark.parametrize(
    "value, expected",
    [
        ("https://www.ncbi.nlm.nih.gov/taxonomy/38727", ("ncbi", 38727)),
        (
            "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?command=show&mode=node&id=38727&lvl=",
            ("ncbi", 38727),
        ),
        ("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=38727", ("ncbi", 38727)),
        ("https://www.ncbi.nlm.nih.gov/datasets/taxonomy/38727/", ("ncbi", 38727)),
        ("http://purl.obolibrary.org/obo/NCBITaxon_38727", ("ncbi", 38727)),
        ("NCBITaxon:38727", ("ncbi", 38727)),
        ("NCBI:txid38727", ("ncbi", 38727)),
        ("https://gold.jgi.doe.gov/project?id=Gp0004954", ("other", "GOLD:Gp0004954")),
        ("https://gold.jgi.doe.gov/resolver?id=Gp0004954", ("other", "GOLD:Gp0004954")),
        ("GOLD:Gp0004954", ("other", "GOLD:Gp0004954")),
        ("Gp0004954", ("other", "GOLD:Gp0004954")),
        (
            "https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=1234567890",
            ("other", "IMG.TAXON:1234567890"),
        ),
        ("IMG.TAXON:1234567890", ("other", "IMG.TAXON:1234567890")),
        ("10.11578/1234567", None),
        ("https://www.ncbi.nlm.nih.gov/bioproject/?term=PRJNA123", None),
        ("https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?name=Populus", None),
        (None, None),
    ],
)
def test_parse_taxon_identifier(value, expected):
    assert _parse_taxon_identifier(value) == expected


def test_organism_vocabulary_has_no_conflicting_names():
    by_name, by_taxid, ambiguous = _load_organism_index()
    assert by_name
    assert all(record["NCBITaxID"] in by_taxid for record in by_name.values())
    assert not ambiguous & set(by_name)


def test_species_from_ncbi_url_is_named_from_vocabulary():
    species = build_brc_species(
        None, None, [_url("https://www.ncbi.nlm.nih.gov/taxonomy/38727")]
    )
    assert species == [{"scientificName": "Panicum virgatum", "NCBITaxID": 38727}]


def test_species_from_ncbi_url_is_named_from_lookup():
    species = build_brc_species(
        None, None, [_url("https://www.ncbi.nlm.nih.gov/taxonomy/947166")]
    )
    assert species == [{"scientificName": "Ramazzottius varieornatus", "NCBITaxID": 947166}]


def test_unknown_ncbi_taxid_is_kept_without_a_name():
    species = build_brc_species(
        None, None, [_url("https://www.ncbi.nlm.nih.gov/taxonomy/999999")]
    )
    assert species == [{"NCBITaxID": 999999}]


def test_genus_common_name_maps_to_genus():
    species = build_brc_species(["Lignin structure, HSQC, poplar, CELF, CBP, CBI"], None, None)
    assert species == [{"scientificName": "Populus", "NCBITaxID": 3689}]


def test_keywords_match_only_whole_names():
    species = build_brc_species(
        ["Populus Trichocarpa, corn stover, Gene expression, E. coli"], None, None
    )
    assert species == [
        {"scientificName": "Populus trichocarpa", "NCBITaxID": 3694},
        {"scientificName": "Escherichia coli", "NCBITaxID": 562},
    ]


def _assert_not_in_vocabulary(name):
    by_name, _, ambiguous = _load_organism_index()
    key = " ".join(name.split()).casefold()
    assert key not in by_name and key not in ambiguous, f"{name} is in organisms.yaml"


def test_name_outside_vocabulary_gets_id_from_lookup():
    _assert_not_in_vocabulary("Ramazzottius varieornatus")
    species = build_brc_species(["Ramazzottius varieornatus"], None, None)
    assert species == [{"scientificName": "Ramazzottius varieornatus", "NCBITaxID": 947166}]


def test_ambiguous_lookup_keeps_name_without_id(offline_taxonomy):
    # Only the lookup sees this name, and it matches two taxa.
    _assert_not_in_vocabulary("Ramazzottius varieornatus")
    offline_taxonomy.taxa["NCBITaxon:9999"] = ("Ramazzottius varieornatus", [], [])
    species = build_brc_species(["Ramazzottius varieornatus"], None, None)
    assert species == [{"scientificName": "Ramazzottius varieornatus"}]


def test_vocabulary_ambiguous_name_skips_lookup():
    assert build_brc_species(["sugarcane"], None, None) == [{"scientificName": "sugarcane"}]


def test_ambiguous_name_is_settled_by_identifier_in_metadata():
    species = build_brc_species(
        ["sorghum"], None, [_url("https://www.ncbi.nlm.nih.gov/taxonomy/4558")]
    )
    assert species == [{"NCBITaxID": 4558, "scientificName": "Sorghum bicolor"}]


def test_unmatched_name_starting_with_known_species_keeps_name():
    species = build_brc_species(["Zymomonas mobilis 2032"], None, None)
    assert species == [{"scientificName": "Zymomonas mobilis 2032"}]


def test_prefix_resolved_by_lookup_keeps_name():
    _assert_not_in_vocabulary("Ramazzottius varieornatus")
    species = build_brc_species(["Ramazzottius varieornatus YOKOZUNA-1"], None, None)
    assert species == [{"scientificName": "Ramazzottius varieornatus YOKOZUNA-1"}]


def test_prefix_candidate_is_settled_by_identifier_in_metadata():
    species = build_brc_species(
        ["Zymomonas mobilis 2032"], None, [_url("https://www.ncbi.nlm.nih.gov/taxonomy/542")]
    )
    assert species == [{"scientificName": "Zymomonas mobilis", "NCBITaxID": 542}]


@pytest.mark.parametrize(
    "keyword",
    ["Sorghum genomics", "Populus Transcriptome", "Zymomonas fermentation", "Carbon cycling"],
)
def test_genus_followed_by_ordinary_word_is_not_an_organism(keyword):
    assert build_brc_species([keyword], None, None) is None


def test_acronyms_are_not_looked_up():
    assert build_brc_species(["HIV"], None, None) is None


def test_lookup_disabled_uses_vocabulary_only():
    taxonomy.configure(enabled=False)
    species = build_brc_species(
        ["poplar, Ramazzottius varieornatus, Ramazzottius varieornatus YOKOZUNA-1"],
        None,
        None,
    )
    assert species == [{"scientificName": "Populus", "NCBITaxID": 3689}]


def test_lookup_failure_is_not_fatal(monkeypatch, caplog):
    class BrokenAdapter:
        def basic_search(self, name, config=None):
            raise ConnectionError("OLS unreachable")

        def label(self, curie):
            raise ConnectionError("OLS unreachable")

    monkeypatch.setattr(taxonomy, "_get_adapter", lambda: BrokenAdapter())
    taxonomy.configure()
    species = build_brc_species(
        ["poplar, Ramazzottius varieornatus"],
        None,
        [_url("https://www.ncbi.nlm.nih.gov/taxonomy/947166")],
    )
    assert species == [
        {"NCBITaxID": 947166},
        {"scientificName": "Populus", "NCBITaxID": 3689},
    ]
    assert "Taxonomy lookup failed" in caplog.text


def test_keyword_and_identifier_for_same_taxon_merge():
    species = build_brc_species(
        ["switchgrass"],
        None,
        [_url("https://www.ncbi.nlm.nih.gov/taxonomy/38727")],
    )
    assert species == [{"scientificName": "Panicum virgatum", "NCBITaxID": 38727}]


def test_former_scientific_name_maps_to_current_name():
    species = build_brc_species(["Clostridium thermocellum"], None, None)
    assert species == [{"scientificName": "Acetivibrio thermocellus", "NCBITaxID": 1515}]


def test_non_ncbi_ids_attach_to_single_organism():
    species = build_brc_species(
        None,
        None,
        [
            _url("https://www.ncbi.nlm.nih.gov/taxonomy/38727"),
            _url("Gp0004954", type_="OTHER"),
        ],
    )
    assert species == [
        {"scientificName": "Panicum virgatum", "NCBITaxID": 38727, "taxon_ids": ["GOLD:Gp0004954"]}
    ]


def test_non_ncbi_ids_stay_separate_when_organism_is_ambiguous():
    species = build_brc_species(
        ["switchgrass, Zymomonas mobilis"],
        None,
        [_url("GOLD:Gp0004954", type_="OTHER")],
    )
    assert species == [
        {"scientificName": "Panicum virgatum", "NCBITaxID": 38727},
        {"scientificName": "Zymomonas mobilis", "NCBITaxID": 542},
        {"taxon_ids": ["GOLD:Gp0004954"]},
    ]


def test_taxon_identifiers_are_not_copied_to_has_related_ids():
    related = build_brc_has_related_ids(
        None,
        [
            _url("https://www.ncbi.nlm.nih.gov/taxonomy/38727"),
            _url("https://gold.jgi.doe.gov/project?id=Gp0004954"),
            {"type": "DOI", "relation": "References", "value": "10.1234/abc"},
        ],
        None,
        None,
        None,
        None,
    )
    assert related == ["doi:10.1234/abc"]


def test_species_written_to_osti_related_identifiers():
    related = build_osti_related_identifiers(
        ["doi:10.1234/abc"],
        [
            {"scientificName": "Panicum virgatum", "NCBITaxID": 38727, "taxon_ids": ["GOLD:Gp0004954"]},
            {"scientificName": "Sorghum"},
            {"NCBITaxID": 38727},
            {"taxon_ids": ["IMG.TAXON:1234567890"]},
        ],
    )
    assert related == [
        {"type": "DOI", "relation": "References", "value": "10.1234/abc"},
        {"type": "URL", "relation": "References", "value": "https://www.ncbi.nlm.nih.gov/taxonomy/38727"},
        {"type": "URL", "relation": "References", "value": "https://gold.jgi.doe.gov/resolver?id=Gp0004954"},
        {
            "type": "URL",
            "relation": "References",
            "value": "https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=1234567890",
        },
    ]


def test_species_identifiers_round_trip():
    species = [
        {"scientificName": "Panicum virgatum", "NCBITaxID": 38727, "taxon_ids": ["GOLD:Gp0004954", "IMG.TAXON:1234567890"]}
    ]
    related = build_osti_related_identifiers(None, species)
    assert build_brc_species(None, None, related) == species


def test_osti_to_brc_transform_emits_valid_species(tmp_path):
    record = {
        "osti_id": "12345",
        "title": "Test Dataset",
        "description": "A test dataset",
        "keywords": ["switchgrass, lignin"],
        "publication_date": "2024-01-01",
        "site_ownership_code": "GLBRC",
        "persons": [{"type": "AUTHOR", "first_name": "Ada", "last_name": "Test"}],
        "related_identifiers": [
            _url("https://www.ncbi.nlm.nih.gov/taxonomy/542"),
            _url("https://gold.jgi.doe.gov/project?id=Gp0004954"),
        ],
    }
    input_file = tmp_path / "input.json"
    input_file.write_text(json.dumps({"records": [record]}), encoding="utf-8")
    output_file = tmp_path / "output.yaml"

    result = CliRunner().invoke(
        main, ["transform", "-T", "osti_to_brc", "-o", str(output_file), str(input_file)]
    )
    assert result.exit_code == 0, result.output

    data = yaml.safe_load(output_file.read_text(encoding="utf-8"))
    assert data["datasets"][0]["species"] == [
        {"scientificName": "Zymomonas mobilis", "NCBITaxID": 542},
        {"scientificName": "Panicum virgatum", "NCBITaxID": 38727},
        {"taxon_ids": ["GOLD:Gp0004954"]},
    ]

    validator = Validator(
        schema=str(SCHEMA_PATH),
        validation_plugins=[JsonschemaValidationPlugin(closed=True)],
    )
    report = validator.validate(data, target_class="DatasetCollection")
    errors = [
        r.message for r in report.results if r.severity in (Severity.ERROR, Severity.FATAL)
    ]
    assert errors == []
