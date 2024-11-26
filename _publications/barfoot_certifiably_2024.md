---
layout: publication
categories: Journal
ref-authors:
- T. D. Barfoot
- C. Holmes
- "F. D\xFCmbgen"
ref-journal: International Journal of Robotics Research
ref-link: https://doi.org/10.1177/02783649241269337
arxiv-link: https://arxiv.org/abs/2308.12418
ref-year: 2024
title: Certifiably Optimal Rotation and Pose Estimation Based on the Cayley Map
image: cayley.png
---

We present novel, convex relaxations for rotation and pose estimation problems that can a posteriori guarantee global optimality for practical measurement noise levels. Some such relaxations exist in the literature for specific problem setups that assume the matrix von Mises-Fisher distribution (a.k.a., matrix Langevin distribution or chordal distance) for isotropic rotational uncertainty. However, another common way to represent uncertainty for rotations and poses is to define anisotropic noise in the associated Lie algebra. Starting from a noise model based on the Cayley map, we define our estimation problems, convert them to Quadratically Constrained Quadratic Programs (QCQPs), then relax them to Semidefinite Programs (SDPs), which can be solved using standard interior-point optimization methods; global optimality follows from Lagrangian strong duality. We first show how to carry out basic rotation and pose averaging. We then turn to the more complex problem of trajectory estimation, which involves many pose variables with both individual and inter-pose measurements (or motion priors). Our contribution is to formulate SDP relaxations for all these problems based on the Cayley map (including the identification of redundant constraints) and to show them working in practical settings. We hope our results can add to the catalogue of useful estimation problems whose solutions can be a posteriori guaranteed to be globally optimal.


