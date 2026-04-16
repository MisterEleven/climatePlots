import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator
from datetime import datetime, timedelta
from matplotlib.gridspec import GridSpec
from matplotlib.collections import LineCollection
import matplotlib.patches as mpatches

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

# Comfort parameters
temp_comfort = (22, 26)
relh_comfort = (30, 60)

# Create datetime array
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(hours=i) for i in range(len(op_temp))]

print("\n" + "="*70)
print("CREATING CREATIVE & UNCOMMON VISUALIZATIONS")
print("="*70 + "\n")

# ===== FIGURE 1: RIPPLE PLOTS & STREAM GRAPHS =====
fig1 = plt.figure(figsize=(20, 12))
fig1.suptitle('Ripple & Flow Visualizations', fontsize=18, fontweight='bold', y=0.98)

gs1 = GridSpec(3, 2, figure=fig1, hspace=0.4, wspace=0.3)

# RIPPLE PLOT 1: Temperature waves
ax1 = fig1.add_subplot(gs1[0, :])
# Create ripple effect by showing daily patterns
days_to_show = 30
hours_per_day = 24
for day in range(days_to_show):
    start_idx = day * hours_per_day
    end_idx = start_idx + hours_per_day
    if end_idx <= len(op_temp):
        hours = np.arange(hours_per_day)
        temps = op_temp[start_idx:end_idx]
        # Create ripple effect with offset and alpha
        offset = day * 0.5
        alpha = 1.0 - (day / days_to_show) * 0.7
        color = plt.cm.coolwarm((np.mean(temps) - min(op_temp)) / (max(op_temp) - min(op_temp)))
        ax1.plot(hours, np.array(temps) + offset, alpha=alpha, linewidth=2, color=color)
        ax1.fill_between(hours, offset, np.array(temps) + offset, alpha=0.1, color=color)

