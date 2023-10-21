---
title: Certifiable perception
image: local_minimum_real.png
date: 2022-09-12
categories: past
--- 

Common solvers used in robotics, such as Gauss-Newton or Levenberg-Marquardt, provide first-order optimal solutions to localization problems. Because most optimization problems encountered in robotics are non-convex, these solutions may correspond to local optima, and may be far from the global optimum. In our current research we are exploring ways to ensure the quality of candidate solutions, exploiting concepts from Lagrangian duality theory. In particular, we are interested in non-linear measurement models such as distances or angles, which arise for instance when doing localization from ultra-wideband signals, sound, or Bluetooth signals, to name a few. An accessible  introduction to this topic is given in our [arXiv paper](https://arxiv.org/pdf/2206.05082.pdf) on robust line fitting, and our first publication on certified range-only localization can be found [here](https://arxiv.org/abs/2209.04266). 
