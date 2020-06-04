## Package dependency networks

**Searches + manual filtering**: 

("Complex Networks" OR "Network Analysis") AND ("Software Repository" OR "Package Repository")

"Package dependency" AND  (network OR  graph)

"Component dependency" AND  (network OR  graph)

("network" OR  "graph") AND (pypi OR npm OR pear OR "Maven central")

**Databases:** 

SCOPUS, Google Scholar

---



Boldi, P. (2019). **How network analysis can improve the reliability of modern software ecosystems.** Proceedings - 2019 IEEE 1st International Conference on Cognitive Machine Intelligence, CogMI 2019. https://doi.org/10.1109/CogMI48466.2019.00032

>*Modern software development is increasingly dependent on components, libraries and frameworks coming from third party vendors or open-source suppliers and made available through a number of platforms (or 'forges'). This way of writing software puts an emphasis on reuse and on composition, commoditizing the services which modern applications require. On the other hand, bugs and vulnerabilities in a single library living in one such ecosystem can affect, directly or by transitivity, a huge number of other libraries and applications. Currently, only product-level information on library dependencies is used to contain this kind of danger, but this knowledge often reveals itself too imprecise to lead to effective (and possibly automated) handling policies. We will discuss how fine-grained function-level dependencies can greatly improve reliability and reduce the impact of vulnerabilities on the whole software ecosystem.*



Kikas, R., Gousios, G., Dumas, M., & Pfahl, D. (2017). **Structure and evolution of package dependency networks**. IEEE International Working Conference on Mining Software Repositories. https://doi.org/10.1109/MSR.2017.55

>*Software developers often include available open-source software packages into their projects to minimize redundant effort. However, adding a package to a project can also introduce risks, which can propagate through multiple levels of dependencies. Currently, not much is known about the structure of open-source package ecosystems of popular programming languages and the extent to which transitive bug propagation is possible. This paper analyzes the dependency network structure and evolution of the JavaScript, Ruby, and Rust ecosystems. The reported results reveal significant differences across language ecosystems. The results indicate that the number of transitive dependencies for JavaScript has grown 60% over the last year, suggesting that developers should look more carefully into their dependencies to understand what exactly is included. The study also reveals that vulnerability to a removal of the most popular package is increasing, yet most other packages have a decreasing impact on vulnerability. The findings of this study can inform the development of dependency management tools.*



Decan, A., Mens, T., & Claes, M. (2016). **On the Topology of Package Dependency Networks A Comparison of Three Programming Language Ecosystems**. Proccedings of the 10th European Conference on Software Architecture Workshops. https://doi.org/10.1145/2993412.3003382

>*Package-based software ecosystems are composed of thou-sands of interdependent software packages. Many empiri-cal studies have focused on software packages belonging to a single software ecosystem, and suggest to generalise the results to more ecosystems. We claim that such a general-isation is not always possible, because the technical struc-ture of software ecosystems can be very different, even if these ecosystems belong to the same domain. We confirm this claim through a study of three big and popular package-based programming language ecosystems: R's CRAN archive network, Python's PyPI distribution, and JavaScript's NPM package manager. We study and compare the structure of their package dependency graphs and reveal some impor-tant differences that may make it difficult to generalise the findings of one ecosystem to another one.*



Wittern, E., Suter, P., & Rajagopalan, S. (2016). **A look at the dynamics of the JavaScript package ecosystem**. Proceedings - 13th Working Conference on Mining Software Repositories, MSR 2016. https://doi.org/10.1145/2901739.2901743

>*The node package manager (npm) serves as the frontend to a large repository of JavaScript-based software packages, which foster the development of currently huge amounts of server-side Node.js and client-side JavaScript applications. In a span of 6 years since its inception, npm has grown to become one of the largest software ecosystems, hosting more than 230, 000 packages, with hundreds of millions of package installations every week. In this paper, we examine the npm ecosystem from two complementary perspectives: 1) we look at package descriptions, the dependencies among them, and download metrics, and 2) we look at the use of npm packages in publicly available applications hosted on GitHub. In both perspectives, we consider historical data, providing us with a unique view on the evolution of the ecosystem. We present analyses that provide insights into the ecosystem's growth and activity, into conflicting measures of package popularity, and into the adoption of package versions over time. These insights help understand the evolution of npm, design better package recommendation engines, and can help developers understand how their packages are being used.*



Kula, R. G., De Roover, C., German, D. M., Ishio, T., & Inoue, K. (2018). **A generalized model for visualizing library popularity, adoption, and diffusion within a software ecosystem**. 25th IEEE International Conference on Software Analysis, Evolution and Reengineering, SANER 2018 - Proceedings. https://doi.org/10.1109/SANER.2018.8330217

>*The popularity of super repositories such as Maven Central and the CRAN is a testament to software reuse activities in both open-source and commercial projects alike. However, several studies have highlighted the risks and dangers brought about by application developers keeping dependencies on outdated library versions. Intelligent mining of super repositories could reveal hidden trends within the corresponding software ecosystem and thereby provide valuable insights for such dependency-related decisions. In this paper, we propose the Software Universe Graph (SUG) Model as a structured abstraction of the evolution of software systems and their library dependencies over time. To demonstrate the SUG's usefulness, we conduct an empirical study using 6,374 Maven artifacts and over 6,509 CRAN packages mined from their real-world ecosystems. Visualizations of the SUG model such as 'library coexistence pairings' and 'dependents diffusion' uncover popularity, adoption and diffusion patterns within each software ecosystem. Results show the Maven ecosystem as having a more conservative approach to dependency updating than the CRAN ecosystem.*



