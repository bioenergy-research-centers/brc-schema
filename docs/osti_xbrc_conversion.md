# OSTI to/from xBRC Conversion

This page describes how this project converts metadata between OSTI E-Link
records and the xBRC schema used for BRC data on bioenergy.org.

In this repository, **xBRC** refers to the cross-BRC metadata model represented
by `brc_schema.yaml`. It captures the fields needed by the Bioenergy Research
Centers and the bioenergy.org data portal, including BRC affiliation, dataset
landing pages, BRC-specific topics and themes, organism metadata, repository
metadata, and portal-oriented status fields.

The conversion logic lives in:

- `src/brc_schema/transform/osti_to_brc.yaml`
- `src/brc_schema/transform/brc_to_osti.yaml`
- `src/brc_schema/transform.py`

## When to Use Each Direction

Use `osti_to_brc` when records have been retrieved from OSTI E-Link and need to
be loaded, validated, or reviewed as xBRC `DatasetCollection` data:

```bash
uv run brcschema transform -T osti_to_brc -o brc_datasets.yaml osti_records.json
```

Use `brc_to_osti` when xBRC metadata needs to be prepared for OSTI E-Link
submission or update workflows:

```bash
uv run brcschema transform -T brc_to_osti -o osti_records.yaml brc_datasets.yaml
```

Input files may be JSON or YAML. Output format is selected from the output file
extension.

## OSTI to xBRC

The `osti_to_brc` transform expects an OSTI-style wrapper object with a
`records` array and produces an xBRC `DatasetCollection` with `datasets`.

Key mappings include:

| OSTI source | xBRC target | Notes |
| --- | --- | --- |
| `records` | `datasets` | Each OSTI `Record` becomes one xBRC `Dataset`. |
| `title` | `title` | Direct mapping. |
| `description` | `description`, `abstract` | OSTI description is copied into both xBRC fields. |
| `publication_date` or `entry_date` | `date` | Publication date is preferred. |
| `osti_id` | `identifier` | Rendered as `https://www.osti.gov/biblio/<osti_id>`. |
| `doi` | `bibliographicCitation` | Rendered as `https://doi.org/<doi>`. |
| `keywords` or `subjects` | `keywords` | Comma-separated strings are split into individual keywords. |
| `persons`, `authors`, `organizations` | `creator`, `contributors` | Structured `persons` are preferred; legacy author strings are fallback input. |
| sponsor `organizations` or `sponsor_orgs` | `funding` | Award identifiers are copied when available. |
| `related_identifiers` | `relatedItem` | OSTI related identifiers become xBRC related items. |
| `identifiers`, `related_identifiers`, and legacy identifier fields | `has_related_ids` | Contract numbers are excluded; BioProject URLs and IDs are normalized where possible. |
| `media` | `media` | OSTI media package metadata is preserved. |
| `site_url` or first `links` entry | `dataset_url` | `site_url` is preferred. |
| `workflow_status` | `active` | `R` maps to `true`; missing status maps to `false`. |

### xBRC Affiliation

The xBRC `brc` field is derived from OSTI metadata in this order:

1. Use `site_ownership_code` directly when present.
2. Otherwise inspect contract fields and `CN_DOE` identifiers.
3. Map known BRC contract numbers:

| Contract number | xBRC `brc` |
| --- | --- |
| `SC0018420` | `CABBI` |
| `SC0018409` | `GLBRC` |
| `AC36-08GO28308` | `CBI` |
| `AC02-05CH11231` | `JBEI` |

If neither `site_ownership_code` nor a known contract number is present, the
transform cannot infer the BRC affiliation.

### Current xBRC-Specific Gaps

Some xBRC fields are more specific than the current OSTI E-Link record model or
are intended for bioenergy.org display and filtering. These fields are not
currently populated from OSTI records unless the transform explicitly maps them:

- `species`
- `plasmid_features`
- `analysisType`
- `datasetType`
- `topic`
- `theme`
- `category`
- `ontology_annotations`

For species and taxon identifiers specifically, OSTI does not currently provide
a dedicated species slot in this transform. If an OSTI record includes a clear
NCBI Taxonomy identifier in related identifiers, additional transform logic
would be needed before it can populate the xBRC `species` slot.

## xBRC to OSTI

The `brc_to_osti` transform expects an xBRC `DatasetCollection` and produces an
OSTI-style object with a `records` array.

Key mappings include:

| xBRC source | OSTI target | Notes |
| --- | --- | --- |
| `datasets` | `records` | Each xBRC `Dataset` becomes one OSTI `Record`. |
| `title` | `title` | Direct mapping. |
| `description` | `description` | Direct mapping. |
| `date` | `publication_date`, `released_to_osti_date` | The same xBRC date is used for both OSTI fields. |
| `identifier` | `osti_id` | Only extracted when the identifier contains `osti.gov/biblio/`. |
| `bibliographicCitation` | `doi` | Supports `https://doi.org/...` and `doi:...` forms. |
| `brc` | `site_ownership_code` | Direct BRC code passthrough. |
| `keywords` | `keywords` | Direct mapping. |
| `dataset_url` or non-OSTI `identifier` | `site_url`, `links` | The dataset landing page is preferred. |
| `active` | `workflow_status` | `true` maps to `R`; falsey values map to `SR`. |
| `creator`, `contributors` | `authors`, `persons` | Names are split into OSTI first/middle/last fields when possible. |
| `funding`, `brc` | `organizations`, `sponsor_orgs`, `research_orgs` | xBRC funding and BRC affiliation are converted into OSTI organization structures. |
| `has_related_ids` | `identifiers`, `related_identifiers` | BioProject IDs and DOI references get special handling. |
| `media` | `media` | Media package metadata is preserved. |

The transform also sets these OSTI defaults:

- `access_limitations`: `["UNL"]`
- `product_type`: `DA`

### BRC-Derived OSTI Fields

When xBRC `brc` is present, the transform emits BRC-specific OSTI metadata:

- `site_ownership_code`
- DOE contract identifiers
- default sponsor organization information when no xBRC funding is provided
- BRC research organization names for OSTI `research_orgs`

This behavior is specific to xBRC. Generic metadata conversion tools should not
assume that all BRC-derived OSTI fields can be recovered from arbitrary OSTI
records.

## Round-Trip Expectations

The transforms are designed for operational metadata exchange, not a lossless
round trip. Several fields are normalized, inferred, defaulted, or omitted.

Expected non-lossless behavior includes:

- OSTI `description` maps to both xBRC `description` and `abstract`; converting
  back uses only xBRC `description`.
- xBRC `active` is represented as OSTI `workflow_status`, not as a native xBRC
  boolean in OSTI.
- xBRC-specific display and filtering fields, such as `topic`, `theme`,
  `category`, and `ontology_annotations`, are not currently emitted to OSTI.
- OSTI fields without xBRC equivalents may be omitted unless they have an
  explicit mapping.
- BRC affiliation may be inferred from contract numbers in `osti_to_brc`, while
  `brc_to_osti` emits contract numbers from the xBRC `brc` value.

For conversion validation, use the repository test suite:

```bash
make test
```

## Related Pages

- [CLI Usage](cli.md)
- [OSTI E-Link Integration](osti_elink_integration.md)
- [Updating the Schema](update_schema.md)
