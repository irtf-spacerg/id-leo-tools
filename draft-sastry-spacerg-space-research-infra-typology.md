---
title: "A typology of Space Research Infrastructures"
abbrev: "SpaceRG-Infra"
category: info

docname: draft-sastry-spacerg-space-research-infra-typology-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
date:
consensus: true
v: 3
# area: AREA
# workgroup: WG Working Group
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
#  group: WG
#  type: Working Group
#  mail: space@irtf.org
#  arch: https://example.com/WG
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

...

--- abstract

Space networking research increasingly relies on a heterogeneous ecosystem of software, datasets, experimental platforms, reference implementations, and operational research assets. These resources have historically been developed independently by different research groups, agencies, and projects, making discovery, comparison, interoperability, and reuse difficult. Existing registries typically catalogue tools individually but provide limited guidance on their functional role within the research lifecycle.

This document proposes a typology for research infrastructures relevant to the Space Research Group (SPACERG). Rather than classifying resources according to implementation technology or project origin, the proposed taxonomy groups resources according to their research function. The typology provides a common vocabulary for describing software and non-software research assets, supports the organization of community registries, and facilitates interoperability, reproducibility, and long-term maintenance of research infrastructures. The classification is intended to evolve as new classes of research resources emerge. The typology is implemented by a machine-readable registry of research resources maintained by the research group.

--- middle

# Introduction


Research in space networking depends upon a broad collection of complementary research infrastructures. These include simulation environments, network emulators, protocol implementations, datasets, browser-based experimentation environments, visualization tools, experimental testbeds, satellite constellations, and software supporting data collection and analysis. While many of these resources have become widely adopted within individual research communities, they are often documented independently, use inconsistent terminology, and overlap in functionality.

As the Space Research Group (SPACERG) develops a shared registry of research infrastructures, it has become apparent that simply maintaining a list of available tools is insufficient. Users require a consistent method of understanding _what role_ a resource plays within the research ecosystem, how it complements other resources, and where it fits within an experimental workflow. A common typology also improves discoverability, assists researchers in selecting appropriate infrastructures, and enables more consistent metadata across independently maintained registries.

The typology described in this document was developed through an analysis of the more than 110 verified research resources collected from the community and curated in the SPACERG registry. Rather than deriving categories from software architecture or implementation language, the classification emerged from the primary research purpose served by each resource. This functional approach accommodates both software and non-software research assets and remains applicable as new technologies are introduced.

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

Although these categories provide broad coverage of the current SPACERG registry, they are not intended to be exhaustive. New categories may emerge as the community develops additional research infrastructures, including digital twins, AI-assisted experimentation platforms, workflow management systems, and cloud-based experimentation environments.

The purpose of this document is therefore not to prescribe a fixed ontology, but rather to establish a common vocabulary that enables researchers to consistently classify and discover research infrastructures relevant to space networking. The taxonomy is intended to support the SPACERG registry, facilitate interoperability with other research infrastructure catalogues, and provide a foundation for future standardization efforts within the IRTF and IETF research communities.

# The SPACERG Registry

The typology in this document is implemented by a community registry maintained by SPACERG in the repository that also hosts this document, and published as a searchable page with JSON and CSV exports {{REGISTRY}}. Each resource is described by one machine-readable record carrying its class under this typology, functional metadata (how orbital dynamics are defined, which layers are covered, whether real protocol stacks are exercised, the largest scale demonstrated in a publication, and input and output formats), and provenance metadata (license, a named contact, how the entry was collected, and when it was last verified).

Additions and corrections are made by pull request, one file per resource, and are validated automatically against the registry schema. To be included, a resource should be specific to space or satellite networking, usable by others through a public artifact or a documented access program, and verifiable through a working URL and, where claims matter, a publication.

Registry entries are point-in-time observations: tools are abandoned, URLs move, and maintenance states go stale. Each record therefore carries a last-verified date and entries are re-verified periodically. Entries that fail verification are marked as historic rather than deleted, because unmaintained resources remain relevant as baselines against which published results were obtained.

# Conventions and Definitions

{::boilerplate bcp14-tagged}


# Security Considerations

TODO Security


# IANA Considerations

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

TODO acknowledge.
