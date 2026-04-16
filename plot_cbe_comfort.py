import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib.gridspec import GridSpec
import requests
import json

# ===== CONFIGURATION =====
# Adjust this value to change how many points are analyzed
# Lower values = more points analyzed (slower but more accurate)
# Higher values = fewer points analyzed (faster but less detailed)
# Examples: 1 = all points, 10 = every 10th point, 100 = every 100th point
SAMPLING_RATE = 1  # Change this value to adjust number of points

# Comfort calculation parameters (adjust based on your scenario)
METABOLIC_RATE = 1.2    # 1.0 = seated, 1.2 = light office work, 1.6 = standing/walking
CLOTHING_INSULATION = 0.5  # 0.5 = summer clothing, 1.0 = winter clothing
AIR_VELOCITY = 0.1      # m/s - typical indoor air movement

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10

# Read all data
with open('op-temp', 'r') as f:
    op_temp = [float(line.strip()) for line in f.readlines()[1:]]
with open('out-temp', 'r') as f:
    out_temp = [float(line.strip()) for line in f.readlines()[1:]]
with open('op-relh', 'r') as f:
    op_relh = [float(line.strip()) for line in f.readlines()[1:]]
with open('out-relh', 'r') as f:
    out_relh = [float(line.strip()) for line in f.readlines()[1:]]

# Create datetime array
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(hours=i) for i in range(len(op_temp))]

print("\n" + "="*80)
print("CBE THERMAL COMFORT TOOL ANALYSIS")
print("="*80 + "\n")

# CBE Thermal Comfort Tool API endpoint
CBE_API_URL = "https://comfort.cbe.berkeley.edu/api/pmv"


def calculate_pmv_comfort(tdb, rh, met=1.2, clo=0.5, v=0.1):
    """
    Calculate PMV and comfort using CBE API
    tdb: dry bulb temperature (°C)
    rh: relative humidity (%)
    met: metabolic rate
    clo: clothing insulation
    v: air velocity (m/s)
    """
    try:
        # Prepare request parameters
        params = {
            'tdb': tdb,
            'tr': tdb,  # Assuming mean radiant temp equals air temp
            'rh': rh,
            'met': met,
            'clo': clo,
            'v': v,
            'wme': 0
        }
        
        # Make API request
        response = requests.get(CBE_API_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'pmv': data.get('pmv', None),
                'ppd': data.get('ppd', None),
                'comfort': data.get('comfort_category', 'unknown')
            }
        else:
            return None
    except Exception as e:
        return None

# Sample data for analysis based on SAMPLING_RATE
sample_indices = list(range(0, len(op_temp), SAMPLING_RATE))
print(f"Analyzing {len(sample_indices)} sampled points (every {SAMPLING_RATE}th point)...")
print(f"Total data points available: {len(op_temp)}")
print(f"Sampling rate: 1 in {SAMPLING_RATE} points")

def simplified_pmv(tdb, rh, met=1.2, clo=0.5):
    """
    Simplified PMV estimation based on temperature and humidity
    This is an approximation - real PMV uses complex heat balance equations
    """
    # Optimal temperature for comfort (can vary with clothing and activity)
    optimal_temp = 22 + (clo * 2)  # Adjust optimal temp based on clothing
    temp_deviation = tdb - optimal_temp
    
    # Adjust for humidity (simplified)
    rh_factor = (rh - 50) / 100  # Deviation from 50% RH
    
    # Simplified PMV calculation
    # Real PMV considers: metabolic rate, clothing, air temp, radiant temp,
    # air velocity, and humidity
    pmv = (temp_deviation * 0.3) + (rh_factor * 0.15)
    
    # Simplified PPD calculation based on PMV
    # Fanger's equation: PPD = 100 - 95*exp(-0.03353*PMV^4 - 0.2179*PMV^2)
    ppd = 100 - 95 * np.exp(-0.03353 * pmv**4 - 0.2179 * pmv**2)
    ppd = max(5, min(100, ppd))  # PPD is minimum 5% even at PMV=0
    
    return pmv, ppd

print("Using simplified PMV calculation (based on Fanger's model)...")

pmv_values = []
ppd_values = []
comfort_categories = []
sample_temps = []
sample_rh = []

for i, idx in enumerate(sample_indices):
    pmv, ppd = simplified_pmv(op_temp[idx], op_relh[idx])
    pmv_values.append(pmv)
    ppd_values.append(ppd)
    sample_temps.append(op_temp[idx])
    sample_rh.append(op_relh[idx])
    
    # Categorize comfort based on ASHRAE 55 standards
    if -0.5 <= pmv <= 0.5:
        comfort_categories.append('comfortable')
    elif -1.0 <= pmv <= 1.0:
        comfort_categories.append('acceptable')
    else:
        comfort_categories.append('uncomfortable')
    
    # Print progress
    if (i + 1) % 20 == 0:
        print(f"  Processed {i + 1}/{len(sample_indices)} points...")

