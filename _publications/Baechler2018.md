---
layout: publication
categories: Conference
ref-authors:
- G. Baechler*
- "F. D\xFCmbgen*"
- "G. Elhami*"
- "M. Krekovic*"
- R. Scheibler
- A. Scholefield
- M. Vetterli
ref-journal: IEEE International Conference on Acoustics, Speech and Signal Processing
  (ICASSP)
ref-link: https://doi.org/10.1109/ICASSP.2018.8462441
ref-year: 2018
ref-code: https://github.com/lcav/localization-icassp2018
title: Combining range and direction for improved localization
image: icassp18.jpg
summary: "Extend concepts from Euclidean Distance Matrices, created for distance (range) measurements only, to angle (direction) measurements, to enable estimating locations from a mixture of range and direction measurements."
---


Self-localization of nodes in a sensor network is typically achieved using either range or direction measurements; in this paper, we show that a constructive combination of both improves the estimation. We propose two localization algorithms that make use of the differences between the sensors' coordinates, or edge vectors; these can be calculated from measured distances and angles. Our first method improves the existing edge-multidimensional scaling algorithm (E- MDS) by introducing additional constraints that enforce geometric consistency between the edge vectors. On the other hand, our second method decomposes the edge vectors onto 1-dimensional spaces and introduces the concept of coordinate difference matrices (CDMs) to independently regularize each projection. This solution is optimal when Gaussian noise is added to the edge vectors. We demonstrate in numerical simulations that both algorithms outperform state-of-the-art solutions.
