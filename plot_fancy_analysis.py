import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator
from datetime import datetime, timedelta
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Set style for fancy plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'sans-serif'
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

# Calculate comfort metrics
temp_in_comfort = sum(1 for t in op_temp if temp_comfort[0] <= t <= temp_comfort[1])
relh_in_comfort = sum(1 for r in op_relh if relh_comfort[0] <= r <= relh_comfort[1])
both_in_comfort = sum(1 for i in range(len(op_temp)) 
                      if temp_comfort[0] <= op_temp[i] <= temp_comfort[1] 
                      and relh_comfort[0] <= op_relh[i] <= relh_comfort[1])

print(f"\n{'='*60}")
print(f"COMFORT ANALYSIS SUMMARY")
print(f"{'='*60}")
print(f"Total hours analyzed: {len(op_temp)}")
print(f"Temperature in comfort: {temp_in_comfort} hrs ({temp_in_comfort/len(op_temp)*100:.1f}%)")
print(f"Humidity in comfort: {relh_in_comfort} hrs ({relh_in_comfort/len(op_relh)*100:.1f}%)")
print(f"Both in comfort: {both_in_comfort} hrs ({both_in_comfort/len(op_temp)*100:.1f}%)")
print(f"{'='*60}\n")

# ===== FIGURE 1: DENSITY PLOTS WITH HEXBIN =====
fig1 = plt.figure(figsize=(18, 10))
fig1.suptitle('Environmental Conditions Density Analysis', fontsize=18, fontweight='bold', y=0.98)

gs1 = GridSpec(2, 3, figure=fig1, hspace=0.35, wspace=0.3)

