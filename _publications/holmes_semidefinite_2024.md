---
layout: publication
categories: Journal
ref-authors:
- C. Holmes
- "F. D\xFCmbgen"
- T. D. Barfoot
ref-journal: IEEE Transactions on Robotics
ref-link: https://doi.org/10.1109/TRO.2024.3475220
arxiv-link: https://arxiv.org/abs/2308.07275
ref-year: 2024
title: On Semidefinite Relaxations for Matrix-Weighted State-Estimation Problems in Robotics
image: matrix-weights.png
summary: "Derive certifiably optimal solutions to non-isotropic point-cloud registration (Wahba's problem) and landmark-based SLAM, for which available certifiably optimal solvers assuming isotropic noise fail."
---

In recent years, there has been remarkable progress in the development of so-called certifiable perception methods, which leverage semidefinite, convex relaxations to find global optima of perception problems in robotics. However, many of these relaxations rely on simplifying assumptions that facilitate the problem formulation, such as an isotropic measurement noise distribution. In this paper, we explore the tightness of the semidefinite relaxations of matrix-weighted (anisotropic) state-estimation problems and reveal the limitations lurking therein: matrix-weighted factors can cause convex relaxations to lose tightness. In particular, we show that the semidefinite relaxations of localization problems with matrix weights may be tight only for low noise levels. To better understand this issue, we introduce a theoretical connection between the posterior uncertainty of the state estimate and the certificate matrix obtained via convex relaxation. With this connection in mind, we empirically explore the factors that contribute to this loss of tightness and demonstrate that redundant constraints can be used to regain it. As a second technical contribution of this paper, we show that the state-of-the-art relaxation of scalar-weighted SLAM cannot be used when matrix weights are considered. We provide an alternate formulation and show that its SDP relaxation is not tight (even for very low noise levels) unless specific redundant constraints are used. We demonstrate the tightness of our formulations on both simulated and real-world data. 


