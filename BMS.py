import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# ----------------------
# Parameters
# ----------------------
battery_capacity_wh = 60
initial_soc = 0.8
current_energy = battery_capacity_wh * initial_soc

time_series = []
power_usage = []
remaining_time_estimates = []
soc_list = []
mode_list = []

# Power usage profiles per mode
mode_profiles = {
    "Idle": (5, 10),
    "Moderate": (10, 15),
    "Performance": (15, 25)
}

# ----------------------
# Simulation Loop
# ----------------------
for t in range(60):
    if current_energy <= 0:
        break

    mode = np.random.choice(list(mode_profiles.keys()))
    power_range = mode_profiles[mode]
    power = np.random.uniform(*power_range)

    time_remaining = current_energy / power
    current_energy -= power / 60  # energy drained in 1 minute
    soc = max(current_energy / battery_capacity_wh, 0)

    time_series.append(t)
    power_usage.append(power)
    remaining_time_estimates.append(time_remaining * 60)
    soc_list.append(soc * 100)
    mode_list.append(mode)

# ----------------------
# Create Subplots
# ----------------------
fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                    vertical_spacing=0.1,
                    row_heights=[0.3, 0.3, 0.4],
                    specs=[[{"type": "xy"}],
                           [{"type": "xy"}],
                           [{"type": "domain"}]],
                    subplot_titles=("Power Usage (W)", "Time Remaining (minutes)", None))  # Removed gauge title

# Power Usage Plot
fig.add_trace(go.Scatter(
    x=time_series, y=power_usage, mode='lines+markers',
    name='Power (W)', line=dict(color='red')
), row=1, col=1)

# Time Remaining Plot
fig.add_trace(go.Scatter(
    x=time_series, y=remaining_time_estimates, mode='lines+markers',
    name='Time Remaining (min)', line=dict(color='blue')
), row=2, col=1)

# SoC Gauge
# Add SoC Gauge (no built-in title)
fig.add_trace(go.Indicator(
    mode="gauge+number",
    value=soc_list[-1],
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0, 20], 'color': "red"},
            {'range': [20, 50], 'color': "orange"},
            {'range': [50, 100], 'color': "lightgreen"},
        ],
    },
    domain={'x': [0, 1], 'y': [0.1, 1]}  # Shift gauge + number upward to make space for title
), row=3, col=1)

# Add separate annotation below the gauge
fig.add_annotation(
    text="<b>Final SoC (%)</b>",
    showarrow=False,
    font=dict(size=18),
    xref="paper", yref="paper",
    x=0.5, y=0.13,
    xanchor='center'
)


# Layout
fig.update_layout(
    title="⚡ Battery Simulation with Smart Modes, SoC Gauge, and Export",
    height=800,
    showlegend=False
)

fig.update_xaxes(title_text="Time (minutes)", row=2, col=1)
fig.update_yaxes(title_text="Power (W)", row=1, col=1)
fig.update_yaxes(title_text="Time Left (min)", row=2, col=1)

fig.show()

# ----------------------
# Export to CSV
# ----------------------
df = pd.DataFrame({
    'Time (min)': time_series,
    'Power (W)': power_usage,
    'Mode': mode_list,
    'SoC (%)': soc_list,
    'Time Remaining (min)': remaining_time_estimates
})
df.to_csv("battery_simulation_log.csv", index=False)
print("✅ Simulation complete. Data saved to 'battery_simulation_log.csv'")

