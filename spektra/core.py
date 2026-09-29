"""Theme file loading shared by themes.py and terminals.py."""

import json
import os


def themes_dir():
    return os.path.join(os.path.dirname(__file__), "themes")


def theme_path(theme_name):
    path = os.path.join(themes_dir(), f"{theme_name}.json")
    if not os.path.exists(path):
        raise ValueError(f"Theme '{theme_name}' not found at {path}")
    return path


def load_config(theme_name):
    with open(theme_path(theme_name)) as f:
        return json.load(f)


def available_themes():
    d = themes_dir()
    if not os.path.exists(d):
        return []
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json"))
