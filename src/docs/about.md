# About the BRC Schema

The BRC schema is used with data on the <https://bioenergy.org/> data portal.

It is intended to represent metadata most relevant to the DOE bioenergy research community. It has also been designed to align with the data submission schema used by [OSTI.gov](https://www.osti.gov/).

## Bioenergy Research Centers

The schema covers datasets from four DOE Bioenergy Research Centers (BRCs). Each dataset names its primary center in the `brc` slot:

| Code | Center |
|------|--------|
| `CABBI` | Center for Advanced Bioenergy and Bioproducts Innovation |
| `CBI` | Center for Bioenergy Innovation |
| `GLBRC` | Great Lakes Bioenergy Research Center |
| `JBEI` | Joint BioEnergy Institute |

### BESC data under CBI

CBI was preceded by the [BioEnergy Science Center (BESC)](https://www.ornl.gov/news/besc-caps-biofuels-research-legacy-license-custom-microbe-enchi-corporation/), also based at Oak Ridge National Laboratory. BESC was a separate project with its own datasets and branding, but its legacy data is gradually being brought into CBI's collection. CBI data may therefore include datasets produced by BESC.

The schema treats CBI as the continuation of BESC. There is no separate `BESC` value in `BRCEnum`; BESC datasets use `brc: CBI`. When transforming OSTI records, organization names that mention "BESC" or "BioEnergy Science Center" are assigned to CBI.
