# Building Environmental Data Analysis & Visualization

A comprehensive Python toolkit for analyzing and visualizing building environmental data, including temperature and relative humidity measurements. This project provides multiple visualization approaches ranging from standard plots to advanced thermal comfort analysis based on ASHRAE 55 standards.

## 📊 Overview

This repository contains scripts for analyzing 8760 hours (one full year) of building environmental data:
- **Operative Temperature** (indoor)
- **Outdoor Temperature**
- **Operative Relative Humidity** (indoor)
- **Outdoor Relative Humidity**

## 🎯 Features

### Standard Visualizations
- Scatter plots with comfort band highlighting
- Time series analysis with monthly aggregation
- Color-coded comfort zone indicators
- 3D environmental condition mapping

### Advanced Visualizations
- **Density Plots**: Hexbin distributions showing data concentration
- **Ridgeline Plots**: Monthly distribution comparisons
- **Polar Plots**: Circular hour-of-day analysis
- **Heatmaps**: Temporal patterns across the year
- **Stream Graphs**: Weekly comfort distribution flows
- **Parallel Coordinates**: Multi-variable relationship visualization

### Thermal Comfort Analysis
- PMV (Predicted Mean Vote) calculations
- PPD (Predicted Percentage Dissatisfied) analysis
- ASHRAE 55 comfort zone evaluation
- Customizable metabolic rate and clothing insulation parameters

## 📁 Project Structure

```
.
├── README.md                      # This file
├── op-temp                        # Operative temperature data (8760 hours)
├── out-temp                       # Outdoor temperature data (8760 hours)
├── op-relh                        # Operative relative humidity data (8760 hours)
├── out-relh                       # Outdoor relative humidity data (8760 hours)
├── plot_temperatures.py           # Basic temperature scatter & time series
├── plot_all_data.py              # Comprehensive 5-subplot analysis
├── plot_fancy_analysis.py        # Advanced visualizations (3 figures)
├── plot_creative_analysis.py     # Uncommon plots (ripple, polar, etc.)
├── plot_ridgeline.py             # Dedicated ridgeline plots
└── plot_cbe_comfort.py           # Thermal comfort analysis (PMV/PPD)
```

## 🚀 Getting Started

### Prerequisites

```bash
pip install matplotlib numpy requests
```

### Data Format

Each data file should contain:
- Line 1: Header (e.g., "Operative Temperature")
- Lines 2-8761: Hourly values (one per line)

Example:
```
Operative Temperature
21.324737
20.824748
...
```

## 📈 Usage

### Basic Analysis

```bash
# Temperature scatter plot with comfort bands
python3 plot_temperatures.py

# Complete analysis with all variables
python3 plot_all_data.py
```

### Advanced Visualizations

```bash
# Fancy analysis with density plots and 3D views
python3 plot_fancy_analysis.py

# Creative visualizations (ripple, polar, stream graphs)
python3 plot_creative_analysis.py

# Ridgeline plots for all variables
python3 plot_ridgeline.py
```

### Thermal Comfort Analysis

```bash
# PMV/PPD analysis based on ASHRAE 55
python3 plot_cbe_comfort.py
```

#### Customizing Comfort Analysis

Edit the configuration section in `plot_cbe_comfort.py`:

```python
# Adjust sampling rate (1 = all points, 100 = every 100th point)
SAMPLING_RATE = 100

# Comfort parameters
METABOLIC_RATE = 1.2        # 1.0 = seated, 1.2 = office work
CLOTHING_INSULATION = 0.5   # 0.5 = summer, 1.0 = winter
AIR_VELOCITY = 0.1          # m/s
```

## 🎨 Output Files

Each script generates high-resolution PNG files:

