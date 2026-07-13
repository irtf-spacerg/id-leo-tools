---
###
# Internet-Draft Markdown Template
#
# Rename this file from draft-todo-yourname-protocol.md to get started.
# Draft name format is "draft-<yourname>-<workgroup>-<name>.md".
#
# For initial setup, you only need to edit the first block of fields.
# Only "title" needs to be changed; delete "abbrev" if your title is short.
# Any other content can be edited, but be careful not to introduce errors.
# Some fields will be set automatically during setup if they are unchanged.
#
# Don't include "-00" or "-latest" in the filename.
# Labels in the form draft-<yourname>-<workgroup>-<name>-latest are used by
# the tools to refer to the current version; see "docname" for example.
#
# This template uses kramdown-rfc: https://github.com/cabo/kramdown-rfc
# You can replace the entire file if you prefer a different format.
# Change the file extension to match the format (.xml for XML, etc...)
#
###
title: "A typology of Space Research Infrastructures"
abbrev: "SpaceRG-Infra"
category: info

docname: draft-sastry-spacerg-space-research-infra-typology-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
date:
consensus: true
v: 3
area: AREA
workgroup: WG Working Group
keyword:
 - simulators
 - emulators
 - testbeds
 - research constellations
 - datasets and data generation tools
 - browser plugins
venue:
  group: WG
  type: Working Group
  mail: space@irtf.org
  arch: https://example.com/WG
  github: irtf-spacerg/id-leo-tools
  latest: https://example.com/LATEST

author:
 -
    fullname: Nishanth Sastry
    organization: University of Surrey
    email: n.sastry@surrey.ac.uk
    
normative:

informative:

...

--- abstract

Space networking research increasingly relies on a heterogeneous ecosystem of software, datasets, experimental platforms, reference implementations, and operational research assets. These resources have historically been developed independently by different research groups, agencies, and projects, making discovery, comparison, interoperability, and reuse difficult. Existing registries typically catalogue tools individually but provide limited guidance on their functional role within the research lifecycle.

This document proposes a typology for research infrastructures relevant to the Space Research Group (SPACERG). Rather than classifying resources according to implementation technology or project origin, the proposed taxonomy groups resources according to their research function. The typology provides a common vocabulary for describing software and non-software research assets, supports the organization of community registries, and facilitates interoperability, reproducibility, and long-term maintenance of research infrastructures. The classification is intended to evolve as new classes of research resources emerge.

--- middle

# Introduction


Research in space networking depends upon a broad collection of complementary research infrastructures. These include simulation environments, network emulators, protocol implementations, datasets, browser-based experimentation environments, visualization tools, experimental testbeds, satellite constellations, and software supporting data collection and analysis. While many of these resources have become widely adopted within individual research communities, they are often documented independently, use inconsistent terminology, and overlap in functionality.

As the Space Research Group (SPACERG) develops a shared registry of research infrastructures, it has become apparent that simply maintaining a list of available tools is insufficient. Users require a consistent method of understanding _what role_ a resource plays within the research ecosystem, how it complements other resources, and where it fits within an experimental workflow. A common typology also improves discoverability, assists researchers in selecting appropriate infrastructures, and enables more consistent metadata across independently maintained registries.

The typology described in this document was developed through an analysis of approximately 130 research resources collected from the community. Rather than deriving categories from software architecture or implementation language, the classification emerged from the primary research purpose served by each resource. This functional approach accommodates both software and non-software research assets and remains applicable as new technologies are introduced.

The initial categories identified include:

-   **Browser plugins**, providing browser-integrated experimentation or protocol support.
-   **Data resources**, including curated datasets and data collection scripts or methodologies.
-   **Emulators**, which reproduce the behaviour of target systems while executing real protocol implementations.
-   **Simulators**, which model network behaviour using abstract representations to support scalable experimentation.
-   **Reference implementations**, providing authoritative implementations of protocols, architectures, or research frameworks intended for validation and interoperability.
-   **Research satellites and constellations**, representing operational or experimental space assets that provide real-world experimentation opportunities.
-   **Testbeds**, offering physical, virtual, or hybrid environments for integrated experimental evaluation.
-   **Visualization tools**, supporting analysis, interpretation, and presentation of experimental results.

Although these categories provide broad coverage of the current SPACERG registry, they are not intended to be exhaustive. New categories may emerge as the community develops additional research infrastructures, including digital twins, AI-assisted experimentation platforms, orchestration frameworks, benchmark suites, workflow management systems, and cloud-based experimentation environments.

The purpose of this document is therefore not to prescribe a fixed ontology, but rather to establish a common vocabulary that enables researchers to consistently classify and discover research infrastructures relevant to space networking. The taxonomy is intended to support the SPACERG registry, facilitate interoperability with other research infrastructure catalogues, and provide a foundation for future standardization efforts within the IRTF and IETF research communities.

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
