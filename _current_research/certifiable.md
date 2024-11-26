---
title: Certifiable state estimation
image: local_minimum_real.png
date: 2022-09-12
categories: past
--- 

Common solvers used in robotics state estimation, such as Gauss-Newton or Levenberg-Marquardt, provide first-order optimal solutions very reliably. Because most optimization problems encountered in robotics are non-convex, these solutions may however correspond to local optima, and may be far from the global optimum. In this research project we are exploring ways to ensure the quality of candidate solutions, exploiting concepts from Lagrangian duality theory. An accessible  introduction to this topic is given in our [arXiv paper](https://arxiv.org/pdf/2206.05082.pdf) on robust line fitting. 

A summary of the work we did in this area was presented at the R:SS 2024 Workshop on Safe Autonomy, available [here](https://duembgen.github.io://drive.google.com/file/d/1Lxu64QotVzkOobjvWUaxNuXKzZYaRMAs/view), under the *extending the catalogue* section. In summary, we created novel certifiably optimal solvers for a variety of state estimation problems; including the non-linear and typically underdetermined [range-only localization](https://ieeexplore.ieee.org/document/10003973), localization from [non-isotropic measurements](https://ieeexplore.ieee.org/document/10706005), common in stereo-camera observations, and finally, rotation and pose averaging and synchronization from rotation measurements, using the [Cayley map](https://journals.sagepub.com/doi/full/10.1177/02783649241269337) to maintain polynomial problem formulations. 
