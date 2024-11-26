---
layout: publication
categories: Other
ref-authors:
- W. Talbot
- J. Nubert
- T. Tuna
- C. Cadena
- "F. D\xFCmbgen"
- J. Tordesillas
- T. D. Barfoot
- M. Hutter
ref-journal: 'under review'
arxiv-link: https://doi.org/10.48550/arXiv.2411.03951
ref-year: 2024
title: 'Continuous-Time State Estimation Methods in Robotics: A Survey'
image: cont-time.png
summary: "An up-to-date overview of works in robotics solving for continuous representations of trajectories (in time) rather than at discrete measurements only, with a focus on spline-based and Gaussian-Process-based methods."  
---

Accurate, efficient, and robust state estimation is more important than ever in robotics as the variety of platforms and complexity of tasks continue to grow. Historically, discrete-time filters and smoothers have been the dominant approach, in which the estimated variables are states at discrete sample times. The paradigm of continuous-time state estimation proposes an alternative strategy by estimating variables that express the state as a continuous function of time, which can be evaluated at any query time. Not only can this benefit downstream tasks such as planning and control, but it also significantly increases estimator performance and flexibility, as well as reduces sensor preprocessing and interfacing complexity. Despite this, continuous-time methods remain underutilized, potentially because they are less well-known within robotics. To remedy this, this work presents a unifying formulation of these methods and the most exhaustive literature review to date, systematically categorizing prior work by methodology, application, state variables, historical context, and theoretical contribution to the field. By surveying splines and Gaussian processes together and contextualizing works from other research domains, this work identifies and analyzes open problems in continuous-time state estimation and suggests new research directions. 