print(f"\n✓ Successfully analyzed {len(pmv_values)} data points")

# ===== CREATE COMPREHENSIVE COMFORT ANALYSIS PLOTS =====
fig = plt.figure(figsize=(20, 14))
fig.suptitle('CBE Thermal Comfort Analysis - PMV & ASHRAE 55', 
             fontsize=20, fontweight='bold', y=0.98)

gs = GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)

# ===== PLOT 1: PMV Distribution =====
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(pmv_values, bins=30, alpha=0.7, color='steelblue', edgecolor='black', linewidth=1)
ax1.axvspan(-0.5, 0.5, alpha=0.2, color='green', label='ASHRAE 55 Comfort (-0.5 to +0.5)')
ax1.axvspan(-1.0, -0.5, alpha=0.15, color='yellow')
ax1.axvspan(0.5, 1.0, alpha=0.15, color='yellow', label='Acceptable (-1.0 to +1.0)')
ax1.axvline(0, color='red', linestyle='--', linewidth=2, label='Neutral (PMV=0)')
ax1.set_xlabel('PMV (Predicted Mean Vote)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax1.set_title('PMV Distribution', fontsize=13, fontweight='bold', pad=10)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3, axis='y')

# ===== PLOT 2: PPD Distribution =====
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(ppd_values, bins=30, alpha=0.7, color='coral', edgecolor='black', linewidth=1)
ax2.axvline(10, color='green', linestyle='--', linewidth=2, label='ASHRAE 55 Limit (10%)')
ax2.axvline(20, color='orange', linestyle='--', linewidth=2, label='Extended Limit (20%)')
ax2.set_xlabel('PPD (Predicted Percentage Dissatisfied) %', fontsize=11, fontweight='bold')
ax2.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax2.set_title('PPD Distribution', fontsize=13, fontweight='bold', pad=10)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3, axis='y')

# ===== PLOT 3: Comfort Categories Pie Chart =====
ax3 = fig.add_subplot(gs[0, 2])
comfort_counts = {
    'comfortable': comfort_categories.count('comfortable'),
    'acceptable': comfort_categories.count('acceptable'),
    'uncomfortable': len(comfort_categories) - comfort_categories.count('comfortable') - comfort_categories.count('acceptable')
}
colors_pie = ['#90EE90', '#FFD700', '#FFB6C6']
labels_pie = [f'Comfortable\n({comfort_counts["comfortable"]} pts)', 
              f'Acceptable\n({comfort_counts["acceptable"]} pts)',
              f'Uncomfortable\n({comfort_counts["uncomfortable"]} pts)']