ax1.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
ax1.set_ylabel('Temperature (°C) + Day Offset', fontsize=12, fontweight='bold')
ax1.set_title('Temperature Ripple Plot - First 30 Days', fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(0, 23)

# RIDGELINE PLOT: Monthly temperature distributions
ax2 = fig1.add_subplot(gs1[1, 0])
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
for month_idx in range(12):
    month_data = [op_temp[i] for i in range(len(op_temp)) if dates[i].month == month_idx + 1]
    if month_data:
        # Create density estimation
        hist, bins = np.histogram(month_data, bins=30, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        # Scale and offset
        hist_scaled = hist * 3 + month_idx * 0.8
        color = plt.cm.viridis(month_idx / 11)
        ax2.fill_between(bin_centers, month_idx * 0.8, hist_scaled, alpha=0.7, color=color)
        ax2.plot(bin_centers, hist_scaled, color='black', linewidth=1, alpha=0.5)

ax2.set_xlabel('Operative Temperature (°C)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Month', fontsize=11, fontweight='bold')
ax2.set_yticks(np.arange(12) * 0.8)
ax2.set_yticklabels(months)
ax2.set_title('Ridgeline Plot - Monthly Temperature Distribution', fontsize=13, fontweight='bold', pad=10)
ax2.axvspan(temp_comfort[0], temp_comfort[1], alpha=0.1, color='green', zorder=0)
ax2.grid(True, alpha=0.2, axis='x')

# RIDGELINE PLOT: Monthly humidity distributions
ax3 = fig1.add_subplot(gs1[1, 1])
for month_idx in range(12):
    month_data = [op_relh[i] for i in range(len(op_relh)) if dates[i].month == month_idx + 1]
    if month_data:
        hist, bins = np.histogram(month_data, bins=30, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        hist_scaled = hist * 8 + month_idx * 0.8
        color = plt.cm.plasma(month_idx / 11)
        ax3.fill_between(bin_centers, month_idx * 0.8, hist_scaled, alpha=0.7, color=color)
        ax3.plot(bin_centers, hist_scaled, color='black', linewidth=1, alpha=0.5)

ax3.set_xlabel('Operative Relative Humidity (%)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Month', fontsize=11, fontweight='bold')
ax3.set_yticks(np.arange(12) * 0.8)
ax3.set_yticklabels(months)
ax3.set_title('Ridgeline Plot - Monthly Humidity Distribution', fontsize=13, fontweight='bold', pad=10)
ax3.axvspan(relh_comfort[0], relh_comfort[1], alpha=0.1, color='green', zorder=0)
ax3.grid(True, alpha=0.2, axis='x')

# STREAM GRAPH: Stacked area showing comfort zones over time
ax4 = fig1.add_subplot(gs1[2, :])
# Aggregate by week
weeks = 52
hours_per_week = len(op_temp) // weeks
week_comfort = []
week_too_hot = []
week_too_cold = []
week_labels = []

for week in range(weeks):
    start_idx = week * hours_per_week
    end_idx = min(start_idx + hours_per_week, len(op_temp))
    week_temps = op_temp[start_idx:end_idx]
    
    comfort_count = sum(1 for t in week_temps if temp_comfort[0] <= t <= temp_comfort[1])
    too_hot_count = sum(1 for t in week_temps if t > temp_comfort[1])
    too_cold_count = sum(1 for t in week_temps if t < temp_comfort[0])
    
    week_comfort.append(comfort_count)
    week_too_hot.append(too_hot_count)
    week_too_cold.append(too_cold_count)
    week_labels.append(week + 1)

# Create stream graph
ax4.fill_between(week_labels, 0, week_too_cold, alpha=0.7, color='blue', label='Too Cold')
ax4.fill_between(week_labels, week_too_cold, 
                 np.array(week_too_cold) + np.array(week_comfort), 
                 alpha=0.7, color='green', label='Comfort')
ax4.fill_between(week_labels, np.array(week_too_cold) + np.array(week_comfort),
                 np.array(week_too_cold) + np.array(week_comfort) + np.array(week_too_hot),
                 alpha=0.7, color='red', label='Too Hot')

ax4.set_xlabel('Week of Year', fontsize=12, fontweight='bold')
ax4.set_ylabel('Hours', fontsize=12, fontweight='bold')
ax4.set_title('Stream Graph - Weekly Comfort Distribution', fontsize=14, fontweight='bold', pad=15)
ax4.legend(loc='upper right', fontsize=11)
ax4.grid(True, alpha=0.3, axis='y')

plt.savefig('creative_analysis_1.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: creative_analysis_1.png (Ripple & Flow Visualizations)")

# ===== FIGURE 2: POLAR & RADIAL PLOTS =====
fig2 = plt.figure(figsize=(18, 12))
fig2.suptitle('Polar & Radial Visualizations', fontsize=18, fontweight='bold', y=0.96)

gs2 = GridSpec(2, 2, figure=fig2, hspace=0.35, wspace=0.3)

# POLAR PLOT 1: Temperature by hour of day (averaged)
ax5 = fig2.add_subplot(gs2[0, 0], projection='polar')
hours_of_day = 24
avg_temp_by_hour = [np.mean([op_temp[i] for i in range(len(op_temp)) if i % 24 == h]) 
                    for h in range(hours_of_day)]
theta = np.linspace(0, 2 * np.pi, hours_of_day, endpoint=False)
radii = avg_temp_by_hour
width = 2 * np.pi / hours_of_day
colors = plt.cm.coolwarm((np.array(radii) - min(radii)) / (max(radii) - min(radii)))
bars = ax5.bar(theta, radii, width=width, bottom=0, alpha=0.8, edgecolor='black', linewidth=0.5)
for bar, color in zip(bars, colors):
    bar.set_facecolor(color)
ax5.set_theta_zero_location('N')
ax5.set_theta_direction(-1)
ax5.set_xticks(theta)
ax5.set_xticklabels([f'{h}h' for h in range(24)])
ax5.set_title('Polar Plot - Average Temperature by Hour', fontsize=13, fontweight='bold', pad=20)

# POLAR PLOT 2: Humidity by hour of day
ax6 = fig2.add_subplot(gs2[0, 1], projection='polar')
avg_relh_by_hour = [np.mean([op_relh[i] for i in range(len(op_relh)) if i % 24 == h]) 
                    for h in range(hours_of_day)]
radii2 = avg_relh_by_hour
colors2 = plt.cm.Blues((np.array(radii2) - min(radii2)) / (max(radii2) - min(radii2)))
bars2 = ax6.bar(theta, radii2, width=width, bottom=0, alpha=0.8, edgecolor='black', linewidth=0.5)
for bar, color in zip(bars2, colors2):
    bar.set_facecolor(color)
ax6.set_theta_zero_location('N')
ax6.set_theta_direction(-1)
ax6.set_xticks(theta)
ax6.set_xticklabels([f'{h}h' for h in range(24)])
ax6.set_title('Polar Plot - Average Humidity by Hour', fontsize=13, fontweight='bold', pad=20)

# RADIAL PLOT: Monthly comfort analysis
ax7 = fig2.add_subplot(gs2[1, 0], projection='polar')
months_count = 12
theta_months = np.linspace(0, 2 * np.pi, months_count, endpoint=False)
comfort_by_month = []
for month in range(1, 13):
    month_temps = [op_temp[i] for i in range(len(op_temp)) if dates[i].month == month]
    month_relh = [op_relh[i] for i in range(len(op_relh)) if dates[i].month == month]
    comfort_count = sum(1 for i in range(len(month_temps)) 
                       if temp_comfort[0] <= month_temps[i] <= temp_comfort[1] 
                       and relh_comfort[0] <= month_relh[i] <= relh_comfort[1])
    comfort_pct = (comfort_count / len(month_temps)) * 100 if month_temps else 0
    comfort_by_month.append(comfort_pct)

width_months = 2 * np.pi / months_count
colors_months = plt.cm.RdYlGn(np.array(comfort_by_month) / 100)
bars3 = ax7.bar(theta_months, comfort_by_month, width=width_months, bottom=0, 
                alpha=0.8, edgecolor='black', linewidth=1)
for bar, color in zip(bars3, colors_months):
    bar.set_facecolor(color)
ax7.set_theta_zero_location('N')
ax7.set_theta_direction(-1)
ax7.set_xticks(theta_months)
ax7.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax7.set_ylim(0, 100)
ax7.set_title('Radial Plot - Monthly Comfort Percentage', fontsize=13, fontweight='bold', pad=20)

# WIND ROSE STYLE: Temperature-Humidity relationship by season
ax8 = fig2.add_subplot(gs2[1, 1], projection='polar')
# Divide into 8 directional bins based on temp-humidity combinations
n_bins = 8
theta_bins = np.linspace(0, 2 * np.pi, n_bins, endpoint=False)
bin_counts = [0] * n_bins

for i in range(len(op_temp)):
    # Map temp and humidity to angle
    temp_norm = (op_temp[i] - min(op_temp)) / (max(op_temp) - min(op_temp))
    relh_norm = (op_relh[i] - min(op_relh)) / (max(op_relh) - min(op_relh))
    angle = np.arctan2(relh_norm - 0.5, temp_norm - 0.5) + np.pi
    bin_idx = int((angle / (2 * np.pi)) * n_bins) % n_bins
    bin_counts[bin_idx] += 1

width_bins = 2 * np.pi / n_bins
colors_bins = plt.cm.viridis(np.array(bin_counts) / max(bin_counts))
bars4 = ax8.bar(theta_bins, bin_counts, width=width_bins, bottom=0, 
                alpha=0.8, edgecolor='black', linewidth=1)
for bar, color in zip(bars4, colors_bins):
    bar.set_facecolor(color)
ax8.set_theta_zero_location('N')
ax8.set_theta_direction(-1)
ax8.set_title('Wind Rose Style - Temp-Humidity Distribution', fontsize=13, fontweight='bold', pad=20)

plt.savefig('creative_analysis_2.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: creative_analysis_2.png (Polar & Radial Visualizations)")

# ===== FIGURE 3: PARALLEL COORDINATES & SANKEY-STYLE =====
fig3 = plt.figure(figsize=(18, 10))
fig3.suptitle('Parallel Coordinates & Flow Diagrams', fontsize=18, fontweight='bold', y=0.96)

gs3 = GridSpec(2, 1, figure=fig3, hspace=0.4)

# PARALLEL COORDINATES: Sample of data points
ax9 = fig3.add_subplot(gs3[0, 0])
# Sample every 100th point for clarity
sample_indices = list(range(0, len(op_temp), 100))
n_samples = len(sample_indices)

# Normalize data for parallel coordinates
out_temp_norm = [(out_temp[i] - min(out_temp)) / (max(out_temp) - min(out_temp)) 
                 for i in sample_indices]
op_temp_norm = [(op_temp[i] - min(op_temp)) / (max(op_temp) - min(op_temp)) 
                for i in sample_indices]
out_relh_norm = [(out_relh[i] - min(out_relh)) / (max(out_relh) - min(out_relh)) 
                 for i in sample_indices]
op_relh_norm = [(op_relh[i] - min(op_relh)) / (max(op_relh) - min(op_relh)) 
                for i in sample_indices]

x_positions = [0, 1, 2, 3]
for i in range(n_samples):
    y_values = [out_temp_norm[i], op_temp_norm[i], out_relh_norm[i], op_relh_norm[i]]
    # Color by comfort status
    temp_ok = temp_comfort[0] <= op_temp[sample_indices[i]] <= temp_comfort[1]
    relh_ok = relh_comfort[0] <= op_relh[sample_indices[i]] <= relh_comfort[1]
    color = 'green' if (temp_ok and relh_ok) else 'red'
    alpha = 0.3 if (temp_ok and relh_ok) else 0.2
    ax9.plot(x_positions, y_values, color=color, alpha=alpha, linewidth=0.5)

ax9.set_xticks(x_positions)
ax9.set_xticklabels(['Outdoor\nTemp', 'Operative\nTemp', 'Outdoor\nHumidity', 'Operative\nHumidity'],
                    fontsize=11, fontweight='bold')
ax9.set_ylabel('Normalized Value (0-1)', fontsize=11, fontweight='bold')
ax9.set_title('Parallel Coordinates Plot - Environmental Variables', fontsize=13, fontweight='bold', pad=15)
ax9.grid(True, alpha=0.3, axis='y')
ax9.set_ylim(-0.05, 1.05)

# Add legend
green_line = plt.Line2D([0], [0], color='green', linewidth=2, alpha=0.7, label='Comfort')
red_line = plt.Line2D([0], [0], color='red', linewidth=2, alpha=0.7, label='Discomfort')
ax9.legend(handles=[green_line, red_line], loc='upper right', fontsize=10)

# CHORD DIAGRAM STYLE: Correlation visualization
ax10 = fig3.add_subplot(gs3[1, 0])

# Calculate correlations
corr_out_temp_op_temp = np.corrcoef(out_temp, op_temp)[0, 1]
corr_out_temp_op_relh = np.corrcoef(out_temp, op_relh)[0, 1]
corr_out_relh_op_temp = np.corrcoef(out_relh, op_temp)[0, 1]
corr_out_relh_op_relh = np.corrcoef(out_relh, op_relh)[0, 1]

# Create matrix visualization
variables = ['Out Temp', 'Out RH', 'Op Temp', 'Op RH']
corr_matrix = np.array([
    [1.0, np.corrcoef(out_temp, out_relh)[0, 1], corr_out_temp_op_temp, corr_out_temp_op_relh],
    [np.corrcoef(out_temp, out_relh)[0, 1], 1.0, corr_out_relh_op_temp, corr_out_relh_op_relh],
    [corr_out_temp_op_temp, corr_out_relh_op_temp, 1.0, np.corrcoef(op_temp, op_relh)[0, 1]],
    [corr_out_temp_op_relh, corr_out_relh_op_relh, np.corrcoef(op_temp, op_relh)[0, 1], 1.0]
])

im = ax10.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
ax10.set_xticks(range(4))
ax10.set_yticks(range(4))
ax10.set_xticklabels(variables, fontsize=11, fontweight='bold')
ax10.set_yticklabels(variables, fontsize=11, fontweight='bold')
ax10.set_title('Correlation Matrix Heatmap', fontsize=13, fontweight='bold', pad=15)

# Add correlation values
for i in range(4):
    for j in range(4):
        text = ax10.text(j, i, f'{corr_matrix[i, j]:.2f}',
                        ha="center", va="center", color="black", fontsize=10, fontweight='bold')

cbar = plt.colorbar(im, ax=ax10, pad=0.02)
cbar.set_label('Correlation Coefficient', fontsize=10)

plt.savefig('creative_analysis_3.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: creative_analysis_3.png (Parallel Coordinates & Correlations)")

print("\n" + "="*70)
print("ALL CREATIVE VISUALIZATIONS COMPLETED!")
print("="*70)
print("\nGenerated files:")
print("  • creative_analysis_1.png - Ripple & Flow Visualizations")
print("  • creative_analysis_2.png - Polar & Radial Visualizations")
print("  • creative_analysis_3.png - Parallel Coordinates & Correlations")
print("="*70 + "\n")

plt.show()

# Made with Bob
