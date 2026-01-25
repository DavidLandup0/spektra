import spektra as sk
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Apply theme
sk.style("ember")
c = sk.get_config()
colors = c["colors"]
settings = c["settings"]
palette = sk.get_palette()

# --- Generate Data ---
np.random.seed(42)
n = 100
time = np.linspace(0, 10, n)
sig_1 = np.sin(time) + np.random.normal(0, 0.1, n)
sig_2 = np.cos(time) + np.random.normal(0, 0.1, n)
sig_3 = np.sin(time * 2) + np.random.normal(0, 0.15, n)

categories = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
values = [45, 32, 28, 52, 38]

scatter_x = np.random.randn(200)
scatter_y = scatter_x * 2 + np.random.randn(200) * 0.5

matrix_data = np.random.rand(10, 10)

# --- Create Dashboard Grid ---
fig = make_subplots(
    rows=2,
    cols=3,
    subplot_titles=(
        "> SIGNAL_MONITOR",
        "> PERFORMANCE_METRICS",
        "> SCATTER_ANALYSIS",
        "> SYSTEM_STATUS",
        "> THERMAL_MAP",
        "> DISTRIBUTION",
    ),
    specs=[
        [{"type": "scatter"}, {"type": "bar"}, {"type": "scatter"}],
        [{"type": "scatter"}, {"type": "heatmap"}, {"type": "histogram"}],
    ],
)

# [1,1] Multi-Line Time Series
fig.add_trace(
    go.Scatter(
        x=time,
        y=sig_1,
        mode="lines+markers",
        name="STREAM_01",
        line=dict(color=palette[0], width=2),
        marker=dict(size=3, symbol="square"),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=time,
        y=sig_2,
        mode="lines+markers",
        name="STREAM_02",
        line=dict(color=palette[1], width=2),
        marker=dict(size=3, symbol="square"),
    ),
    row=1,
    col=1,
)
fig.add_trace(
    go.Scatter(
        x=time,
        y=sig_3,
        mode="lines+markers",
        name="STREAM_03",
        line=dict(color=palette[2], width=2),
        marker=dict(size=3, symbol="square"),
    ),
    row=1,
    col=1,
)

# [1,2] Bar Chart
fig.add_trace(
    go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors["accent"], line=dict(color=colors["bg"], width=2)),
    ),
    row=1,
    col=2,
)

# [1,3] Scatter with Color Gradient
fig.add_trace(
    go.Scatter(
        x=scatter_x,
        y=scatter_y,
        mode="markers",
        marker=dict(
            size=8,
            color=scatter_y,
            colorscale=[[0, colors["bg"]], [1, colors["accent"]]],
            symbol="square",
            line=dict(width=1, color=colors["secondary"]),
        ),
        showlegend=False,
    ),
    row=1,
    col=3,
)

# [2,1] Area Chart
fig.add_trace(
    go.Scatter(
        x=time,
        y=sig_1,
        fill="tozeroy",
        line=dict(color=colors["accent"], width=2),
        fillcolor=f"rgba({int(colors['accent'][1:3], 16)}, {int(colors['accent'][3:5], 16)}, {int(colors['accent'][5:7], 16)}, {settings['op']})",
        showlegend=False,
    ),
    row=2,
    col=1,
)

# [2,2] Heatmap
fig.add_trace(
    go.Heatmap(
        z=matrix_data,
        colorscale=[[0, colors["bg"]], [0.5, colors["secondary"]], [1, colors["accent"]]],
        showscale=False,
        xgap=2,
        ygap=2,
    ),
    row=2,
    col=2,
)

# [2,3] Histogram
hist_data = np.random.normal(0, 1, 1000)
fig.add_trace(
    go.Histogram(
        x=hist_data,
        marker=dict(color=colors["accent"], line=dict(color=colors["bg"], width=1)),
        opacity=settings["op"] * 2,
        showlegend=False,
    ),
    row=2,
    col=3,
)

# --- Layout Configuration ---
theme_name = sk.get_current_theme()
fig.update_layout(
    height=800,
    width=1400,
    paper_bgcolor=colors["bg"],
    plot_bgcolor=colors["bg"],
    font=dict(color=colors["text"], family="Roboto Mono, Cascadia Code, monospace", size=11),
    title=dict(
        text=f"// TACTICAL_DASHBOARD // MODE: {theme_name.upper()} //",
        font=dict(size=20, color=colors["accent"]),
        x=0.5,
        xanchor="center",
    ),
    showlegend=True,
    legend=dict(
        bgcolor=colors["bg"], bordercolor=colors["secondary"], borderwidth=1, font=dict(size=10)
    ),
    margin=dict(t=100, l=80, r=80, b=80),
)

# Update all axes with grid and styling
fig.update_xaxes(
    showline=True,
    linewidth=2,
    linecolor=colors["secondary"] if theme_name == "tactical" else "#444444",
    gridcolor=colors["grid"],
    gridwidth=1,
    zeroline=False,
    tickfont=dict(size=9),
)

fig.update_yaxes(
    showline=True,
    linewidth=2,
    linecolor=colors["secondary"] if theme_name == "tactical" else "#444444",
    gridcolor=colors["grid"],
    gridwidth=1,
    zeroline=False,
    tickfont=dict(size=9),
)

fig.update_annotations(font=dict(color=colors["accent"], size=12))
fig.show()
