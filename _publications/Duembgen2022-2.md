---
layout: publication
categories: Journal
ref-authors:
- F. Dümbgen
- C. Holmes 
- T. D. Barfoot
ref-journal: arXiv (submitted to IEEE Robotics and Automation Letters)
ref-link: https://arxiv.org/abs/2209.04266 
ref-year: 2022
title: "Safe and Smooth: Certified Continuous-Time Range-Only Localization"
image: local_minimum_sim.jpg
---

A common approach to localize a mobile robot is by measuring distances to points of known positions, called anchors. Locating a device from distance measurements is typically phrased as a non-convex optimization problem, stemming from the nonlinearity of the measurement model. Non-convex optimization problems may yield suboptimal solutions when local iterative solvers such as Gauss-Newton are employed. In this paper, we design an optimality certificate for continuous-time range-only localization. Our formulation allows for the integration of a motion prior, which ensures smoothness of the solution and is crucial for localizing from only a few distance measurements. The proposed certificate comes at little additional cost since it has the same complexity as the sparse local solver itself: linear in the number of positions. We show, both in simulation and on real-world datasets, that the efficient local solver often finds the globally optimal solution (confirmed by our certificate) and when it does not, simple random reinitialization eventually leads to the certifiable optimum. 
