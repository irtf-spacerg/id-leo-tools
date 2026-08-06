---
title: "A typology of Space Research Infrastructures"
abbrev: "SpaceRG-Infra"
category: info

docname: draft-sastry-spacerg-space-research-infra-typology-latest
submissiontype: IRTF
number:
date:
consensus: true
v: 3
area: IRTF
workgroup: "Systems and Protocol Aspects for Circumstellar Environments"
keyword:
 - simulators
 - emulators
 - testbeds
 - in-orbit platforms
 - datasets
 - measurement tools
 - implementations
 - libraries
 - visualizers
 - research platforms
venue:
  group: "Systems and Protocol Aspects for Circumstellar Environments"
  type: "Research Group"
  mail: "space@irtf.org"
  github: "irtf-spacerg/id-leo-tools"
  latest: "https://irtf-spacerg.github.io/id-leo-tools/draft-sastry-spacerg-space-research-infra-typology.html"

author:
 -
    fullname: Nishanth Sastry
    organization: University of Surrey
    email: n.sastry@surrey.ac.uk
 -
    fullname: Juan A. Fraire
    organization: Inria
    email: juan.fraire@inria.fr

normative:

informative:
  REGISTRY:
    title: SPACERG Space Networking Tools Registry
    target: https://irtf-spacerg.github.io/id-leo-tools/registry/
    author:
      org: IRTF Space Research Group
    date: false
  CONSTELLATIONS:
    title: SPACERG Satellite Constellation Registry
    target: https://irtf-spacerg.github.io/id-leo-constellations/registry/
    author:
      org: IRTF Space Research Group
    date: false
  DAGSTUHL:
    title: "Dagstuhl Seminar 26062: Connected Space: Challenges and Opportunities in Satellite Computing and Networking"
    target: https://www.dagstuhl.de/seminars/seminar-calendar/seminar-details/26062
    author:
      org: Schloss Dagstuhl, Leibniz Center for Informatics
    date: 2026-02

...

--- abstract

Space networking research increasingly relies on a heterogeneous ecosystem of software, datasets, experimental platforms, reference implementations, and operational research assets.
These resources have historically been developed independently by different research groups, agencies, and projects, making discovery, comparison, interoperability, and reuse difficult.
Existing registries typically catalogue tools individually but provide limited guidance on their functional role within the research lifecycle.

This document proposes a typology for research infrastructures relevant to the Space Research Group (SPACERG).
The proposed taxonomy groups resources by the research function they serve, independently of their implementation technology or project origin.
The typology provides a common vocabulary for describing software and non-software research assets, supports the organization of community registries, and facilitates interoperability, reproducibility, and long-term maintenance of research infrastructures.
The classification is intended to evolve as new classes of research resources emerge.
The typology is implemented by a machine-readable registry of research resources maintained by the research group.

--- middle

# Introduction

Research in space networking depends upon a broad collection of complementary research infrastructures.
These include simulation environments, network emulators, protocol implementations, datasets, browser-based experimentation environments, visualization tools, experimental testbeds, satellite constellations, and software supporting data collection and analysis.
While many of these resources have become widely adopted within individual research communities, they are often documented independently, use inconsistent terminology, and overlap in functionality.

As the Space Research Group (SPACERG) develops a shared registry of research infrastructures, it has become apparent that simply maintaining a list of available tools is insufficient.
Users require a consistent method of understanding _what role_ a resource plays within the research ecosystem, how it complements other resources, and where it fits within an experimental workflow.
A common typology also improves discoverability, assists researchers in selecting appropriate infrastructures, and enables more consistent metadata across independently maintained registries.

The purpose of this document is to establish a common vocabulary that lets researchers classify and discover research infrastructures relevant to space networking consistently.
It does not prescribe a fixed ontology.
The taxonomy is intended to support the SPACERG registry, facilitate interoperability with other research infrastructure catalogues, and provide a foundation for future standardization efforts within the IRTF and IETF research communities.

# The typology

The typology described in this document was developed by analysing the verified research resources collected from the community and curated in the SPACERG registry.
The categories emerged from the primary research purpose each resource serves.
Software architecture and implementation language proved to be poor discriminators: two resources built on the same framework and written in the same language may occupy entirely different positions in an experimental workflow.
This functional approach accommodates both software and non-software research assets and remains applicable as new technologies are introduced.

The initial categories identified include, under the names used by the registry:

