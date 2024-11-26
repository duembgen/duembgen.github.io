---
layout: publication
categories: Journal
ref-authors:
- F. Dümbgen
- C. Holmes
- T. D. Barfoot
ref-journal: IEEE Robotics and Automation Letters 
ref-link: https://ieeexplore.ieee.org/document/10003973
arxiv-link: https://arxiv.org/abs/2301.0832
ref-year: 2023
ref-code: https://github.com/utiasASRL/safe_and_smooth
title: "Safe and Smooth: Certified Continuous-Time Range-Only Localization"
image: local_minimum_real.png
summary: "Certify, in linear time, the solutions of a standard Gauss-Newton solver that computes the continuous-time trajectory estimates using sparse range measurements with a Gaussian Process motion prior."
---
A common approach to localize a mobile robot is by measuring distances to points of known positions, called anchors.  
Locating a device from distance measurements is typically posed as a non-convex optimization problem, stemming from the nonlinearity of the measurement model. Non-convex optimization problems may yield suboptimal solutions when local iterative solvers such as Gauss-Newton are employed. 
In this paper, we design an optimality certificate for continuous-time range-only localization. 
Our formulation allows for the integration of a motion prior, which ensures smoothness of the solution and is crucial for localizing from only a few distance measurements. The proposed certificate comes at little additional cost since it has the same complexity as the sparse local solver itself: linear in the number of positions. We show, both in simulation and on real-world datasets, that the efficient local solver often finds the globally optimal solution (confirmed by our certificate), but it may converge to local solutions with high errors, which our certificate correctly detects.
