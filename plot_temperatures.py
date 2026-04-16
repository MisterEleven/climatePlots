import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator, DayLocator
from datetime import datetime, timedelta

# Read operative temperature data
with open('op-temp', 'r') as f:
    lines = f.readlines()
    op_temp = [float(line.strip()) for line in lines[1:]]  # Skip header

# Read outdoor temperature data
with open('out-temp', 'r') as f:
    lines = f.readlines()
    out_temp = [float(line.strip()) for line in lines[1:]]  # Skip header

# Verify data length
print(f"Operative temperature data points: {len(op_temp)}")
print(f"Outdoor temperature data points: {len(out_temp)}")

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ===== SUBPLOT 1: SCATTER PLOT =====

# Separate points inside and outside comfort band
comfort_min, comfort_max = 22, 26
inside_comfort = []
outside_comfort = []
inside_out = []
outside_out = []

for i in range(len(op_temp)):
    if comfort_min <= op_temp[i] <= comfort_max:
        inside_comfort.append(op_temp[i])
        inside_out.append(out_temp[i])
    else:
        outside_comfort.append(op_temp[i])
        outside_out.append(out_temp[i])

# Plot points outside comfort band in red
if outside_comfort:
    ax1.scatter(outside_out, outside_comfort, alpha=0.5, s=10, c='red',
                edgecolors='none', label=f'Outside Comfort Band ({len(outside_comfort)} points)')

# Plot points inside comfort band in blue
if inside_comfort:
    ax1.scatter(inside_out, inside_comfort, alpha=0.5, s=10, c='blue',
                edgecolors='none', label=f'Inside Comfort Band ({len(inside_comfort)} points)')

# Add comfort band (22-26°C)
ax1.axhspan(comfort_min, comfort_max, alpha=0.2, color='green', label='Comfort Band (22-26°C)', zorder=0)

# Set labels
ax1.set_xlabel('Outdoor Temperature (°C)', fontsize=12)
ax1.set_ylabel('Operative Temperature (°C)', fontsize=12)
ax1.set_title('Operative Temperature vs Outdoor Temperature', fontsize=14, fontweight='bold')

# Add legend
ax1.legend(loc='best', fontsize=10)

# Adjust axis ranges based on data
x_min, x_max = min(out_temp), max(out_temp)
y_min, y_max = min(op_temp), max(op_temp)

# Add some padding (5% on each side)
x_padding = (x_max - x_min) * 0.05
y_padding = (y_max - y_min) * 0.05

ax1.set_xlim(x_min - x_padding, x_max + x_padding)
ax1.set_ylim(y_min - y_padding, y_max + y_padding)

# Add grid for better readability
ax1.grid(True, alpha=0.3, linestyle='--')

# ===== SUBPLOT 2: TIME SERIES PLOT =====
# Create datetime array for x-axis (assuming data starts Jan 1)
start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(hours=i) for i in range(len(op_temp))]

# Plot outdoor temperature in blue
ax2.plot(dates, out_temp, linewidth=1, color='blue', alpha=0.7, label='Outdoor Temperature')

# Plot operative temperature with color coding
# Split into segments based on comfort band
for i in range(len(op_temp) - 1):
    if comfort_min <= op_temp[i] <= comfort_max and comfort_min <= op_temp[i+1] <= comfort_max:
        # Both points inside comfort band - yellow
        ax2.plot([dates[i], dates[i+1]], [op_temp[i], op_temp[i+1]],
                color='yellow', linewidth=2, alpha=0.8)
    elif op_temp[i] < comfort_min or op_temp[i] > comfort_max or op_temp[i+1] < comfort_min or op_temp[i+1] > comfort_max:
        # At least one point outside comfort band - red
        ax2.plot([dates[i], dates[i+1]], [op_temp[i], op_temp[i+1]],
                color='red', linewidth=2, alpha=0.8)

# Add legend entries for operative temperature colors
ax2.plot([], [], color='yellow', linewidth=2, label='Op. Temp (Inside Comfort)')
ax2.plot([], [], color='red', linewidth=2, label='Op. Temp (Outside Comfort)')

# Add comfort band
ax2.axhspan(comfort_min, comfort_max, alpha=0.15, color='green', label='Comfort Band (22-26°C)', zorder=0)

# Set labels
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Temperature (°C)', fontsize=12)
ax2.set_title('Temperature Time Series Throughout the Year', fontsize=14, fontweight='bold')

# Format x-axis to show months
ax2.xaxis.set_major_locator(MonthLocator())
ax2.xaxis.set_major_formatter(DateFormatter('%b'))
ax2.xaxis.set_minor_locator(DayLocator(bymonthday=[1, 15]))

# Rotate date labels for better readability
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0, ha='center')

# Adjust axis ranges to show all points (both outdoor and operative temps)
all_temps = op_temp + out_temp
all_min, all_max = min(all_temps), max(all_temps)
all_padding = (all_max - all_min) * 0.05

ax2.set_xlim(dates[0], dates[-1])
ax2.set_ylim(all_min - all_padding, all_max + all_padding)

# Add grid
ax2.grid(True, alpha=0.3, linestyle='--')

# Add legend
ax2.legend(loc='best', fontsize=10)

# Display statistics
print(f"\nOutdoor Temperature Range: {x_min:.2f}°C to {x_max:.2f}°C")
print(f"Operative Temperature Range: {y_min:.2f}°C to {y_max:.2f}°C")

# Save the plot
plt.tight_layout()
plt.savefig('temperature_plots.png', dpi=300, bbox_inches='tight')
print("\nPlots saved as 'temperature_plots.png'")

# Show the plot
plt.show()
