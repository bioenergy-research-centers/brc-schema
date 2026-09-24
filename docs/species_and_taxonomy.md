# Species and Taxonomy Identifiers

The BRC schema records the organisms a dataset studies in the `species` slot.
Each entry is an `Organism` with a `scientificName`, an NCBI Taxonomy ID in
`NCBITaxID`, and, where available, other taxon identifiers in `taxon_ids`.

OSTI records have no field for species. When BRC records are built from OSTI
metadata with `brcschema transform -T osti_to_brc`, the transform looks for
organisms in two places in each OSTI record: its **related identifiers** and
its **keywords**. This page explains what to put in an OSTI record so that its
organisms come through with the right names and IDs.

## Quick guide for OSTI submitters

For each organism the dataset studies:

1. **Add a related identifier with the organism's NCBI Taxonomy URL.** This
   is the most reliable way. It gives an exact ID with no guessing.
2. **Add the organism's scientific name as a keyword.** This gives a
   readable name. When the name is ambiguous, the related identifier from
   step 1 settles it.

A record for a switchgrass dataset would include:

| OSTI field | Value |
| --- | --- |
| Related identifier: type | `URL` |
| Related identifier: relation | `References` |
| Related identifier: value | `https://www.ncbi.nlm.nih.gov/taxonomy/38727` |
| Keywords | `Panicum virgatum, lignin, field trial` |

The resulting BRC record gets:

```yaml
species:
  - scientificName: Panicum virgatum
    NCBITaxID: 38727
```

## Related identifiers

OSTI has no identifier type for taxonomy, so use type `URL` (or `URI` or
`OTHER`). The transform recognises the value itself, whatever type is given.
Any relation type is accepted; `References` is what `brc_to_osti` writes, so
use it for consistency.

### NCBI Taxonomy

Find the taxid by searching the organism at
<https://www.ncbi.nlm.nih.gov/taxonomy>. Any of these forms works:

| Form | Example |
| --- | --- |
| Short URL (preferred) | `https://www.ncbi.nlm.nih.gov/taxonomy/38727` |
| Taxonomy Browser URL | `https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=38727` |
| NCBI Datasets URL | `https://www.ncbi.nlm.nih.gov/datasets/taxonomy/38727/` |
| OBO PURL | `http://purl.obolibrary.org/obo/NCBITaxon_38727` |
| CURIE | `NCBITaxon:38727`, `NCBI:txid38727`, `txid38727`, or `taxid:38727` |

Add one related identifier per organism. Taxonomy URLs go only to `species`;
they are not copied into the BRC record's `has_related_ids`.

### JGI GOLD and IMG

JGI identifiers go to `taxon_ids`:

| Source | Accepted forms | Stored as |
| --- | --- | --- |
| GOLD | `https://gold.jgi.doe.gov/resolver?id=Gp0004954` (or `project?id=`, `organism?id=`, ...), `GOLD:Gp0004954`, `Gp0004954` | `GOLD:Gp0004954` |
| IMG | `https://img.jgi.doe.gov/...&taxon_oid=<oid>`, `IMG.TAXON:<oid>` | `IMG.TAXON:<oid>` |

GOLD organism IDs begin with `Go`; sequencing project IDs begin with `Gp`.
Both are accepted.

The record does not say which organism a GOLD or IMG ID belongs to. If the
record names exactly one organism, the IDs are attached to it. Otherwise each
becomes its own `species` entry with no name. To keep them together, give a
record with GOLD or IMG IDs only one organism, or add the NCBI URL as well.

## Keywords

OSTI keywords are usually one comma-separated string, such as
`13C NMR, lignin, poplar, field trial`. The transform splits it on commas and
checks each keyword against organism names.

A keyword counts as an organism only when **the whole keyword** is an organism
name. Matching ignores case and extra spaces, but nothing else: `corn` is an
organism, while `corn stover` is not.

| Keyword | Result | Why |
| --- | --- | --- |
| `Populus trichocarpa` or `Populus Trichocarpa` | *Populus trichocarpa*, 3694 | Exact name |
| `black cottonwood` | *Populus trichocarpa*, 3694 | Known common name |
| `poplar` | *Populus*, 3689 | Common name for the genus; genus IDs are fine |
| `Clostridium thermocellum` | *Acetivibrio thermocellus*, 1515 | Former name, mapped to NCBI's current one |
| `sorghum` | `sorghum`, no ID | Could be the genus (4557) or *S. bicolor* (4558) |
| `sorghum` plus the NCBI URL for 4558 | *Sorghum bicolor*, 4558 | The related identifier settles it |
| `Zymomonas mobilis 2032` | `Zymomonas mobilis 2032`, no ID | Starts with a known species, but the whole keyword is not a taxon name |
| `Sorghum genomics` | not an organism | A genus followed by an ordinary word |
| `HSQC`, `CBI` | not an organism | Keywords in all capitals are treated as acronyms and never looked up |

