# sapling_monitoring


🌱 Sapling Survival Analysis – PoC
📌 Project Overview

This project is a Proof of Concept (PoC) for estimating the survival percentage of planted saplings using drone-based orthomosaic imagery.

Two drone surveys are used:

OP1 – Baseline survey (after plantation)

OP3 – Follow-up survey (after weeding operation)

The pipeline:

Aligns OP3 imagery to OP1

Detects plantation pits from OP1

Checks sapling survival in OP3 at the same locations

Outputs:

A CSV survival report

A visual overlay image for verification

Summary statistics in the terminal

This PoC demonstrates the technical feasibility of automated sapling survival assessment using computer vision and geospatial data.

🧠 Key Features

Orthomosaic alignment using affine transformation

Automated pit detection from baseline imagery

Patch-based survival classification

Pixel-to-geographic coordinate conversion

GIS-ready CSV output

Visual validation via annotated imagery


⚠️ Important Note About Data Files

🚨 The orthomosaic .tif files are too large to be uploaded to GitHub.
As a result, they are NOT included in this repository.

👉 What you need to do:

read the instruction present in the .txt file in data folder

Required libraries:

pip install rasterio opencv-python numpy pandas


📊 Output Details
1. CSV Report (survival_report.csv)

Each row represents one detected pit:
| Column     | Description            |
| ---------- | ---------------------- |
| pit_id     | Unique pit index       |
| lat        | Latitude of pit        |
| lon        | Longitude of pit       |
| status     | Alive / Dead           |
| confidence | Model confidence score |


2. Visual Overlay (detections.png)

Green circles → Alive saplings

Red circles → Dead saplings

This image is intended for manual verification and audits.

🧪 Methodology Summary

Pits are detected from OP1 to establish baseline planting locations.

OP3 is geometrically aligned to OP1 to ensure spatial consistency.

A fixed-size image patch around each pit is extracted from OP3.

Survival is determined using computer vision / ML logic.

Results are mapped back to real-world coordinates using raster metadata.

🚧 Current Limitations (PoC Scope)

Survival logic depends on visual heuristics / ML confidence

No ground-truth accuracy validation included yet

Performance not optimized for very large areas

Assumes minimal seasonal or lighting variation

These are expected limitations for a PoC.
# sapling_monitoring
# sapling_monitoring
