# repo-net
**Studying vulnerabilities in package dependency networks**

The use of libraries from open source package repositories to reduce development time and cost is almost universal, regarding all languages and types of software projects.  However, their inclusion introduces risks such as exposure to bugs and malicious modifications, those derived from the maintenance and updating of the software and, ultimately, all those inherent in the functional dependence on a third party. These risks can be difficult to appreciate in their entirety by the developers, who only explicitly import a small part of the libraries used in each project. Due to the transitivity of dependencies, a single defect or modification can have extensive and difficult-to-predict effects on the software ecosystem.

In this project we will build a packet dependency network model for the analysis of its vulnerability to failures and attacks. Our aim is to contribute to improve the risk assessment of external dependencies in software projects, the design of package management tools and the organization of activities and resources in open source development ecosystems.