### Tips

- **Use the full scientific name**, spelled as in NCBI Taxonomy. Misspellings
  such as `Sorghum biocolor` are not matched.
- **Give each organism its own keyword**, separated by commas. Do not wrap
  names in extra text such as `switchgrass (Panicum virgatum L.)`.
- **Strains:** a keyword like `Zymomonas mobilis ZM4` is kept as a name with
  no ID. For a strain-level ID, add the strain's NCBI URL as a related
  identifier.
- **Common names** work only when they point to one taxon. When in doubt, use
  the scientific name or add the NCBI URL.
- Titles and descriptions are **not** searched for organism names. Only
  keywords and related identifiers are used.

## How names are resolved

Each keyword is checked in this order. The first match wins.

1. **Ambiguous names** in `src/brc_schema/transform/organisms.yaml`, such as
   `sorghum` and `sugarcane`. These give a name with no ID, unless the record
   carries one of the listed candidate taxids.
2. **Curated organisms** in the same file. These give the listed taxid.
3. **Organisms from the live BRC data feeds**, generated into the same file
   (see [Maintaining the vocabulary](#maintaining-the-vocabulary)). Their
   names and taxids have been checked against NCBI Taxonomy.
4. **A live NCBI Taxonomy lookup** through the EBI Ontology Lookup Service
   (OLS), using [oaklib](https://github.com/INCATools/ontology-access-kit).
   It looks for an exact label or synonym. One match gives that taxon's ID,
   at any rank. More than one match gives the name with no ID.
5. **A known species followed by more text** (such as a strain designation).
   This gives the name with no ID.

A keyword that passes none of these is an ordinary keyword and stays only in
`keywords`.

NCBI Taxonomy URLs in related identifiers become `NCBITaxID` directly. The
name comes from the vocabulary, or from a lookup when the taxid is not in it.

### Lookups and network access

Step 4 needs network access to OLS. It is on by default. OLS can be slow or
unreachable. Each lookup is tried three times, and results are cached for the
run. After three lookups in a row fail, lookups stop for the rest of the run.
The run still finishes, using the vocabulary alone, and a warning is logged.

```bash
# Default: vocabulary plus OLS lookups
uv run brcschema transform -T osti_to_brc -o out.yaml records.json

# Offline: vocabulary only
uv run brcschema transform -T osti_to_brc --no-taxon-lookup -o out.yaml records.json

# A different oaklib adapter
uv run brcschema transform -T osti_to_brc --taxon-adapter sqlite:/path/to/ncbitaxon.db -o out.yaml records.json
```

## BRC to OSTI

`brc_to_osti` writes each `species` identifier back to OSTI
`related_identifiers`, with type `URL` and relation `References`:

| BRC value | OSTI related identifier value |
| --- | --- |
| `NCBITaxID: 38727` | `https://www.ncbi.nlm.nih.gov/taxonomy/38727` |
| `GOLD:Gp0004954` | `https://gold.jgi.doe.gov/resolver?id=Gp0004954` |
| `IMG.TAXON:<oid>` | `https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=TaxonDetail&page=taxonDetail&taxon_oid=<oid>` |

These URLs are read back as the same species by `osti_to_brc`. A species with
a name but no identifier is **not** written to OSTI. OSTI has nowhere to put
it except keywords, and the transform does not edit keywords.

## Maintaining the vocabulary

`src/brc_schema/transform/organisms.yaml` has two parts:

- A **curated** part, edited by hand: `ambiguous_names` (each name with its
  candidate taxids) and `organisms` (scientific name, NCBI taxid, synonyms).
  Curated entries always win.
- A **generated** `feed_organisms` block with every organism already used in
  the live BRC data feeds. Do not edit it by hand.

To refresh the generated block:

```bash
uv run python scripts/update_organisms_from_feeds.py --report organisms_report.md
```

The script reads the feeds that bioenergy.org imports and checks every taxid
against NCBI Taxonomy. Each entry is named by NCBI. A feed's own spelling is
kept as a synonym only when it agrees with NCBI, and no name may point to two
taxa. The report lists everything that was left out, such as feed names that
do not match their taxid, merged taxids, and unknown taxids. Report errors in
a feed to the BRC that publishes it. Set `NCBI_API_KEY` to raise the NCBI rate
limit.

To fix a name for good, add it to the curated part and rerun the script.

## Related Pages

- [OSTI to/from xBRC Conversion](osti_xbrc_conversion.md)
- [CLI Usage](cli.md)
- [Schema reference: Organism](Organism.md)