| Script | Output File(s) | Description |
|--------|---------------|-------------|
| `plot_temperatures.py` | `temperature_plots.png` | Basic scatter & time series |
| `plot_all_data.py` | `complete_analysis.png` | 5-subplot comprehensive view |
| `plot_fancy_analysis.py` | `fancy_analysis_1.png`<br>`fancy_analysis_2.png`<br>`fancy_analysis_3.png` | Density plots, 3D views, heatmaps |
| `plot_creative_analysis.py` | `creative_analysis_1.png`<br>`creative_analysis_2.png`<br>`creative_analysis_3.png` | Ripple, polar, parallel coordinates |
| `plot_ridgeline.py` | `ridgeline_plots.png` | Monthly distribution ridgelines |
| `plot_cbe_comfort.py` | `cbe_comfort_analysis.png` | PMV/PPD thermal comfort analysis |

All images are saved at 300 DPI for publication quality.

## 🌡️ Comfort Standards

### Temperature Comfort Band
- **Range**: 22-26°C
- **Standard**: Typical thermal comfort zone
- **Visualization**: Green shaded areas in plots

### Relative Humidity Comfort Band
- **Range**: 30-60%
- **Standard**: Recommended indoor humidity levels
- **Visualization**: Green shaded areas in plots

### PMV (Predicted Mean Vote)
- **Comfortable**: -0.5 to +0.5
- **Acceptable**: -1.0 to +1.0
- **Scale**: -3 (cold) to +3 (hot)

### PPD (Predicted Percentage Dissatisfied)
- **ASHRAE 55 Limit**: ≤10%
- **Extended Limit**: ≤20%

## 📊 Visualization Types

### 1. Scatter Plots
- Outdoor vs operative conditions
- Color-coded by comfort status
- Comfort zones highlighted

### 2. Time Series
- Hourly data throughout the year
- Color-coded comfort indicators
- Monthly x-axis labels

### 3. Density Plots (Hexbin)
- Data concentration visualization
- Color gradients showing frequency
- Comfort zones overlaid

### 4. Ridgeline Plots
- Monthly distribution comparisons
- Stacked density curves
- Easy seasonal pattern identification

### 5. Polar Plots
- Hour-of-day circular analysis
- Radial comfort percentages
- Wind rose style distributions

### 6. Heatmaps
- Day-of-year vs hour-of-day
- Temperature/humidity patterns
- Temporal trend identification

### 7. 3D Visualizations
- Multi-variable relationships
- Comfort zone volumes
- Interactive viewing angles

### 8. Stream Graphs
- Weekly comfort distribution flows
- Stacked area charts
- Temporal comfort trends

## 🔧 Customization

### Adjusting Comfort Zones

Edit the comfort parameters in any script:

```python
temp_comfort = (22, 26)      # Temperature range in °C
relh_comfort = (30, 60)      # Humidity range in %
```

### Changing Plot Styles

Modify the matplotlib style:

```python
plt.style.use('seaborn-v0_8-darkgrid')  # or 'ggplot', 'bmh', etc.
```

### Color Schemes

Change colormaps for different visualizations:

```python
cmap='YlOrRd'    # Yellow-Orange-Red
cmap='Blues'     # Blue gradient
cmap='viridis'   # Perceptually uniform
cmap='RdYlGn'    # Red-Yellow-Green
```

## 📝 Notes

- All timestamps assume data starts on January 1, 2024
- Operative temperature approximates mean radiant temperature
- PMV calculations use simplified Fanger model
- For production use, consider using the full CBE Thermal Comfort Tool API

## 🤝 Contributing

Feel free to:
- Add new visualization types
- Improve comfort calculations
- Enhance data processing
- Add additional environmental parameters

## 📄 License

This project is open source and available for educational and research purposes.

## 🔗 References

- [ASHRAE Standard 55](https://www.ashrae.org/technical-resources/bookstore/standard-55-thermal-environmental-conditions-for-human-occupancy)
- [CBE Thermal Comfort Tool](https://comfort.cbe.berkeley.edu/)
- [Fanger's PMV Model](https://en.wikipedia.org/wiki/Thermal_comfort#Fanger's_thermal_comfort_model)

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Last Updated**: April 2026