wedges, texts, autotexts = ax3.pie(comfort_counts.values(), labels=labels_pie, colors=colors_pie,
                                     autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontweight('bold')
ax3.set_title('Comfort Categories', fontsize=13, fontweight='bold', pad=10)

# ===== PLOT 4: PMV vs Temperature =====
ax4 = fig.add_subplot(gs[1, 0])
scatter = ax4.scatter(sample_temps, pmv_values, c=pmv_values, cmap='RdYlGn_r', 
                     alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
ax4.axhspan(-0.5, 0.5, alpha=0.15, color='green', zorder=0)
ax4.axhline(0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax4.set_xlabel('Operative Temperature (°C)', fontsize=11, fontweight='bold')
ax4.set_ylabel('PMV', fontsize=11, fontweight='bold')
ax4.set_title('PMV vs Operative Temperature', fontsize=13, fontweight='bold', pad=10)
ax4.grid(True, alpha=0.3)
cbar = plt.colorbar(scatter, ax=ax4)
cbar.set_label('PMV', fontsize=9)

# ===== PLOT 5: PMV vs Humidity =====
ax5 = fig.add_subplot(gs[1, 1])
scatter2 = ax5.scatter(sample_rh, pmv_values, c=pmv_values, cmap='RdYlGn_r', 
                      alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
ax5.axhspan(-0.5, 0.5, alpha=0.15, color='green', zorder=0)
ax5.axhline(0, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
ax5.set_xlabel('Operative Relative Humidity (%)', fontsize=11, fontweight='bold')
ax5.set_ylabel('PMV', fontsize=11, fontweight='bold')
ax5.set_title('PMV vs Relative Humidity', fontsize=13, fontweight='bold', pad=10)
ax5.grid(True, alpha=0.3)
cbar2 = plt.colorbar(scatter2, ax=ax5)
cbar2.set_label('PMV', fontsize=9)

# ===== PLOT 6: ASHRAE 55 Comfort Zone =====
ax6 = fig.add_subplot(gs[1, 2])
# Color points by comfort category
colors_scatter = []
for cat in comfort_categories:
    if cat == 'comfortable':
        colors_scatter.append('green')
    elif cat == 'acceptable':
        colors_scatter.append('yellow')
    else:
        colors_scatter.append('red')

ax6.scatter(sample_temps, sample_rh, c=colors_scatter, alpha=0.5, s=20, edgecolors='black', linewidth=0.3)
# Add ASHRAE 55 comfort zone approximation
comfort_temp_range = [20, 27]
comfort_rh_range = [30, 60]
rect = plt.Rectangle((comfort_temp_range[0], comfort_rh_range[0]), 
                     comfort_temp_range[1] - comfort_temp_range[0],
                     comfort_rh_range[1] - comfort_rh_range[0],
                     fill=False, edgecolor='green', linewidth=3, linestyle='--',
                     label='Typical Comfort Zone')
ax6.add_patch(rect)
ax6.set_xlabel('Operative Temperature (°C)', fontsize=11, fontweight='bold')
ax6.set_ylabel('Relative Humidity (%)', fontsize=11, fontweight='bold')
ax6.set_title('ASHRAE 55 Comfort Zone', fontsize=13, fontweight='bold', pad=10)
ax6.legend(fontsize=9)
ax6.grid(True, alpha=0.3)

# ===== PLOT 7: PMV Time Series (sampled) =====
ax7 = fig.add_subplot(gs[2, :])
sample_dates = [dates[i] for i in sample_indices[:len(pmv_values)]]
# Color code by comfort
for i in range(len(pmv_values) - 1):
    if -0.5 <= pmv_values[i] <= 0.5:
        color = 'green'
    elif -1.0 <= pmv_values[i] <= 1.0:
        color = 'yellow'
    else:
        color = 'red'
    ax7.plot([sample_dates[i], sample_dates[i+1]], [pmv_values[i], pmv_values[i+1]], 
            color=color, linewidth=2, alpha=0.7)

ax7.axhspan(-0.5, 0.5, alpha=0.15, color='green', label='Comfortable', zorder=0)
ax7.axhspan(-1.0, -0.5, alpha=0.1, color='yellow', zorder=0)
ax7.axhspan(0.5, 1.0, alpha=0.1, color='yellow', label='Acceptable', zorder=0)
ax7.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax7.set_xlabel('Date', fontsize=12, fontweight='bold')
ax7.set_ylabel('PMV', fontsize=12, fontweight='bold')
ax7.set_title('PMV Time Series (Sampled Data)', fontsize=14, fontweight='bold', pad=15)
ax7.legend(fontsize=10)
ax7.grid(True, alpha=0.3)

# Format x-axis
from matplotlib.dates import MonthLocator, DateFormatter
ax7.xaxis.set_major_locator(MonthLocator())
ax7.xaxis.set_major_formatter(DateFormatter('%b'))

# Save figure
plt.savefig('cbe_comfort_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
print("\n✓ Saved: cbe_comfort_analysis.png")

# Print summary statistics
print("\n" + "="*80)
print("COMFORT ANALYSIS SUMMARY")
print("="*80)
print(f"Total sampled points: {len(pmv_values)}")
print(f"\nPMV Statistics:")
print(f"  Mean PMV: {np.mean(pmv_values):.3f}")
print(f"  Std Dev: {np.std(pmv_values):.3f}")
print(f"  Min PMV: {np.min(pmv_values):.3f}")
print(f"  Max PMV: {np.max(pmv_values):.3f}")
print(f"\nPPD Statistics:")
print(f"  Mean PPD: {np.mean(ppd_values):.1f}%")
print(f"  Min PPD: {np.min(ppd_values):.1f}%")
print(f"  Max PPD: {np.max(ppd_values):.1f}%")
print(f"\nComfort Categories:")
print(f"  Comfortable (PMV -0.5 to +0.5): {comfort_counts['comfortable']} ({comfort_counts['comfortable']/len(pmv_values)*100:.1f}%)")
print(f"  Acceptable (PMV -1.0 to +1.0): {comfort_counts['acceptable']} ({comfort_counts['acceptable']/len(pmv_values)*100:.1f}%)")
print(f"  Uncomfortable: {comfort_counts['uncomfortable']} ({comfort_counts['uncomfortable']/len(pmv_values)*100:.1f}%)")
print("="*80 + "\n")

plt.show()

# Made with Bob
