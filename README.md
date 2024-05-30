# brc-schema

Example schema

See:

- [creating a dataset schema for the BRCs](https://docs.google.com/presentation/d/1Z7pq7JxbSkuKMhfWMPGPwbMKrysbqfyVnhvWDxqhy9U/edit#slide=id.p)
- [other background](https://docs.google.com/document/d/1H8fQ7IiCI_SASYuKNQElcpcPzfgHSrXMz8kwLfSWKvw/edit)

## Website

[https://bioenergy-research-centers.github.io/brc-schema](https://bioenergy-research-centers.github.io/brc-schema)

(will not work so long as repo is private)

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

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
