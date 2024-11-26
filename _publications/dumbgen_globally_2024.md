---
layout: publication
categories: Journal
ref-authors:
- "F. D\xFCmbgen"
- C. Holmes
- B. Agro
- T. D. Barfoot
ref-journal: IEEE Transactions on Robotics
ref-link: https://doi.org/10.1109/TRO.2024.3454570
arxiv-link: https://arxiv.org/abs/2308.05783
ref-code: https://github.com/utiasASRL/constraint_learning
ref-year: 2024
title: Toward Globally Optimal State Estimation Using Automatically Tightened Semidefinite Relaxations
image: tightening.png
summary: "Instead of a tedious pen-and-paper or expensive symbolic approach, find the redundant constraints for making the semidefinite relaxation of non-convex optimization problems tight using a numerical approach involving sampling feasible points and solving a nullspace problem." 
---

In recent years, semidefinite relaxations of common optimization problems in robotics have attracted growing attention due to their ability to provide globally optimal solutions. In many cases, it was shown that specific handcrafted redundant constraints are required to obtain tight relaxations and thus global optimality. These constraints are formulation-dependent and typically identified through a lengthy manual process. Instead, the present paper suggests an automatic method to find a set of sufficient redundant constraints to obtain tightness, if they exist. We first propose an efficient feasibility check to determine if a given set of variables can lead to a tight formulation. Secondly, we show how to scale the method to problems of bigger size. At no point of the process do we have to find redundant constraints manually. We showcase the effectiveness of the approach, in simulation and on real datasets, for range-based localization and stereo-based pose estimation. Finally, we reproduce semidefinite relaxations presented in recent literature and show that our automatic method always finds a smaller set of constraints sufficient for tightness than previously considered. 

