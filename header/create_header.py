import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import spektra as sk
import os

np.random.seed(42)

n = 100
time = np.linspace(0, 10, n)
sig_1 = np.sin(time) + np.random.normal(0, 0.1, n)
sig_2 = np.cos(time) + np.random.normal(0, 0.1, n)
dist_data = np.random.normal(0, 1, 500)
matrix_data = np.random.rand(12, 12)
scatter_data = (np.random.randn(40), np.random.randn(40))
hex_data = (np.random.randn(300), np.random.randn(300))
bar_data = np.random.rand(8) * 10


def create_header(theme_name, output_dir="."):
    sk.style(theme_name)
    c = sk.get_config()
    colors = c["colors"]
    settings = c["settings"]
    fig = plt.figure(figsize=(24, 5), facecolor=colors["bg"])

    ax_main = fig.add_axes([0.3, 0.2, 0.4, 0.6])
    ax_main.set_facecolor(colors["bg"])
    ax_main.set_xlim(0, 1)
    ax_main.set_ylim(0, 1)
    ax_main.axis("off")

    border = mpatches.Rectangle(
        (0.02, 0.05),
        0.96,
        0.9,
        linewidth=3,
        edgecolor=colors["accent"],
        facecolor="none",
    )
    ax_main.add_patch(border)

    code_text = f"import spektra as sk\nsk.style('{theme_name}')"
    ax_main.text(
        0.5,
        0.5,
        code_text,
        fontsize=36,
        fontfamily="monospace",
        color=colors["accent"],
        ha="center",
        va="center",
        weight="bold",
        linespacing=1.5,
    )

    ax_main.text(
        0.95,
        0.92,
        f"// {theme_name.upper()} //",
        fontsize=14,
        fontfamily="monospace",
        color=colors["secondary"],
        ha="right",
        va="top",
        alpha=0.8,
    )

    # plots around the main panel
    plot_positions = [
        [0.02, 0.55, 0.12, 0.35],  # Top-left
        [0.15, 0.65, 0.12, 0.28],  # Top-mid-left
        [0.73, 0.60, 0.12, 0.32],  # Top-mid-right
        [0.86, 0.52, 0.12, 0.38],  # Top-right
        [0.02, 0.08, 0.11, 0.35],  # Bottom-left
        [0.15, 0.08, 0.11, 0.32],  # Bottom-mid-left
        [0.75, 0.08, 0.11, 0.35],  # Bottom-mid-right
        [0.88, 0.08, 0.11, 0.35],  # Bottom-right
    ]

    axs = [fig.add_axes(pos) for pos in plot_positions]

    # [0] single line
    axs[0].plot(time, sig_1, color=colors["accent"], linewidth=1.2)
    axs[0].fill_between(time, sig_1, color=colors["accent"], alpha=settings["alpha"])
    axs[0].set_title(
        "> SIGNAL", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [1] scatter
    axs[1].scatter(
        scatter_data[0],
        scatter_data[1],
        facecolors="none",
        edgecolors=colors["accent"],
        marker="s",
        s=15,
    )
    axs[1].set_title(
        "> TARGET", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [2] multi line
    axs[2].plot(time, sig_1, color=colors["accent"], linewidth=1)
    axs[2].plot(time, sig_2, color=colors["secondary"], alpha=0.7, linewidth=1)
    axs[2].set_title(
        "> STREAM", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [3] hex
    axs[3].hexbin(
        hex_data[0],
        hex_data[1],
        gridsize=10,
        cmap=c["cmap"],
        edgecolors=colors["bg"],
        linewidths=0.5,
    )
    axs[3].set_title(
        "> DENSITY", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [4] heat
    sns.heatmap(
        matrix_data[:8, :8],
        ax=axs[4],
        cmap=c["cmap"],
        cbar=False,
        linewidths=0.8,
        linecolor=colors["bg"],
    )
    axs[4].set_title(
        "> MEMORY", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )
    axs[4].set_xticks([])
    axs[4].set_yticks([])

    # [5] dist
    sns.histplot(
        dist_data,
        kde=True,
        ax=axs[5],
        color=colors["accent"],
        element="step",
        alpha=settings["alpha"],
    )
    axs[5].set_title(
        "> DIST", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [6] bar
    axs[6].bar(
        range(len(bar_data)),
        bar_data,
        color=colors["accent"],
        alpha=settings["alpha"],
        edgecolor=colors["accent"],
        linewidth=1,
    )
    axs[6].set_title(
        "> METRICS", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # [7] sine
    axs[7].plot(time, np.sin(time * 3), color=colors["secondary"], linewidth=1.5)
    axs[7].set_title(
        "> WAVEFORM", fontsize=7, color=colors["accent"], fontfamily="monospace"
    )

    # generic styling
    for ax in axs:
        ax.tick_params(labelsize=5, colors=colors["accent"])
        ax.grid(True, alpha=0.2, linestyle=":", linewidth=0.5)
        ax.set_facecolor(colors["bg"])

    output_path = os.path.join(output_dir, f"header_{theme_name}.png")
    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
        facecolor=colors["bg"],
        edgecolor="none",
        pad_inches=0.1,
    )
    plt.close()


def create_all_headers(output_dir="."):
    themes = sk.available_themes()

    print(f"Creating headers for {len(themes)} themes...")
    print(f"Output directory: {os.path.abspath(output_dir)}\n")

    for theme in sorted(themes):
        create_header(theme, output_dir)


if __name__ == "__main__":
    create_all_headers()
