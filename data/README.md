# Registry data

One YAML file per tool under `data/tools/`. The registry page and the
JSON/CSV exports are built from these files by `scripts/build_site.py`.

## Adding or correcting an entry

Open a pull request that adds or edits a single file under `data/tools/`.
Start from [`TEMPLATE.yaml`](TEMPLATE.yaml), or use the "Suggest a tool" form
on the registry page, which composes the YAML for you. CI validates the
schema on every PR.

Corrections are as welcome as additions. Maintenance states in particular
are best-effort snapshots (see `verified:` in each file); if you know better,
send a PR that fixes the state and bumps `verified:`.

## Inclusion criteria

An entry should be:

1. specific to space or satellite networking (or a de facto standard
   dependency of such work), not a general Internet resource that happens to
   include some satellite data;
2. usable by others: a public artifact (code, data, service) or a documented
   access program (testbed sign-up, experimenter call);
3. verifiable: a working URL and, where claims matter (scale, maintenance),
   a publication or repository that backs them.

Historic but influential tools (e.g. unmaintained simulators that papers
still compare against) belong in the registry with `maintenance: inactive`.
Tools announced in papers without a public artifact do not; they can be
listed in the survey draft instead.

## Allowed values

- `class`: Simulator, Emulator, Testbed, In-orbit platform, Dataset / data,
  Measurement, Implementation, Library, Visualizer, Research platform,
  Meta-resource, Commercial / service, Unresolved, Other
- `domains`: LEO, Deep space / DTN, IoT, NTN-5G, GEO / DVB, Optical,
  Orbital compute, Ground segment, Orbits / astro, Security, Transport, Other
- `maintenance`: active, low, inactive, planned, unknown
- `real_stack`: yes, no, partial, na
- `source`: dagstuhl (Dagstuhl 26062 collection), sweep (July 2026
  literature/web sweep), community (submitted afterwards)

## Provenance

The initial data set was collected by the participants of Dagstuhl Seminar
26062 (February 2026) and extended by a systematic web and literature sweep
in July 2026. Every record carries `source`, `added` and `verified` fields.
