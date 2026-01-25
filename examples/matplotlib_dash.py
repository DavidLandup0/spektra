import spektra as sk
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sk.style("ember")
c = sk.get_config()
colors = c["colors"]
settings = c["settings"]

np.random.seed(42)
n = 100
time = np.linspace(0, 10, n)
sig_1 = np.sin(time) + np.random.normal(0, 0.1, n)
sig_2 = np.cos(time) + np.random.normal(0, 0.1, n)
dist_data = np.random.normal(0, 1, 500)
matrix_data = np.random.rand(12, 12)

fig, axs = plt.subplots(2, 3, figsize=(18, 10))
theme_mode = sk.get_current_theme()
title_base = "BIOMETRIC_STABILITY" if theme_mode == "ash" else "TACTICAL_OVERRIDE"
fig.suptitle(
    f"// {title_base} // MODE_{theme_mode.upper()}",
    color=colors["accent"],
    fontsize=16,
    y=0.96,
)

# line plot
axs[0, 0].plot(time, sig_1, color=colors["accent"], linewidth=1.5)
axs[0, 0].fill_between(time, sig_1, color=colors["accent"], alpha=settings["alpha"])
axs[0, 0].set_title("> SIGNAL_STABILITY")

# multi line
axs[0, 1].plot(time, sig_1, color=colors["accent"], label="STRM_01")
axs[0, 1].plot(
    time, sig_2, color=colors["secondary"], label="STRM_02", alpha=0.6, linewidth=1
)
axs[0, 1].set_title("> STREAM_FEED")
axs[0, 1].legend(frameon=False, fontsize=8)

# scatter
axs[0, 2].scatter(
    np.random.randn(50),
    np.random.randn(50),
    facecolors="none",
    edgecolors=colors["accent"],
    marker="s",
    s=30,
)
axs[0, 2].set_title("> TARGET_ID")

# hex
axs[1, 0].hexbin(
    np.random.randn(500),
    np.random.randn(500),
    gridsize=15,
    cmap=c["cmap"],
    edgecolors=colors["bg"],
)
axs[1, 0].set_title("> DENSITY_SCAN")

# heat
sns.heatmap(
    matrix_data,
    ax=axs[1, 1],
    cmap=c["cmap"],
    cbar=False,
    linewidths=1.5,
    linecolor=colors["bg"],
)
axs[1, 1].set_title("> MEMORY_BUFFER")

# dist
sns.histplot(
    dist_data,
    kde=True,
    ax=axs[1, 2],
    color=colors["accent"],
    element="step",
    alpha=settings["alpha"],
)
axs[1, 2].set_title("> FREQUENCY_DIST")

for ax in axs.flat:
    ax.grid(True, alpha=0.3, linestyle=":")
    for y_line in np.linspace(*ax.get_ylim(), 20):
        ax.axhline(y_line, color="white", alpha=0.015, linewidth=0.5)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
