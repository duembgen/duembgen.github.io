---
layout: publication
categories: Journal
ref-authors:
- F. Dümbgen
- C. Holmes
- B. Agro
- T. D. Barfoot
ref-journal: under review
ref-arxiv: https://arxiv.org/abs/2308.05783
ref-year: 2023
ref-code: https://github.com/utiasASRL/constraint_learning
title: "Toward Globally Optimal State Estimation Using Automatically Tightened Semidefinite Relaxations"
image: tightening.png
---

In recent years, semidefinite relaxations of common optimization problems in robotics have attracted growing attention due to their ability to provide globally optimal solutions. In many cases, it was shown that specific handcrafted redundant constraints are required to obtain tight relaxations and thus global optimality. These constraints are formulation-dependent and typically require a lengthy manual process to find. Instead, the present paper suggests an automatic method to find a set of sufficient redundant constraints to obtain tightness, if they exist. We first propose an efficient feasibility check to determine if a given set of variables can lead to a tight formulation. Secondly, we show how to scale the method to problems of bigger size. At no point of the process do we have to manually find redundant constraints. We showcase the effectiveness of the approach, in simulation and on real datasets, for range-based localization and stereo-based pose estimation. Finally, we reproduce semidefinite relaxations presented in recent literature and show that our automatic method finds a smaller set of constraints sufficient for tightness than previously considered. 
