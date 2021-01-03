# OLIVIA

[![Build Status](https://travis-ci.com/dsr0018/olivia.svg?branch=master)](https://travis-ci.com/dsr0018/olivia)
[![codecov](https://codecov.io/gh/dsr0018/olivia/branch/master/graph/badge.svg)](https://codecov.io/gh/dsr0018/olivia)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0b151ed6a3794874b1d3083e2532497d)](https://www.codacy.com/manual/dsr0018/olivia?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dsr0018/olivia&amp;utm_campaign=Badge_Grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dsr0018_olivia&metric=alert_status)](https://sonarcloud.io/dashboard?id=dsr0018_olivia)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dsr0018_olivia&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=dsr0018_olivia)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dsr0018_olivia&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=dsr0018_olivia)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dsr0018_olivia&metric=security_rating)](https://sonarcloud.io/dashboard?id=dsr0018_olivia)

_**Open-source Library Indexes Vulnerability Identification and Analysis**_

The use of centralized library repositories (such as PyPI for Python, Maven for Java, npm for Node.js, CRAN for R, etc.) to reduce development times and costs is universal, in virtually all languages and types of software projects. Due to the transitivity of dependencies, the appearance of a single defect in the repository can have extensive and difficult-to-predict effects on the ecosystem. These defects cause functional errors or performance or security problems. The risk is difficult to grasp for developers, who only explicitly import a small part of the dependencies.

OLVIA uses an approach based on the vulnerability of the dependency network of software packages, which measures how sensitive the repository is to the random introduction of defects. The goals of the model are to contribute to the understanding of propagation mechanisms of software defects and to study feasible protection strategies. 

OLIVIA implements part of the results from the author's final year project for the BSc in Computer Science Engineering at the University of Burgos. Work tutored by Prof. Carlos López Nozal and Prof. Jose Ignacio Santos Martín.

## Intended audience
OLIVIA may be of interest to multiple parties:
* __Centralised package managers__, to establish policies and manual or automatic control processes that improve the security and stability of the repositories.
* __Software developers__ in general, to assess the different risks introduced by the dependencies used in their projects, and __package developers__ in particular to understand their responsibility on the ecosystem.
* Developers of __continuous quality tools__, to define the concept of vulnerability based on the modeling of the network of package dependencies.

## Key results
The results obtained suggest that:

* Network’s vulnerability is related to the size of the largest strongly connected component present, a structure caused by the appearance of cyclic dependencies. When this component has a significant size the vulnerability of the network is much greater. By protecting these packets to avoid the introduction or propagation of defects we can almost completely eliminate the network’s vulnerability, although depending on their number, this approach may not be useful in practice. 
* We use a variety of techniques to narrow down the sets of important packets in relation to the network’s vulnerability, achieving reductions of a similar magnitude by acting on a smaller number of packages, and to heuristically select a specific number of packages, a problem whose exact solution we prove to be intractable.
* Example models for PyPI and Maven are provided. Models for other package repositories are easy to build from arbitrary dependency data.

## Getting started
Jupyter notebooks in the root folder of the repository (*A-Model.ipynb*, *B-Analysis.ipynb*, *C-Immunization.ipynb*) contain a user guide covering the main use cases for the library. 

OLIVIA API documentation is contained in */docs* and may be accessed through https://dsr0018.github.io/olivia/ 

## License
Copyright (c) 2021 Daniel Setó Rey

OLIVIA is distributed under the MIT License. See LICENSE file for details.

Dependency Network Models in /data are built from libraries.io snapshots by Tidelift (https://libraries.io/data) and are made available under the CC BY-SA 4.0 License (https://creativecommons.org/licenses/by-sa/4.0/) 