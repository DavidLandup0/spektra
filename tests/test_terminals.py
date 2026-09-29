"""Validation for `spektra apply` output (Konsole, iTerm2, OpenCode).

Runs on Linux and macOS alike; the macOS CI job additionally runs
`plutil -lint` over the generated files (see .github/workflows/).
"""

import configparser
import json
import plistlib

import pytest

from spektra.core import available_themes, load_config
from spektra.terminals import (
    OPENCODE_ROLES,
    apply,
    apply_all,
    available_targets,
    to_iterm2,
    to_konsole,
    to_opencode,
)

THEMES = available_themes()

KONSOLE_SECTIONS = (
    ["Background", "BackgroundFaint", "BackgroundIntense"]
    + [f"Color{i}" for i in range(8)]
    + [f"Color{i}{v}" for i in range(8) for v in ("Faint", "Intense")]
    + ["Foreground", "ForegroundFaint", "ForegroundIntense", "General"]
)

ITERM_KEYS = {f"Ansi {i} Color" for i in range(16)} | {
    "Background Color",
    "Foreground Color",
    "Bold Color",
    "Cursor Color",
    "Cursor Text Color",
    "Cursor Guide Color",
    "Selection Color",
    "Selected Text Color",
}

COLOR_KEYS = ("Red Component", "Green Component", "Blue Component", "Alpha Component")


def lum(rgb):
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    l1, l2 = lum(a), lum(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def rgb_triplet(s):
    return tuple(int(v) for v in s.split(","))


def plist_rgb(d):
    return tuple(round(d[k] * 255) for k in COLOR_KEYS[:3])


@pytest.mark.parametrize("theme", THEMES)
def test_konsole_parses_and_has_all_sections(theme):
    cfg = configparser.ConfigParser()
    cfg.read_string(to_konsole(load_config(theme), theme))
    missing = [s for s in KONSOLE_SECTIONS if s not in cfg.sections()]
    assert not missing, f"{theme}: missing sections {missing}"
    assert cfg["General"]["Description"] == f"Spektra {theme.capitalize()}"


@pytest.mark.parametrize("theme", THEMES)
def test_konsole_colors_in_range_and_foreground_readable(theme):
    cfg = configparser.ConfigParser()
    cfg.read_string(to_konsole(load_config(theme), theme))
    bg = rgb_triplet(cfg["Background"]["Color"])
    fg = rgb_triplet(cfg["Foreground"]["Color"])
    for section in cfg.sections():
        if "Color" not in cfg[section]:
            continue
        rgb = rgb_triplet(cfg[section]["Color"])
        assert all(0 <= v <= 255 for v in rgb), f"{theme} [{section}] out of range"
    assert contrast(fg, bg) >= 4.5, f"{theme}: fg/bg contrast too low"


@pytest.mark.parametrize("theme", THEMES)
def test_iterm2_schema_matches_reference_key_set(theme):
    d = plistlib.loads(to_iterm2(load_config(theme), theme))
    assert set(d) == ITERM_KEYS, f"{theme}: key mismatch {sorted(set(d) ^ ITERM_KEYS)}"
    for key, color in d.items():
        assert set(color) >= set(COLOR_KEYS) | {"Color Space"}, f"{theme} {key}"
        assert color["Color Space"] == "sRGB", f"{theme} {key}"
        assert all(0 <= color[k] <= 1 for k in COLOR_KEYS), f"{theme} {key}"


@pytest.mark.parametrize("theme", THEMES)
def test_iterm2_round_trips_theme_colors(theme):
    from spektra.terminals import lighten, theme_slots

    cfg = load_config(theme)
    d = plistlib.loads(to_iterm2(load_config(theme), theme))
    assert plist_rgb(d["Background Color"]) == tuple(
        int(cfg["colors"]["bg"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
    )
    assert plist_rgb(d["Foreground Color"]) == tuple(
        int(cfg["colors"]["text"].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
    )
    # Ansi 1-6 match theme_slots(); the guard may lighten dark entries.
    assert [plist_rgb(d[f"Ansi {i} Color"]) for i in range(1, 7)] == theme_slots(cfg)[
        "normals"
    ]
    for raw_hex, normal in zip(cfg["palette"], theme_slots(cfg)["normals"]):
        raw = tuple(int(raw_hex.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        assert normal == raw or normal == lighten(raw, 0.35), f"{theme} {raw_hex}"


def test_targets_list():
    assert available_targets() == ["konsole", "iterm2", "opencode"]


def test_apply_writes_files(tmp_path):
    dest = apply("sakura", terminal="konsole", out=str(tmp_path / "x.colorscheme"))
    assert dest.endswith("x.colorscheme")
    paths = apply_all(terminal="iterm2", out=str(tmp_path))
    assert len(paths) == len(THEMES)
    assert all(p.endswith(".itermcolors") for p in paths)


@pytest.mark.parametrize("theme", THEMES)
def test_opencode_is_valid_theme_json(theme):
    data = json.loads(to_opencode(load_config(theme), theme))
    assert data["$schema"] == "https://opencode.ai/theme.json"
    assert set(data["theme"]) == set(OPENCODE_ROLES)
    for role, src in OPENCODE_ROLES.items():
        assert data["theme"][role] == {"dark": src, "light": src}, f"{theme} {role}"
        assert src in data["defs"], f"{theme} {role} -> missing def {src}"
    for name, value in data["defs"].items():
        assert value.startswith("#") and len(value) == 7, f"{theme} def {name}"


@pytest.mark.parametrize("theme", THEMES)
def test_opencode_round_trips_theme_colors(theme):
    cfg = load_config(theme)
    data = json.loads(to_opencode(load_config(theme), theme))
    defs = data["defs"]
    assert defs["bg"] == cfg["colors"]["bg"].upper()
    assert defs["text"] == cfg["colors"]["text"].upper()
    assert defs["accent"] == cfg["colors"]["accent"]
    assert defs["secondary"] == cfg["colors"]["secondary"]
    for i, hex_color in enumerate(cfg["palette"]):
        assert defs[f"p{i}"] == hex_color.upper(), f"{theme} p{i}"


def test_apply_opencode_uses_lowercase_name(tmp_path):
    dest = apply("sakura", terminal="opencode", out=str(tmp_path / "out.json"))
    assert dest.endswith("out.json")
    with open(dest) as f:
        data = json.load(f)
    assert set(data["theme"]) == set(OPENCODE_ROLES)
    paths = apply_all(terminal="opencode", out=str(tmp_path))
    assert len(paths) == len(THEMES)
    assert all(p.endswith(".json") for p in paths)
    assert any(p.endswith("spektra-sakura.json") for p in paths)