Hejderup, J., Van Deursen, A., & Gousios, G. (2018). **Software ecosystem call graph for dependency management.** Proceedings - International Conference on Software Engineering. https://doi.org/10.1145/3183399.3183417

>*A popular form of software reuse is the use of open source software libraries hosted on centralized code repositories, such as Maven or npm. Developers only need to declare dependencies to external libraries, and automated tools make them available to theworkspace of the project. Recent incidents, such as the Equifax data breach and the leftpad package removal, demonstrate the difficulty in assessing the severity, impact and spread of bugs in dependency networks. While dependency checkers are being adapted as a counter measure, they only provide indicative information. To remedy this situation, we propose a fine-grained dependency network that goes beyond packages and into call graphs. The result is a versioned ecosystemlevel call graph. In this paper,we outline the process to construct the proposed graph and present a preliminary evaluation of a security issue from a core package to an affected client application.*



Benelallam, A., Harrand, N., Soto-Valero, C., Baudry, B., & Barais, O. (2019). **The maven dependency graph: A temporal graph-based representation of maven central.** IEEE International Working Conference on Mining Software Repositories. https://doi.org/10.1109/MSR.2019.00060

>*The Maven Central Repository provides an extraordinary source of data to understand complex architecture and evolution phenomena among Java applications. As of September 6, 2018, this repository includes 2.8M artifacts (compiled piece of code implemented in a JVM-based language), each of which is characterized with metadata such as exact version, date of upload and list of dependencies towards other artifacts. Today, one who wants to analyze the complete ecosystem of Maven artifacts and their dependencies faces two key challenges: (i) this is a huge data set; and (ii) dependency relationships among artifacts are not modeled explicitly and cannot be queried. In this paper, we present the Maven Dependency Graph. This open source data set provides two contributions: a snapshot of the whole Maven Central taken on September 6, 2018, stored in a graph database in which we explicitly model all dependencies; an open source infrastructure to query this huge dataset.*



Zheng, X., Zeng, D., Li, H., & Wang, F. (2008). **Analyzing open-source software systems as complex networks.** Physica A: Statistical Mechanics and Its Applications. https://doi.org/10.1016/j.physa.2008.06.050

>*Software systems represent one of the most complex man-made artifacts. Understanding the structure of software systems can provide useful insights into software engineering efforts and can potentially help the development of complex system models applicable to other domains. In this paper, we analyze one of the most popular open-source Linux meta packages/distributions called the Gentoo Linux. In our analysis, we model software packages as nodes and dependencies among them as edges. Our empirical results show that the resulting Gentoo network cannot be easily explained by existing complex network models. This in turn motivates our research in developing two new network growth models in which a new node is connected to an old node with the probability that depends not only on the degree but also on the "age" of the old node. Through computational and empirical studies, we demonstrate that our models have better explanatory power than the existing ones. In an effort to further explore the properties of these new models, we also present some related analytical results.*



##  Related

Cox, J., Bouwers, E., Eekelen, M. Van, & Visser, J. (2015). **Measuring Dependency Freshness in Software Systems**. Proceedings - International Conference on Software Engineering. https://doi.org/10.1109/ICSE.2015.140



Decan, A., Mens, T., & Claes, M. (2017). **An empirical comparison of dependency issues in OSS packaging ecosystems.** SANER 2017 - 24th IEEE International Conference on Software Analysis, Evolution, and Reengineering. https://doi.org/10.1109/SANER.2017.7884604



Bogart, C., Kästner, C., & Herbsleb, J. (2016). **When it breaks, it breaks: How ecosystem developers reason about the stability of dependencies.** Proceedings - 2015 30th IEEE/ACM International Conference on Automated Software Engineering Workshops, ASEW 2015. https://doi.org/10.1109/ASEW.2015.21



Bogart, C., Kästner, C., Herbsleb, J., & Thung, F. (2016). **How to break an API: Cost negotiation and community values in three software ecosystems.** Proceedings of the ACM SIGSOFT Symposium on the Foundations of Software Engineering. https://doi.org/10.1145/2950290.2950325



Abate, P., Boender, J., Di Cosmo, R., & Zacchiroli, S. (2009). **Strong dependencies between software components.** 2009 3rd International Symposium on Empirical Software Engineering and Measurement, ESEM 2009. https://doi.org/10.1109/ESEM.2009.5316017



Abate, P., Di Cosmo, R., Gesbert, L., Le Fessant, F., Treinen, R., & Zacchiroli, S. (2015). **Mining component repositories for installability issues.** IEEE International Working Conference on Mining Software Repositories. https://doi.org/10.1109/MSR.2015.10



Lertwittayatrai, N., Kula, R. G., Onoue, S., Hata, H., Rungsawang, A., Leelaprute, P., & Matsumoto, K. (2018). **Extracting Insights from the Topology of the JavaScript Package Ecosystem.** Proceedings - Asia-Pacific Software Engineering Conference, APSEC. https://doi.org/10.1109/APSEC.2017.36



Decan, A., Mens, T., & Constantinou, E. (2018). **On the impact of security vulnerabilities in the npm package dependency network.** Proceedings - International Conference on Software Engineering. https://doi.org/10.1145/3196398.3196401



Bommarito, E., & Bommarito, M. J. (2019). **An Empirical Analysis of the Python Package Index (PyPI).** SSRN Electronic Journal. https://doi.org/10.2139/ssrn.3426281
