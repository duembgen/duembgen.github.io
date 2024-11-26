---
layout: publication
categories: Conference
ref-authors:
- "F. D\xFCmbgen"
- C. Oeschger
- M. Kolundzija
- A. Scholefield
- E. Girardin
- J. Leuenberger
- S. Ayer
ref-journal: International Conference on Indoor Positioning and Indoor Navigation
  (IPIN)
ref-link: https://doi.org/10.1109/IPIN.2019.8911765
ref-year: 2019
title: Multi-Modal Probabilistic Indoor Localization on a Smartphone
image: ipin2.jpg
note: Shortlisted for best student paper award
summary: "Combine Bluetooth signal-strength, WiFi round-trip-time measurements, and an IMU with an auto-calibration scheme whenever known landmarks are observed by the camera to obtain a location probability map of a smartphone's location in an indoor environment." 
---

The satellite-based Global Positioning System (GPS) provides robust localization on smartphones outdoors. In indoor environments, however, no system is close to achieving a similar level of ubiquity, with existing solutions offering different trade-offs in terms of accuracy, robustness and cost. In this paper, we develop a multi-modal positioning system, targeted at smartphones, which aims to get the best out of each of its constituent modalities. More precisely, we combine Bluetooth low energy (BLE) beacons, round-trip-time (RTT) enabled WiFi access points and the smartphone's inertial measurement unit (IMU) to provide a cheap robust localization system that, unlike fingerprinting methods, requires no pre-training. To do this, we use a probabilistic algorithm based on a conditional random field (CRF). We show how to incorporate sparse visual information to improve the accuracy of our system, using pose estimation from pre-scanned visual landmarks, to calibrate the system online. Our method achieves an accuracy of around 2 meters on two realistic datasets, outperforming other distance-based localization approaches. We also compare our approach with an ultra-wideband (UWB) system. While we do not match the performance of UWB, our system is cheap, smartphone compatible and provides satisfactory performance for many applications.
