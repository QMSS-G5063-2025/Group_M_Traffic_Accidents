# NYC Traffic Collision Dashboard

This is an interactive Streamlit web application for visualizing and analyzing traffic collision data in New York City. The dashboard provides geographic, categorical, and fatality-based insights into traffic incidents using heatmaps, pie charts, and bar charts.

## Project Objectives

The purpose of this project is to:

- Visualize the spatial distribution of traffic collisions across NYC boroughs
- Analyze the most common causes of collisions
- Break down the number of fatalities by type (pedestrians, cyclists, motorists)
- Practice building and deploying an interactive Streamlit dashboard

## Features

### 1. Interactive Hexagon Heatmap
- Based on **latitude/longitude** coordinates of each crash
- Users can select a specific **borough** or analyze **all NYC**
- Map powered by **PyDeck** and Mapbox

### 2. Accident Cause Analysis
- Pie chart: shows proportional breakdown of top 5 collision causes
- Bar chart: shows count of each cause
- Data is filtered dynamically based on selected borough

### 3. Fatality Breakdown
- Pie chart: visualizes share of fatalities among pedestrians, cyclists, motorists
- Bar chart: compares absolute counts of each fatality type

---

How to Run
1. Clone or download this repository
2. Install required packages
