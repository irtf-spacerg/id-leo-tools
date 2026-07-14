<!-- regenerate: off -->

# A typology of Space Research Infrastructures

This is the working area for the individual Internet-Draft, "A typology of Space Research Infrastructures", and for the SPACERG space networking tools registry that backs it.

* [Editor's Copy](https://irtf-spacerg.github.io/id-leo-tools/#go.draft-sastry-spacerg-space-research-infra-typology.html)
* [Datatracker Page](https://datatracker.ietf.org/doc/draft-sastry-spacerg-space-research-infra-typology)
* [Individual Draft](https://datatracker.ietf.org/doc/html/draft-sastry-spacerg-space-research-infra-typology)
* [Compare Editor's Copy to Individual Draft](https://irtf-spacerg.github.io/id-leo-tools/#go.draft-sastry-spacerg-space-research-infra-typology.diff)


## Tool registry

The registry lives under [`data/tools/`](data/tools/), one YAML file per
tool, and is published as a searchable page at
<https://irtf-spacerg.github.io/id-leo-tools/registry/> together with JSON
and CSV exports. To add or correct an entry, open a pull request (start
from [`data/TEMPLATE.yaml`](data/TEMPLATE.yaml)) or use the "Suggest a
tool" form on the page. See [data/README.md](data/README.md) for the field
reference and inclusion criteria.

To build the page locally:

```sh
$ pip install pyyaml
$ python scripts/build_site.py        # writes public/
$ python scripts/build_site.py --check  # validate only
```

## Contributing

See the
[guidelines for contributions](https://github.com/irtf-spacerg/id-leo-tools/blob//CONTRIBUTING.md).

The contributing file also has tips on how to make contributions, if you
don't already know how to do that.

## Command Line Usage

Formatted text and HTML versions of the draft can be built using `make`.

```sh
$ make
```

Command line usage requires that you have the necessary software installed.  See
[the instructions](https://github.com/martinthomson/i-d-template/blob/main/doc/SETUP.md).

