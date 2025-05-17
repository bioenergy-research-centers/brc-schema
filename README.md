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