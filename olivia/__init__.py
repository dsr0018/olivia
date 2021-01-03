"""
OLIVIA (Open-source Library Indexes Vulnerability Identification and Analysis).

The use of centralized library repositories to reduce development times and costs is universal, in virtually all
languages and types of software projects. Due to the transitivity of dependencies, the appearance of a single defect
in the repository can have extensive and difficult-to-predict effects on the ecosystem. These defects cause functional
errors or performance or security problems. The risk is difficult to grasp for developers, who only explicitly import
a small part of the dependencies.

OLVIA uses an approach based on the vulnerability of the dependency network of software packages, which measures how
sensitive the repository is to the random introduction of defects. The goals of the model are to contribute to the
understanding of propagation mechanisms of software defects and to study feasible protection strategies.

Copyright (c) 2021 Daniel Setó Rey

OLIVIA is distributed under the MIT License. See LICENSE file for details.
Includes tools for the analysis of package dependency networks vulnerability to failures and attacks.
"""