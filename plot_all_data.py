import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator, DayLocator
from datetime import datetime, timedelta
from mpl_toolkits.mplot3d import Axes3D

# Read operative temperature data
with open('op-temp', 'r') as f:
    lines = f.readlines()
    op_temp = [float(line.strip()) for line in lines[1:]]  # Skip header

# Read outdoor temperature data
with open('out-temp', 'r') as f:
    lines = f.readlines()
    out_temp = [float(line.strip()) for line in lines[1:]]  # Skip header

# Read operative relative humidity data
with open('op-relh', 'r') as f:
    lines = f.readlines()
    op_relh = [float(line.strip()) for line in lines[1:]]  # Skip header

# Read outdoor relative humidity data
with open('out-relh', 'r') as f:
    lines = f.readlines()
    out_relh = [float(line.strip()) for line in lines[1:]]  # Skip header

# Verify data length
print(f"Data points: {len(op_temp)}")
print(f"Temperature range - Op: {min(op_temp):.2f} to {max(op_temp):.2f}°C")
print(f"Temperature range - Out: {min(out_temp):.2f} to {max(out_temp):.2f}°C")
print(f"Rel. Humidity range - Op: {min(op_relh):.2f} to {max(op_relh):.2f}%")
print(f"Rel. Humidity range - Out: {min(out_relh):.2f} to {max(out_relh):.2f}%")

# Comfort band parameters
temp_comfort_min, temp_comfort_max = 22, 26
relh_comfort_min, relh_comfort_max = 30, 60

# Create datetime array for time series
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(hours=i) for i in range(len(op_temp))]

# ===== CREATE FIGURE WITH 5 SUBPLOTS =====
fig = plt.figure(figsize=(16, 22))

# ===== SUBPLOT 1: TEMPERATURE SCATTER PLOT =====
ax1 = plt.subplot(3, 2, 1)

# Separate points inside and outside temperature comfort band
inside_temp_comfort = []
outside_temp_comfort = []
inside_temp_out = []
outside_temp_out = []

for i in range(len(op_temp)):
    if temp_comfort_min <= op_temp[i] <= temp_comfort_max:
        inside_temp_comfort.append(op_temp[i])
        inside_temp_out.append(out_temp[i])
    else:
        outside_temp_comfort.append(op_temp[i])
        outside_temp_out.append(out_temp[i])

# Plot points
if outside_temp_comfort:
    ax1.scatter(outside_temp_out, outside_temp_comfort, alpha=0.5, s=10, c='red', 
                edgecolors='none', label=f'Outside Comfort ({len(outside_temp_comfort)} pts)')
if inside_temp_comfort:
    ax1.scatter(inside_temp_out, inside_temp_comfort, alpha=0.5, s=10, c='blue', 
                edgecolors='none', label=f'Inside Comfort ({len(inside_temp_comfort)} pts)')

ax1.axhspan(temp_comfort_min, temp_comfort_max, alpha=0.2, color='green', 
            label='Comfort Band (22-26°C)', zorder=0)

ax1.set_xlabel('Outdoor Temperature (°C)', fontsize=11)
ax1.set_ylabel('Operative Temperature (°C)', fontsize=11)
ax1.set_title('Operative vs Outdoor Temperature', fontsize=12, fontweight='bold')
ax1.legend(loc='best', fontsize=9)
ax1.grid(True, alpha=0.3, linestyle='--')

# ===== SUBPLOT 2: TEMPERATURE TIME SERIES =====
ax2 = plt.subplot(3, 2, 2)

# Plot outdoor temperature
ax2.plot(dates, out_temp, linewidth=1, color='blue', alpha=0.7, label='Outdoor Temperature')

# Plot operative temperature with color coding
for i in range(len(op_temp) - 1):
    if temp_comfort_min <= op_temp[i] <= temp_comfort_max and temp_comfort_min <= op_temp[i+1] <= temp_comfort_max:
        ax2.plot([dates[i], dates[i+1]], [op_temp[i], op_temp[i+1]], 
                color='yellow', linewidth=2, alpha=0.8)
    else:
        ax2.plot([dates[i], dates[i+1]], [op_temp[i], op_temp[i+1]], 
                color='red', linewidth=2, alpha=0.8)

ax2.plot([], [], color='yellow', linewidth=2, label='Op. Temp (Inside Comfort)')
ax2.plot([], [], color='red', linewidth=2, label='Op. Temp (Outside Comfort)')
ax2.axhspan(temp_comfort_min, temp_comfort_max, alpha=0.15, color='green', 
            label='Comfort Band', zorder=0)

ax2.set_xlabel('Date', fontsize=11)
ax2.set_ylabel('Temperature (°C)', fontsize=11)
ax2.set_title('Temperature Time Series', fontsize=12, fontweight='bold')
ax2.xaxis.set_major_locator(MonthLocator())
ax2.xaxis.set_major_formatter(DateFormatter('%b'))
ax2.legend(loc='best', fontsize=9)
ax2.grid(True, alpha=0.3, linestyle='--')

# ===== SUBPLOT 3: RELATIVE HUMIDITY SCATTER PLOT =====
ax3 = plt.subplot(3, 2, 3)

# Separate points inside and outside humidity comfort band
inside_relh_comfort = []
outside_relh_comfort = []
inside_relh_out = []
outside_relh_out = []

