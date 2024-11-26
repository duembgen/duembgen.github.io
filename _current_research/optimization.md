---
title: Global optimization for robotics with unknown models
image: unknown_models.png
date: 2024-11-26
categories: past
--- 

Recent work in robotics has shown that many classical state estimation problems can be formulated as polynomial problems with *tight* semidefinite relaxations. This means that the global minimum can often be found by just solving one convex problem (usually a semidefinite program). I have explored instances of this methodology in past and ongoing research, described in the section below.

In this research project, I am exploring two follow-up questions. First, how can we find globally optimal solutions to problems where the model may be inaccurate, only partially (or not at all) known, or when we have no tractable state representation (think cloth or grains)? Answering this question will unlock many new application areas for globally optimal methods; including planning through contact, safe control of poorly calibrated systems, and efficient manipulation of soft and uncountable objects. Second, I explore how to learn optimal models from data; using ingredients such as differentiable optimization to find models that are adapted to the task of interest. This research directly spawns many interesting subproblems, such as active perception to learn models from less data, online adaptation of model estimates, and their global optimality.   