# Temperature Hexbin
ax1 = fig1.add_subplot(gs1[0, 0])
hb1 = ax1.hexbin(out_temp, op_temp, gridsize=30, cmap='YlOrRd', mincnt=1, alpha=0.8)
ax1.axhspan(temp_comfort[0], temp_comfort[1], alpha=0.15, color='green', zorder=0)
ax1.set_xlabel('Outdoor Temperature (°C)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Operative Temperature (°C)', fontsize=11, fontweight='bold')
ax1.set_title('Temperature Density Distribution', fontsize=13, fontweight='bold', pad=10)
cb1 = plt.colorbar(hb1, ax=ax1)
cb1.set_label('Count', fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Humidity Hexbin
ax2 = fig1.add_subplot(gs1[0, 1])
hb2 = ax2.hexbin(out_relh, op_relh, gridsize=30, cmap='Blues', mincnt=1, alpha=0.8)
ax2.axhspan(relh_comfort[0], relh_comfort[1], alpha=0.15, color='green', zorder=0)
ax2.set_xlabel('Outdoor Rel. Humidity (%)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Operative Rel. Humidity (%)', fontsize=11, fontweight='bold')
ax2.set_title('Humidity Density Distribution', fontsize=13, fontweight='bold', pad=10)
cb2 = plt.colorbar(hb2, ax=ax2)
cb2.set_label('Count', fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Comfort Zone 2D
ax3 = fig1.add_subplot(gs1[0, 2])
comfort_colors = ['red' if not (temp_comfort[0] <= op_temp[i] <= temp_comfort[1] and 
                                relh_comfort[0] <= op_relh[i] <= relh_comfort[1])
                  else 'green' for i in range(len(op_temp))]
scatter = ax3.scatter(op_temp, op_relh, c=comfort_colors, alpha=0.3, s=3, edgecolors='none')
ax3.axvspan(temp_comfort[0], temp_comfort[1], alpha=0.1, color='green')
ax3.axhspan(relh_comfort[0], relh_comfort[1], alpha=0.1, color='green')
ax3.add_patch(mpatches.Rectangle((temp_comfort[0], relh_comfort[0]), 
                                  temp_comfort[1]-temp_comfort[0], 
                                  relh_comfort[1]-relh_comfort[0],
                                  fill=True, alpha=0.2, color='green', 
                                  label='Comfort Zone'))
ax3.set_xlabel('Operative Temperature (°C)', fontsize=11, fontweight='bold')
ax3.set_ylabel('Operative Rel. Humidity (%)', fontsize=11, fontweight='bold')
ax3.set_title('Comfort Zone Analysis', fontsize=13, fontweight='bold', pad=10)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Monthly averages - Temperature
ax4 = fig1.add_subplot(gs1[1, 0])
months = np.arange(1, 13)
monthly_op_temp = [np.mean([op_temp[i] for i in range(len(op_temp)) 
                            if dates[i].month == m]) for m in months]
monthly_out_temp = [np.mean([out_temp[i] for i in range(len(out_temp)) 
                             if dates[i].month == m]) for m in months]
x = np.arange(len(months))
width = 0.35
bars1 = ax4.bar(x - width/2, monthly_out_temp, width, label='Outdoor', 
                color='steelblue', alpha=0.8, edgecolor='black', linewidth=0.5)
bars2 = ax4.bar(x + width/2, monthly_op_temp, width, label='Operative', 
                color='coral', alpha=0.8, edgecolor='black', linewidth=0.5)
ax4.axhline(temp_comfort[0], color='green', linestyle='--', alpha=0.5, linewidth=1.5)
ax4.axhline(temp_comfort[1], color='green', linestyle='--', alpha=0.5, linewidth=1.5)
ax4.set_xlabel('Month', fontsize=11, fontweight='bold')
ax4.set_ylabel('Temperature (°C)', fontsize=11, fontweight='bold')
ax4.set_title('Monthly Average Temperatures', fontsize=13, fontweight='bold', pad=10)
ax4.set_xticks(x)
ax4.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')

# Monthly averages - Humidity
ax5 = fig1.add_subplot(gs1[1, 1])
monthly_op_relh = [np.mean([op_relh[i] for i in range(len(op_relh)) 
                            if dates[i].month == m]) for m in months]
monthly_out_relh = [np.mean([out_relh[i] for i in range(len(out_relh)) 
                             if dates[i].month == m]) for m in months]
bars3 = ax5.bar(x - width/2, monthly_out_relh, width, label='Outdoor', 
                color='steelblue', alpha=0.8, edgecolor='black', linewidth=0.5)
bars4 = ax5.bar(x + width/2, monthly_op_relh, width, label='Operative', 
                color='lightcoral', alpha=0.8, edgecolor='black', linewidth=0.5)
ax5.axhline(relh_comfort[0], color='green', linestyle='--', alpha=0.5, linewidth=1.5)
ax5.axhline(relh_comfort[1], color='green', linestyle='--', alpha=0.5, linewidth=1.5)
ax5.set_xlabel('Month', fontsize=11, fontweight='bold')
ax5.set_ylabel('Relative Humidity (%)', fontsize=11, fontweight='bold')
ax5.set_title('Monthly Average Humidity', fontsize=13, fontweight='bold', pad=10)
ax5.set_xticks(x)
ax5.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax5.legend(fontsize=10)
ax5.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')

# Comfort statistics pie chart
ax6 = fig1.add_subplot(gs1[1, 2])
comfort_hours = both_in_comfort
discomfort_hours = len(op_temp) - both_in_comfort
sizes = [comfort_hours, discomfort_hours]
colors = ['#90EE90', '#FFB6C6']
explode = (0.05, 0)
wedges, texts, autotexts = ax6.pie(sizes, explode=explode, labels=['Comfort', 'Discomfort'],
                                     colors=colors, autopct='%1.1f%%', startangle=90,
                                     textprops={'fontsize': 11, 'fontweight': 'bold'},
                                     shadow=True)
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')
ax6.set_title('Overall Comfort Hours', fontsize=13, fontweight='bold', pad=10)

plt.savefig('fancy_analysis_1.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: fancy_analysis_1.png")

# ===== FIGURE 2: 3D VISUALIZATIONS =====
fig2 = plt.figure(figsize=(18, 12))
fig2.suptitle('3D Environmental Analysis', fontsize=18, fontweight='bold', y=0.96)

gs2 = GridSpec(2, 2, figure=fig2, hspace=0.3, wspace=0.25)

# 3D Scatter - All data
ax7 = fig2.add_subplot(gs2[0, 0], projection='3d')
comfort_mask = [(temp_comfort[0] <= op_temp[i] <= temp_comfort[1] and 
                 relh_comfort[0] <= op_relh[i] <= relh_comfort[1]) 
                for i in range(len(op_temp))]
comfort_idx = [i for i, m in enumerate(comfort_mask) if m]
discomfort_idx = [i for i, m in enumerate(comfort_mask) if not m]

if discomfort_idx:
    ax7.scatter([out_temp[i] for i in discomfort_idx],
                [out_relh[i] for i in discomfort_idx],
                [op_temp[i] for i in discomfort_idx],
                c='red', alpha=0.2, s=3, label='Discomfort')
if comfort_idx:
    ax7.scatter([out_temp[i] for i in comfort_idx],
                [out_relh[i] for i in comfort_idx],
                [op_temp[i] for i in comfort_idx],
                c='green', alpha=0.4, s=3, label='Comfort')

ax7.set_xlabel('Outdoor Temp (°C)', fontsize=10, fontweight='bold')
ax7.set_ylabel('Outdoor RH (%)', fontsize=10, fontweight='bold')
ax7.set_zlabel('Op. Temp (°C)', fontsize=10, fontweight='bold')
ax7.set_title('3D Scatter: Outdoor vs Operative', fontsize=12, fontweight='bold', pad=15)
ax7.legend(fontsize=9)
ax7.view_init(elev=25, azim=45)

# 3D Scatter - Operative conditions
ax8 = fig2.add_subplot(gs2[0, 1], projection='3d')
# Sample data for better visualization (every 10th point)
sample_idx = list(range(0, len(op_temp), 10))
scatter = ax8.scatter([op_temp[i] for i in sample_idx],
                      [op_relh[i] for i in sample_idx],
                      [dates[i].timetuple().tm_yday for i in sample_idx],
                      c=[dates[i].timetuple().tm_yday for i in sample_idx],
                      cmap='viridis', alpha=0.6, s=20)
ax8.set_xlabel('Op. Temp (°C)', fontsize=10, fontweight='bold')
ax8.set_ylabel('Op. RH (%)', fontsize=10, fontweight='bold')
ax8.set_zlabel('Day of Year', fontsize=10, fontweight='bold')
ax8.set_title('Operative Conditions Over Time', fontsize=12, fontweight='bold', pad=15)
cbar = plt.colorbar(scatter, ax=ax8, pad=0.1, shrink=0.8)
cbar.set_label('Day of Year', fontsize=9)
ax8.view_init(elev=20, azim=135)

# Distribution histograms - Temperature
ax9 = fig2.add_subplot(gs2[1, 0])
ax9.hist(op_temp, bins=50, alpha=0.6, color='coral', edgecolor='black', 
         linewidth=0.5, label='Operative Temp')
ax9.hist(out_temp, bins=50, alpha=0.6, color='steelblue', edgecolor='black', 
         linewidth=0.5, label='Outdoor Temp')
ax9.axvspan(temp_comfort[0], temp_comfort[1], alpha=0.2, color='green', 
            label='Comfort Zone')
ax9.set_xlabel('Temperature (°C)', fontsize=11, fontweight='bold')
ax9.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax9.set_title('Temperature Distribution', fontsize=13, fontweight='bold', pad=10)
ax9.legend(fontsize=10)
ax9.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')

# Distribution histograms - Humidity
ax10 = fig2.add_subplot(gs2[1, 1])
ax10.hist(op_relh, bins=50, alpha=0.6, color='lightcoral', edgecolor='black', 
          linewidth=0.5, label='Operative RH')
ax10.hist(out_relh, bins=50, alpha=0.6, color='steelblue', edgecolor='black', 
          linewidth=0.5, label='Outdoor RH')
ax10.axvspan(relh_comfort[0], relh_comfort[1], alpha=0.2, color='green', 
             label='Comfort Zone')
ax10.set_xlabel('Relative Humidity (%)', fontsize=11, fontweight='bold')
ax10.set_ylabel('Frequency', fontsize=11, fontweight='bold')
ax10.set_title('Humidity Distribution', fontsize=13, fontweight='bold', pad=10)
ax10.legend(fontsize=10)
ax10.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')

plt.savefig('fancy_analysis_2.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: fancy_analysis_2.png")

# ===== FIGURE 3: HEATMAPS =====
fig3 = plt.figure(figsize=(18, 10))
fig3.suptitle('Temporal Heatmap Analysis', fontsize=18, fontweight='bold', y=0.96)

gs3 = GridSpec(2, 2, figure=fig3, hspace=0.35, wspace=0.3)

# Create hourly/daily matrices
days = 365
hours_per_day = 24
temp_matrix = np.array(op_temp[:days*hours_per_day]).reshape(days, hours_per_day)
relh_matrix = np.array(op_relh[:days*hours_per_day]).reshape(days, hours_per_day)

# Temperature heatmap
ax11 = fig3.add_subplot(gs3[0, :])
im1 = ax11.imshow(temp_matrix.T, aspect='auto', cmap='RdYlBu_r', interpolation='nearest')
ax11.set_xlabel('Day of Year', fontsize=11, fontweight='bold')
ax11.set_ylabel('Hour of Day', fontsize=11, fontweight='bold')
ax11.set_title('Operative Temperature Heatmap (°C)', fontsize=13, fontweight='bold', pad=10)
ax11.set_yticks(range(0, 24, 3))
ax11.set_xticks(range(0, 365, 30))
cbar1 = plt.colorbar(im1, ax=ax11, pad=0.01)
cbar1.set_label('Temperature (°C)', fontsize=10)

# Humidity heatmap
ax12 = fig3.add_subplot(gs3[1, :])
im2 = ax12.imshow(relh_matrix.T, aspect='auto', cmap='Blues', interpolation='nearest')
ax12.set_xlabel('Day of Year', fontsize=11, fontweight='bold')
ax12.set_ylabel('Hour of Day', fontsize=11, fontweight='bold')
ax12.set_title('Operative Relative Humidity Heatmap (%)', fontsize=13, fontweight='bold', pad=10)
ax12.set_yticks(range(0, 24, 3))
ax12.set_xticks(range(0, 365, 30))
cbar2 = plt.colorbar(im2, ax=ax12, pad=0.01)
cbar2.set_label('Relative Humidity (%)', fontsize=10)

plt.savefig('fancy_analysis_3.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: fancy_analysis_3.png")

print("\n" + "="*60)
print("All fancy visualizations created successfully!")
print("="*60)

plt.show()

# Made with Bob
