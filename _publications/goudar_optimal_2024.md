---
layout: publication
categories: Journal
ref-authors:
- A. Goudar
- "F. D\xFCmbgen"
- T. D. Barfoot
- A. Schoellig
ref-journal: IEEE Robotics and Automation Letters
ref-link: https://doi.org/10.1109/LRA.2024.3354623
arxiv-link: https://arxiv.org/abs/2309.09011
ref-year: 2024
title: Optimal Initialization Strategies for Range-Only Trajectory Estimation
image: optimal_init.png
summary: "Combine range measurements from multiple UWB tags on a moving device to estimate the pose or trajectory, in a certifiably optimal way." 
---

Range-only (RO) pose estimation involves determining a robot's pose over time by measuring the distance between multiple devices on the robot, known as tags, and devices installed in the environment, known as anchors. The nonconvex nature of the range measurement model results in a cost function with possible local minima. In the absence of a good initialization, commonly used iterative solvers can get stuck in these local minima resulting in poor trajectory estimation accuracy. In this work, we propose convex relaxations to the original nonconvex problem based on semidefinite programs (SDPs). Specifically, we formulate computationally tractable SDP relaxations to obtain accurate initial pose and trajectory estimates for RO trajectory estimation under static and dynamic (i.e., constant-velocity motion) conditions. Through simulation and real experiments, we demonstrate that our proposed initialization strategies estimate the initial state accurately compared to iterative local solvers. Additionally, the proposed relaxations recover global minima under moderate range measurement noise levels. 

