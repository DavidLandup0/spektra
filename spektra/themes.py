import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

import plotly.graph_objects as go
import plotly.io as pio
import matplotlib as mpl

from .core import available_themes
from .core import load_config
from .core import theme_path


class ThemeManager:
    """Convenience class for loading theme configs and getting the current state."""

    def __init__(self):
        self.theme = None
        self.config = None

    def get_theme_directory(self, theme_name):
        return theme_path(theme_name)

    def load_config(self, theme_name):
        """Load config from JSON file."""
        return load_config(theme_name)

    @staticmethod
    def create_colormap(color):
        rgb = mcolors.hex2color(color)

        # Create gradient from near-black to color
        colors = [
            (0.05, 0.05, 0.05),
            tuple(c * 0.3 for c in rgb),
            tuple(c * 0.6 for c in rgb),
            rgb,
        ]

        return mcolors.LinearSegmentedColormap.from_list("cmap", colors)


_theme_manager = ThemeManager()


def get_available_themes():
    """Return list of available theme names."""
    return available_themes()


def get_theme():
    """Return the name of the currently applied theme."""
    return _theme_manager.theme


def get_config(theme_name=None):
    """Get theme configuration dict. Uses current theme if theme_name is None."""
    if theme_name is not None:
        return _theme_manager.load_config(theme_name)
    if _theme_manager.config is None:
        raise ValueError("No theme applied yet. Call style() first.")
    return _theme_manager.config


def get_palette(theme_name=None, num_colors=None):
    """Create color palette for the theme."""
    cfg = get_config(theme_name)
    palette = cfg["palette"]
    if num_colors is None:
        return palette
    elif num_colors <= len(palette):
        return palette[:num_colors]
    else:
        # Cycle through palette if more colors requested
        return [palette[i % len(palette)] for i in range(num_colors)]


def get_cmap(theme_name=None):
    """Create colormap for the given theme (or current theme if None).

    Returns:
        Colormap object.
    """
    cfg = get_config(theme_name)
    return ThemeManager.create_colormap(cfg["colors"]["accent"])


def style_matplotlib(theme_name="ember"):
    """Apply a theme to matplotlib/seaborn.

    Args:
        theme_name: Name of theme to apply. Options: 'ash', 'ember', 'mitsuki', 'neon', 'nightshade', 'raiden', 'sakura', 'sky'.

    Examples:
        >>> import spektra as sk
        >>> sk.style_matplotlib('ember')
    """
    # Load theme config
    cfg = _theme_manager.load_config(theme_name)
    cfg["cmap"] = get_cmap(theme_name)
    plt.rcParams.update(cfg["matplotlib"])
    sns.set_palette(cfg["palette"])
    cmap_name = f"{theme_name}"
    if cmap_name not in mpl.colormaps:
        mpl.colormaps.register(cmap=cfg["cmap"], name=cmap_name)

    plt.rcParams["image.cmap"] = cmap_name
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=cfg["palette"])

    _theme_manager.theme = theme_name
    _theme_manager.config = cfg


def style_plotly(theme_name="ember"):
    """Apply a theme to plotly.

            Args:
                theme_name: Name of theme to apply. Options: 'ash', 'ember', 'mitsuki', 'neon', 'nightshade', 'raiden', 'sakura', 'sky'.
    Examples:
        >>> import spektra as sk
        >>> sk.style_plotly('ember')
    """
    cfg = _theme_manager.load_config(theme_name)
    cfg["cmap"] = get_cmap(theme_name)

    plotly_cfg = cfg["plotly"]

    plotly_template = go.layout.Template()
    plotly_template.layout = go.Layout(
        paper_bgcolor=plotly_cfg["paper_bgcolor"],
        plot_bgcolor=plotly_cfg["plot_bgcolor"],
        font=dict(color=plotly_cfg["font_color"], family=plotly_cfg["font_family"]),
        xaxis=dict(
            gridcolor=plotly_cfg["grid_color"],
            linecolor=plotly_cfg["axis_line_color"],
            tickcolor=plotly_cfg["font_color"],
        ),
        yaxis=dict(
            gridcolor=plotly_cfg["grid_color"],
            linecolor=plotly_cfg["axis_line_color"],
            tickcolor=plotly_cfg["font_color"],
        ),
        colorway=[cfg["colors"]["accent"], cfg["colors"]["secondary"]],
    )

    plotly_template.data.scatter = [
        go.Scatter(marker=dict(color=cfg["colors"]["accent"]))
    ]
    plotly_template.data.bar = [go.Bar(marker=dict(color=cfg["colors"]["accent"]))]

    pio.templates[f"{theme_name}"] = plotly_template
    pio.templates.default = f"{theme_name}"

    _theme_manager.theme = theme_name
    _theme_manager.config = cfg


def style(theme_name="ember"):
    """Apply a theme to both matplotlib and plotly.

    Args:
        theme_name: Name of theme to apply. Options: 'ash', 'ember', 'mitsuki', 'neon', 'nightshade', 'raiden', 'sakura', 'sky'.

    Examples:
        >>> import spektra as sk
        >>> sk.style('ember')
        >>> sk.get_available_themes()
        ['ash', 'ember', 'mitsuki', 'neon', 'nightshade', 'raiden', 'sakura', 'sky']
    """
    style_matplotlib(theme_name)
    style_plotly(theme_name)
