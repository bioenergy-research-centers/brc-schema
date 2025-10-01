# brc-schema

The Bioenergy Research Center data schema.

This schema supports the data search platform at [Bioenergy.org](https://bioenergy.org/).

See:

- [creating a dataset schema for the BRCs](https://docs.google.com/presentation/d/1Z7pq7JxbSkuKMhfWMPGPwbMKrysbqfyVnhvWDxqhy9U/edit#slide=id.p)
- [other background](https://docs.google.com/document/d/1H8fQ7IiCI_SASYuKNQElcpcPzfgHSrXMz8kwLfSWKvw/edit)

## Website

[https://bioenergy-research-centers.github.io/brc-schema](https://bioenergy-research-centers.github.io/brc-schema)

## Repository Structure

* [examples/](examples/) - example data
* [project/](project/) - project files (do not edit these)
* [src/](src/) - source files (edit these)
  * [brc_schema](src/brc_schema)
    * [schema](src/brc_schema/schema) -- LinkML schema
      (edit this)
    * [datamodel](src/brc_schema/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

* `make all`: make everything
* `make deploy`: deploys site
</details>

## CLI Commands

The `brcschema` command-line interface provides tools for data retrieval and transformation.

### Installation

Install the package with its dependencies:

```bash
poetry install
```

### Available Commands

#### `transform` - Transform data between OSTI and BRC formats

Transform input data from OSTI format to BRC schema or vice-versa.

```bash
brcschema transform -T <transformation_type> -o <output_file> <input_file>
```

**Options:**
- `-T, --tx-type`: Type of transformation. Either `osti_to_brc` or `brc_to_osti` (required)
- `-o, --output PATH`: Output YAML file path (required)
- `-v, --verbose`: Enable verbose logging (can be repeated for more verbosity)
- `-q, --quiet`: Suppress output except errors

**Examples:**

```bash
# Transform OSTI format to BRC schema
brcschema transform -T osti_to_brc -o data_out_brc_form.yaml data_in_osti_form.yaml

# Transform BRC schema to OSTI format
brcschema transform -T brc_to_osti -o data_out_osti_form.yaml data_in_brc_form.yaml
```

#### `retrieve-osti` - Retrieve records from OSTI E-Link API

Retrieve records from the OSTI E-Link 2.0 API by OSTI ID or DOI.

```bash
brcschema retrieve-osti [OPTIONS] -o <output_file>
```

**Options:**
- `--osti-ids TEXT`: One or more OSTI IDs to retrieve (can be repeated)
- `--dois TEXT`: One or more DOIs to retrieve (can be repeated)
- `--osti-id-file PATH`: File containing OSTI IDs, one per line
- `--doi-file PATH`: File containing DOIs, one per line
- `-o, --output PATH`: Output JSON file path (required)
- `--api-key TEXT`: OSTI API key for authentication
- `--no-pretty`: Disable pretty-printing of JSON output
- `-v, --verbose`: Enable verbose logging

**Examples:**

```bash
# Retrieve by OSTI IDs
brcschema retrieve-osti --osti-ids 2562995 2574191 -o records.json

# Retrieve by DOIs
brcschema retrieve-osti --dois 10.1002/aesr.202500034 -o records.json

# Retrieve from ID file
brcschema retrieve-osti --osti-id-file ids.txt -o records.json

# Mix of OSTI IDs and DOIs with authentication
brcschema retrieve-osti --osti-ids 2562995 --dois 10.1002/aesr.202500034 --api-key YOUR_KEY -o records.json

# With verbose logging
brcschema -vv retrieve-osti --osti-ids 2562995 -o records.json
```

### Complete Workflow Example

Retrieve OSTI records and transform them to BRC format:

```bash
# Step 1: Retrieve OSTI records
brcschema retrieve-osti --osti-ids 2562995 2574191 -o osti_records.json

# Step 2: Transform to BRC format
brcschema transform -T osti_to_brc -o brc_datasets.yaml osti_records.json
```

## Using the OSTI E-Link API

The package includes Python functions for retrieving records from the OSTI E-Link 2.0 API programmatically.

### Authentication

Many OSTI records require authentication. To access the API:

1. **Register for an API key** at: https://www.osti.gov/user/register?appname=ELINK
2. **Provide your API key** using one of these methods:

   **Method 1: Environment variable (recommended)**
   ```bash
   export OSTI_API_KEY="your_api_key_here"
   ```

   **Method 2: Pass directly to Python functions**
   ```python
   from brc_schema.util.elink import OSTIRecordRetriever
   
   retriever = OSTIRecordRetriever(api_key="your_api_key_here")
   ```

   **Method 3: Command-line option**
   ```bash
   brcschema retrieve-osti --api-key "your_api_key_here" --osti-ids 2562995 -o records.json
   ```

### Python API Usage

#### Simple Retrieval

```python
from brc_schema.util.elink import retrieve_osti_records

# Retrieve records and save to file
records = retrieve_osti_records(
    osti_ids=[2562995, 2574191],
    dois=["10.1002/aesr.202500034"],
    output_file="osti_records.json"
)

print(f"Retrieved {len(records)} records")
```

#### Class-Based Approach

```python
from brc_schema.util.elink import OSTIRecordRetriever

# Initialize retriever (will use OSTI_API_KEY environment variable if available)
retriever = OSTIRecordRetriever()

# Or initialize with explicit API key
retriever = OSTIRecordRetriever(api_key="your_api_key_here")

# Retrieve single record by OSTI ID
record = retriever.get_record_by_osti_id(2562995)
if record:
    print(f"Title: {record.get('title')}")

# Retrieve single record by DOI
record = retriever.get_record_by_doi("10.1002/aesr.202500034")

# Retrieve multiple records
records = retriever.get_records(
    osti_ids=[2562995, 2574191],
    dois=["10.1002/aesr.202500034"]
)

# Save records to file
retriever.save_records_to_file(
    output_path="output/osti_records.json",
    osti_ids=[2562995, 2574191],
    pretty=True
)
```

#### Reading IDs from Files

Create a text file with one ID per line (comments starting with `#` are ignored):

```text
# Example OSTI IDs
2562995
2574191
1807585
```

Then retrieve:

```bash
brcschema retrieve-osti --osti-id-file my_ids.txt -o records.json
```

Or in Python:

```python
from pathlib import Path

def read_ids_from_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f 
                if line.strip() and not line.strip().startswith('#')]

ids = read_ids_from_file('my_ids.txt')
records = retrieve_osti_records(osti_ids=ids, output_file="records.json")
```

### Output Format

Retrieved records are saved in JSON format following the OSTI schema structure:

```json
{
  "records": [
    {
      "osti_id": "2562995",
      "title": "Example Dataset Title",
      "description": "Dataset description...",
      "doi": "10.1002/aesr.202500034",
      "persons": [...],
      "publication_date": "2024-01-15",
      ...
    }
  ]
}
```

This format can be directly used with the `transform` command to convert to BRC schema.

### Additional Documentation

For more detailed information:
- [OSTI E-Link Integration Documentation](docs/osti_elink_integration.md)
- [OSTI E-Link 2.0 API Documentation](https://www.osti.gov/elink2api/)

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).

## Copyright Notice
InterBRC Data Products Portal Copyright (c) 2025, The Regents of the University of California, through Lawrence Berkeley National Laboratory, and UT-Battelle LLC,  through Oak Ridge National Laboratory (both subject to receipt of any required approvals from the U.S. Dept. of Energy), University of Wisconsin - Madison, University of Illinois Urbana - Champaign, and Michigan State University. All rights reserved.

If you have questions about your rights to use or distribute this software,
please contact Berkeley Lab's Intellectual Property Office at
IPO@lbl.gov.

NOTICE.  This Software was developed under funding from the U.S. Department
of Energy and the U.S. Government consequently retains certain rights.  As
such, the U.S. Government has been granted for itself and others acting on
its behalf a paid-up, nonexclusive, irrevocable, worldwide license in the
Software to reproduce, distribute copies to the public, prepare derivative
works, and perform publicly and display publicly, and to permit others to do so.