-   **Simulator**, modelling network behaviour using abstract representations (flow-level, packet-level, or discrete-event) to support scalable experimentation without executing real protocol stacks.
-   **Emulator**, reproducing the timing and topology of target systems while executing real protocol implementations and operating-system network stacks.
-   **Testbed**, offering physical, virtual, or hybrid environments with real links, such as terminal deployments and ground stations, for integrated experimental evaluation.
-   **In-orbit platform**, representing operational or experimental space assets (research satellites, constellations, and hosted payloads) that provide real-world experimentation opportunities.
-   **Dataset / data**, including curated measurement datasets and live data services such as orbital-element feeds.
-   **Measurement**, providing tools and methodologies that produce new measurements, including browser-integrated extensions, terminal-telemetry collectors, Internet-scanning methodologies, and benchmarking frameworks.
-   **Implementation**, providing runnable protocol stacks, proxies, and flight software deployed in experiments, such as Bundle Protocol implementations, non-terrestrial-network radio access stacks, and performance-enhancing proxies.
-   **Library**, providing reusable building blocks embedded by other resources, such as orbit propagators, contact-plan generators, and routing libraries.
-   **Visualizer**, supporting analysis, interpretation, and presentation of orbital and network state.
-   **Research platform**, offering orchestration and service environments for experimentation, such as satellite edge-computing and serverless frameworks.

The registry vocabulary additionally reserves a small set of auxiliary labels (Meta-resource, Commercial / service, Unresolved, Other) for resources that fall outside these research categories or that await classification.

Although these categories provide broad coverage of the current SPACERG registry, they are not intended to be exhaustive.
New categories may emerge as the community develops additional research infrastructures, including digital twins, AI-assisted experimentation platforms, workflow management systems, and cloud-based experimentation environments.

## What resisted classification

Applying the typology to the collected resources exposed four boundaries that a single class label cannot carry on its own.
They are recorded here because they shape the registry schema, and because they are the places where two curators are most likely to disagree.

The first is the boundary between simulation and emulation.
Whether a resource executes real protocol stacks is the property researchers most often want to know, and it does not align cleanly with either class.
Some emulators run unmodified containers over shaped links, some simulators embed a real transport implementation, and some resources do either depending on how they are configured.
The registry therefore carries execution fidelity on its own axis, and the class label alone does not imply it.

The second is that a project and a resource are different units.
A testbed and the measurement traces it publishes have different licences, contacts, maintenance states and lifecycles, so they are described by separate records under different classes even when one produces the other.
Several projects in the registry appear this way, spanning three or four classes between them.

The third is that the distinction between a library and an implementation depends on how a resource is used.
The same codebase can be a standalone protocol stack in one deployment and an embedded component in another, and the class records the role in which it is most commonly encountered.

The fourth is that in-orbit platforms and testbeds share an access model.
Both are typically reached through an experimenter programme rather than a download, and the class records where the asset is while the access model is described separately.

None of the collected resources have so far required the Unresolved or Other labels.
That the categories held is a weak result: the collection comes from a community with shared assumptions about what counts as a research resource, and a sweep across adjacent fields would likely surface cases that do not fit.

# The SPACERG Registry

The typology in this document is implemented by a community registry maintained by SPACERG in the repository that also hosts this document, and published as a searchable page with JSON and CSV exports {{REGISTRY}}.
Each resource is described by one machine-readable record carrying its class under this typology, functional metadata (how orbital dynamics are defined, which layers are covered, whether real protocol stacks are exercised, the largest scale demonstrated in a publication, and input and output formats), and provenance metadata (license, a named contact, how the entry was collected, and when it was last verified).

Additions and corrections are made by pull request, one file per resource, and are validated automatically against the registry schema.
To be included, a resource should be specific to space or satellite networking, usable by others through a public artifact or a documented access program, and verifiable through a working URL and, where claims matter, a publication.

Registry entries are point-in-time observations: tools are abandoned, URLs move, and maintenance states go stale.
Each record therefore carries a last-verified date and entries are re-verified periodically.
Entries that fail verification are marked as historic rather than deleted, because unmaintained resources remain relevant as baselines against which published results were obtained.

# Relationship to other SPACERG work

This typology and the registry that implements it are complementary to the registry of announced, filed and deployed satellite constellations maintained by the research group {{CONSTELLATIONS}}.
This work catalogues what researchers can experiment with; that one catalogues what is being built and what has been claimed.
The two use the same contribution model, the same validation approach and the same publication mechanics, and are intended to be usable together.

One design choice is shared between them.
A record describes a single resource, under this typology, or a single authorisation, in the constellation registry, and a project-level or operator-level view is composed from the records by whoever needs one.
Both registries also treat their entries as observations at a date and carry the date with the claim.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

# Security Considerations

This document defines a vocabulary for describing research infrastructures and introduces no protocol mechanisms.
The registry that implements it records public information about publicly available resources.

Entries link to third-party code, data and services.
Inclusion in the registry carries no security assessment of what a link points to, and readers running registry-listed software should evaluate it as they would any other third-party dependency.

# IANA Considerations

This document has no IANA actions.

--- back

# Acknowledgments
{:numbered="false"}

The initial collection of research resources was assembled by the participants of Dagstuhl Seminar 26062, "Connected Space: Challenges and Opportunities in Satellite Computing and Networking", held from 1 to 4 February 2026.
The seminar page lists its organizers and participants {{DAGSTUHL}}, and the authors thank all of them.
The collection was extended by a systematic literature and web sweep in July 2026, and the typology described in this document was derived from it.