for i in range(len(op_relh)):
    if relh_comfort_min <= op_relh[i] <= relh_comfort_max:
        inside_relh_comfort.append(op_relh[i])
        inside_relh_out.append(out_relh[i])
    else:
        outside_relh_comfort.append(op_relh[i])
        outside_relh_out.append(out_relh[i])

# Plot points
if outside_relh_comfort:
    ax3.scatter(outside_relh_out, outside_relh_comfort, alpha=0.5, s=10, c='red', 
                edgecolors='none', label=f'Outside Comfort ({len(outside_relh_comfort)} pts)')
if inside_relh_comfort:
    ax3.scatter(inside_relh_out, inside_relh_comfort, alpha=0.5, s=10, c='blue', 
                edgecolors='none', label=f'Inside Comfort ({len(inside_relh_comfort)} pts)')

ax3.axhspan(relh_comfort_min, relh_comfort_max, alpha=0.2, color='green', 
            label='Comfort Band (30-60%)', zorder=0)

ax3.set_xlabel('Outdoor Relative Humidity (%)', fontsize=11)
ax3.set_ylabel('Operative Relative Humidity (%)', fontsize=11)
ax3.set_title('Operative vs Outdoor Relative Humidity', fontsize=12, fontweight='bold')
ax3.legend(loc='best', fontsize=9)
ax3.grid(True, alpha=0.3, linestyle='--')

# ===== SUBPLOT 4: RELATIVE HUMIDITY TIME SERIES =====
ax4 = plt.subplot(3, 2, 4)

# Plot outdoor relative humidity
ax4.plot(dates, out_relh, linewidth=1, color='blue', alpha=0.7, label='Outdoor Rel. Humidity')

# Plot operative relative humidity with color coding
for i in range(len(op_relh) - 1):
    if relh_comfort_min <= op_relh[i] <= relh_comfort_max and relh_comfort_min <= op_relh[i+1] <= relh_comfort_max:
        ax4.plot([dates[i], dates[i+1]], [op_relh[i], op_relh[i+1]], 
                color='yellow', linewidth=2, alpha=0.8)
    else:
        ax4.plot([dates[i], dates[i+1]], [op_relh[i], op_relh[i+1]], 
                color='red', linewidth=2, alpha=0.8)

ax4.plot([], [], color='yellow', linewidth=2, label='Op. RelH (Inside Comfort)')
ax4.plot([], [], color='red', linewidth=2, label='Op. RelH (Outside Comfort)')
ax4.axhspan(relh_comfort_min, relh_comfort_max, alpha=0.15, color='green', 
            label='Comfort Band', zorder=0)

ax4.set_xlabel('Date', fontsize=11)
ax4.set_ylabel('Relative Humidity (%)', fontsize=11)
ax4.set_title('Relative Humidity Time Series', fontsize=12, fontweight='bold')
ax4.xaxis.set_major_locator(MonthLocator())
ax4.xaxis.set_major_formatter(DateFormatter('%b'))
ax4.legend(loc='best', fontsize=9)
ax4.grid(True, alpha=0.3, linestyle='--')

# ===== SUBPLOT 5: 3D SCATTER PLOT (spans bottom row) =====
ax5 = plt.subplot(3, 1, 3, projection='3d')

# Determine comfort status for each point (both temp and humidity must be in comfort)
comfort_status = []
for i in range(len(op_temp)):
    temp_ok = temp_comfort_min <= op_temp[i] <= temp_comfort_max
    relh_ok = relh_comfort_min <= op_relh[i] <= relh_comfort_max
    comfort_status.append(temp_ok and relh_ok)

# Separate points
comfort_indices = [i for i, status in enumerate(comfort_status) if status]
discomfort_indices = [i for i, status in enumerate(comfort_status) if not status]

# Plot discomfort points in red
if discomfort_indices:
    ax5.scatter([out_temp[i] for i in discomfort_indices],
                [out_relh[i] for i in discomfort_indices],
                [op_temp[i] for i in discomfort_indices],
                c='red', alpha=0.3, s=5, label=f'Discomfort ({len(discomfort_indices)} pts)')

# Plot comfort points in green
if comfort_indices:
    ax5.scatter([out_temp[i] for i in comfort_indices],
                [out_relh[i] for i in comfort_indices],
                [op_temp[i] for i in comfort_indices],
                c='green', alpha=0.5, s=5, label=f'Comfort ({len(comfort_indices)} pts)')

ax5.set_xlabel('Outdoor Temperature (°C)', fontsize=10)
ax5.set_ylabel('Outdoor Rel. Humidity (%)', fontsize=10)
ax5.set_zlabel('Operative Temperature (°C)', fontsize=10)
ax5.set_title('3D View: Outdoor Conditions vs Operative Temperature', fontsize=12, fontweight='bold')
ax5.legend(loc='best', fontsize=9)

# Adjust viewing angle
ax5.view_init(elev=20, azim=45)

# ===== SAVE AND DISPLAY =====
plt.tight_layout(pad=3.0, h_pad=4.0, w_pad=3.0)
plt.savefig('complete_analysis.png', dpi=300, bbox_inches='tight')
print("\nComplete analysis saved as 'complete_analysis.png'")

plt.show()

# Made with Bob
