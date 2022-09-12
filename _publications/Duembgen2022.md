---
layout: publication
categories: Journal
ref-authors:
- F. Dümbgen
- A. Hoffet
- M. Mihailo Kolundžija
- A. Scholefield 
- M. Vetterli
ref-journal: IEEE Robotics and Automation Letters 
ref-link: https://ieeexplore.ieee.org/document/9844245
ref-year: 2022
ref-code: https://github.com/lcav/audioROS
title: "Blind as a Bat: Audible Echolocation on Small Robots"
image: drone-epuck.jpg
---

For safe and efficient operation, mobile robots need
to perceive their environment, and in particular, perform tasks
such as obstacle detection, localization, and mapping. Although
robots are often equipped with microphones and speakers, the
audio modality is rarely used for these tasks. Compared to the
localization of sound sources, for which many practical solutions
exist, algorithms for active echolocation are less developed and
often rely on hardware requirements that are out of reach for
small robots.

We propose an end-to-end pipeline for sound-based localization and mapping that is targeted at, but not limited to, robots equipped with only simple buzzers and low-end microphones.
The method is model-based, runs in real time, and requires no
prior calibration or training. We successfully test the algorithm
on the e-puck robot with its integrated audio hardware, and on
the Crazyflie drone, for which we design a reproducible audio
extension deck. We achieve centimeter-level wall localization on
both platforms when the robots are static during the measurement process. Even in the more challenging setting of a flying drone, we can successfully localize walls, which we demonstrate
in a proof-of-concept multi-wall localization and mapping demo
