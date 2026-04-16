import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib.gridspec import GridSpec

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

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

# Comfort parameters
temp_comfort = (22, 26)
relh_comfort = (30, 60)

print("\n" + "="*70)
print("CREATING RIDGELINE PLOTS")
print("="*70 + "\n")

# ===== CREATE FIGURE WITH 4 RIDGELINE PLOTS =====
fig = plt.figure(figsize=(20, 16))
fig.suptitle('Ridgeline Plots - Monthly Environmental Distributions', 
             fontsize=20, fontweight='bold', y=0.98)

gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_colors = plt.cm.viridis(np.linspace(0, 1, 12))

# ===== RIDGELINE 1: OUTDOOR TEMPERATURE =====
ax1 = fig.add_subplot(gs[0, 0])

for month_idx in range(12):
    month_data = [out_temp[i] for i in range(len(out_temp)) if dates[i].month == month_idx + 1]
    if month_data:
        # Create density estimation with more bins for smoother curves
        hist, bins = np.histogram(month_data, bins=50, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        # Scale the histogram for better visualization
        scale_factor = 4.0
        hist_scaled = hist * scale_factor + month_idx * 1.0
        
        # Fill area
        ax1.fill_between(bin_centers, month_idx * 1.0, hist_scaled, 
                        alpha=0.75, color=month_colors[month_idx], 
                        edgecolor='black', linewidth=1.5)
        
        # Add outline
        ax1.plot(bin_centers, hist_scaled, color='black', linewidth=1.5, alpha=0.8)
        
        # Add month label
        ax1.text(min(bin_centers) - 2, month_idx * 1.0 + 0.3, months[month_idx], 
                fontsize=11, fontweight='bold', va='center')

# Add comfort zone
ax1.axvspan(temp_comfort[0], temp_comfort[1], alpha=0.15, color='green', 
           zorder=0, label='Comfort Zone')

ax1.set_xlabel('Outdoor Temperature (°C)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Month', fontsize=13, fontweight='bold')
ax1.set_title('Outdoor Temperature Distribution by Month', 
             fontsize=15, fontweight='bold', pad=15)
ax1.set_yticks(np.arange(12) * 1.0)
ax1.set_yticklabels([])
ax1.grid(True, alpha=0.2, axis='x', linestyle='--')
ax1.legend(loc='upper right', fontsize=11)

# ===== RIDGELINE 2: OPERATIVE TEMPERATURE =====
ax2 = fig.add_subplot(gs[0, 1])

for month_idx in range(12):
    month_data = [op_temp[i] for i in range(len(op_temp)) if dates[i].month == month_idx + 1]
    if month_data:
        hist, bins = np.histogram(month_data, bins=50, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        scale_factor = 4.0
        hist_scaled = hist * scale_factor + month_idx * 1.0
        
        ax2.fill_between(bin_centers, month_idx * 1.0, hist_scaled, 
                        alpha=0.75, color=month_colors[month_idx], 
                        edgecolor='black', linewidth=1.5)
        ax2.plot(bin_centers, hist_scaled, color='black', linewidth=1.5, alpha=0.8)
        
        ax2.text(min(bin_centers) - 2, month_idx * 1.0 + 0.3, months[month_idx], 
                fontsize=11, fontweight='bold', va='center')

ax2.axvspan(temp_comfort[0], temp_comfort[1], alpha=0.15, color='green', 
           zorder=0, label='Comfort Zone')

ax2.set_xlabel('Operative Temperature (°C)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Month', fontsize=13, fontweight='bold')
ax2.set_title('Operative Temperature Distribution by Month', 
             fontsize=15, fontweight='bold', pad=15)
ax2.set_yticks(np.arange(12) * 1.0)
ax2.set_yticklabels([])
ax2.grid(True, alpha=0.2, axis='x', linestyle='--')
ax2.legend(loc='upper right', fontsize=11)

# ===== RIDGELINE 3: OUTDOOR RELATIVE HUMIDITY =====
ax3 = fig.add_subplot(gs[1, 0])

humidity_colors = plt.cm.plasma(np.linspace(0, 1, 12))

for month_idx in range(12):
    month_data = [out_relh[i] for i in range(len(out_relh)) if dates[i].month == month_idx + 1]
    if month_data:
        hist, bins = np.histogram(month_data, bins=50, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        scale_factor = 10.0
        hist_scaled = hist * scale_factor + month_idx * 1.0
        
        ax3.fill_between(bin_centers, month_idx * 1.0, hist_scaled, 
                        alpha=0.75, color=humidity_colors[month_idx], 
                        edgecolor='black', linewidth=1.5)
        ax3.plot(bin_centers, hist_scaled, color='black', linewidth=1.5, alpha=0.8)
        
        ax3.text(min(bin_centers) - 5, month_idx * 1.0 + 0.3, months[month_idx], 
                fontsize=11, fontweight='bold', va='center')

ax3.axvspan(relh_comfort[0], relh_comfort[1], alpha=0.15, color='green', 
           zorder=0, label='Comfort Zone')

ax3.set_xlabel('Outdoor Relative Humidity (%)', fontsize=13, fontweight='bold')
ax3.set_ylabel('Month', fontsize=13, fontweight='bold')
ax3.set_title('Outdoor Relative Humidity Distribution by Month', 
             fontsize=15, fontweight='bold', pad=15)
ax3.set_yticks(np.arange(12) * 1.0)
ax3.set_yticklabels([])
ax3.grid(True, alpha=0.2, axis='x', linestyle='--')
ax3.legend(loc='upper right', fontsize=11)

# ===== RIDGELINE 4: OPERATIVE RELATIVE HUMIDITY =====
ax4 = fig.add_subplot(gs[1, 1])

for month_idx in range(12):
    month_data = [op_relh[i] for i in range(len(op_relh)) if dates[i].month == month_idx + 1]
    if month_data:
        hist, bins = np.histogram(month_data, bins=50, density=True)
        bin_centers = (bins[:-1] + bins[1:]) / 2
        
        scale_factor = 10.0
        hist_scaled = hist * scale_factor + month_idx * 1.0
        
        ax4.fill_between(bin_centers, month_idx * 1.0, hist_scaled, 
                        alpha=0.75, color=humidity_colors[month_idx], 
                        edgecolor='black', linewidth=1.5)
        ax4.plot(bin_centers, hist_scaled, color='black', linewidth=1.5, alpha=0.8)
        
        ax4.text(min(bin_centers) - 3, month_idx * 1.0 + 0.3, months[month_idx], 
                fontsize=11, fontweight='bold', va='center')

ax4.axvspan(relh_comfort[0], relh_comfort[1], alpha=0.15, color='green', 
           zorder=0, label='Comfort Zone')

ax4.set_xlabel('Operative Relative Humidity (%)', fontsize=13, fontweight='bold')
ax4.set_ylabel('Month', fontsize=13, fontweight='bold')
ax4.set_title('Operative Relative Humidity Distribution by Month', 
             fontsize=15, fontweight='bold', pad=15)
ax4.set_yticks(np.arange(12) * 1.0)
ax4.set_yticklabels([])
ax4.grid(True, alpha=0.2, axis='x', linestyle='--')
ax4.legend(loc='upper right', fontsize=11)

# Save figure
plt.savefig('ridgeline_plots.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ridgeline_plots.png")

print("\n" + "="*70)
print("RIDGELINE PLOTS COMPLETED!")
print("="*70)
print("\nThe plot shows monthly distributions for:")
print("  • Outdoor Temperature (top left)")
print("  • Operative Temperature (top right)")
print("  • Outdoor Relative Humidity (bottom left)")
print("  • Operative Relative Humidity (bottom right)")
print("\nGreen shaded areas indicate comfort zones.")
print("="*70 + "\n")

plt.show()

# Made with Bob
