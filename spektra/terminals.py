"""Export themes to terminal color schemes."""

import json
import os
import platform
import plistlib
import shutil

from .core import available_themes, load_config

TARGETS = ("konsole", "iterm2", "opencode")

FOLLOW_UPS = {
    "konsole": "Restart Konsole, then Settings > Edit Current Profile > Appearance > pick Spektra {Name}.",
    "iterm2": "iTerm2 > Settings > Profiles > Colors > Color Presets > Import {path}.",
    "opencode": 'Set "theme": "spektra-{name}" in tui.json, or run /theme inside opencode.',
}


def available_targets():
    return list(TARGETS)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def lighten(c, a):
    return tuple(min(255, int(v + (255 - v) * a)) for v in c)


def darken(c, a):
    return tuple(max(0, int(v * (1 - a))) for v in c)


def theme_slots(cfg):
    bg = hex_to_rgb(cfg["colors"]["bg"])
    tx = hex_to_rgb(cfg["colors"]["text"])
    gr = hex_to_rgb(cfg["colors"]["grid"])
    pal = [hex_to_rgb(x) for x in cfg["palette"]]
    normals = [lighten(p, 0.35) if sum(p) / 3 < 60 else p for p in pal]
    white = tx if sum(tx) / 3 > 60 else lighten(tx, 0.25)
    return {
        "bg": bg,
        "fg": tx,
        "black": gr,
        "pal": pal,
        "normals": normals,
        "white": white,
    }


def format_rgb(c):
    return f"{c[0]},{c[1]},{c[2]}"


def to_konsole(cfg, name):
    s = theme_slots(cfg)
    F, L, D = format_rgb, lighten, darken
    out = [
        f"[Background]\nColor={F(s['bg'])}",
        f"[BackgroundFaint]\nColor={F(D(s['bg'], 0.1))}",
        f"[BackgroundIntense]\nColor={F(L(s['bg'], 0.12))}",
        f"[Color0]\nColor={F(s['black'])}",
        f"[Color0Faint]\nColor={F(D(s['black'], 0.25))}",
        f"[Color0Intense]\nColor={F(L(s['black'], 0.45))}",
    ]
    for i in range(6):
        out += [
            f"[Color{i + 1}]\nColor={F(s['normals'][i])}",
            f"[Color{i + 1}Faint]\nColor={F(D(s['pal'][i], 0.45))}",
            f"[Color{i + 1}Intense]\nColor={F(L(s['normals'][i], 0.3))}",
        ]
    out += [
        f"[Color7]\nColor={F(s['white'])}",
        f"[Color7Faint]\nColor={F(D(s['white'], 0.4))}",
        "[Color7Intense]\nColor=255,255,255",
        f"[Foreground]\nColor={F(s['fg'])}",
        f"[ForegroundFaint]\nColor={F(D(s['fg'], 0.4))}",
        "[ForegroundIntense]\nColor=255,255,255",
        f"[General]\nDescription=Spektra {name.capitalize()}\nOpacity=1\nWallpaper=",
    ]
    return "\n\n".join(out) + "\n"


def plist_color(c, alpha=1.0):
    r, g, b = (v / 255 for v in c)
    return {
        "Red Component": r,
        "Green Component": g,
        "Blue Component": b,
        "Alpha Component": alpha,
        "Color Space": "sRGB",
    }


def to_iterm2(cfg, name):
    s = theme_slots(cfg)
    normal = [s["black"]] + s["normals"] + [s["white"]]
    bright = [lighten(a, 0.3) for a in normal]
    d = {}
    for i, c in enumerate(normal + bright):
        d[f"Ansi {i} Color"] = plist_color(c)
    d.update(
        {
            "Background Color": plist_color(s["bg"]),
            "Foreground Color": plist_color(s["fg"]),
            "Bold Color": plist_color(lighten(s["fg"], 0.15)),
            "Cursor Color": plist_color(s["normals"][0]),
            "Cursor Text Color": plist_color(s["bg"]),
            "Cursor Guide Color": plist_color(lighten(s["bg"], 0.1)),
            "Selection Color": plist_color(lighten(s["bg"], 0.18)),
            "Selected Text Color": plist_color(s["fg"]),
        }
    )
    return plistlib.dumps(d, fmt=plistlib.FMT_XML)


EXT = {"konsole": "colorscheme", "iterm2": "itermcolors", "opencode": "json"}


def rgb_hex(c):
    return f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}"


OPENCODE_ROLES = {
    "primary": "accent",
    "secondary": "secondary",
    "accent": "accent",
    "error": "p0",
    "warning": "p3",
    "success": "p4",
    "info": "accent",
    "text": "text",
    "textMuted": "muted",
    "background": "bg",
    "backgroundPanel": "panel",
    "backgroundElement": "element",
    "border": "border",
    "borderActive": "accent",
    "borderSubtle": "panel",
    "diffAdded": "p4",
    "diffRemoved": "p0",
    "diffContext": "muted",
    "diffHunkHeader": "muted",
    "diffHighlightAdded": "p4",
    "diffHighlightRemoved": "p0",
    "diffAddedBg": "panel",
    "diffRemovedBg": "panel",
    "diffContextBg": "panel",
    "diffLineNumber": "muted",
    "diffAddedLineNumberBg": "panel",
    "diffRemovedLineNumberBg": "panel",
    "markdownText": "text",
    "markdownHeading": "accent",
    "markdownLink": "secondary",
    "markdownLinkText": "p1",
    "markdownCode": "p4",
    "markdownBlockQuote": "muted",
    "markdownEmph": "p0",
    "markdownStrong": "p3",
    "markdownHorizontalRule": "muted",
    "markdownListItem": "accent",
    "markdownListEnumeration": "p1",
    "markdownImage": "secondary",
    "markdownImageText": "p1",
    "markdownCodeBlock": "text",
    "syntaxComment": "muted",
    "syntaxKeyword": "secondary",
    "syntaxFunction": "accent",
    "syntaxVariable": "p1",
    "syntaxString": "p4",
    "syntaxNumber": "p5",
    "syntaxType": "p2",
    "syntaxOperator": "secondary",
    "syntaxPunctuation": "text",
}


def to_opencode(cfg, name):
    pal = [hex_to_rgb(x) for x in cfg["palette"]]
    bg = hex_to_rgb(cfg["colors"]["bg"])
    tx = hex_to_rgb(cfg["colors"]["text"])
    gr = hex_to_rgb(cfg["colors"]["grid"])
    defs = {
        "bg": rgb_hex(bg),
        "text": rgb_hex(tx),
        "accent": cfg["colors"]["accent"],
        "secondary": cfg["colors"]["secondary"],
        "muted": rgb_hex(darken(tx, 0.35)),
        "panel": rgb_hex(gr),
        "element": rgb_hex(lighten(bg, 0.1)),
        "border": rgb_hex(lighten(bg, 0.15)),
    }
    for i, p in enumerate(pal):
        defs[f"p{i}"] = rgb_hex(p)
    theme = {role: {"dark": src, "light": src} for role, src in OPENCODE_ROLES.items()}
    return (
        json.dumps(
            {"$schema": "https://opencode.ai/theme.json", "defs": defs, "theme": theme},
            indent=2,
        )
        + "\n"
    )


def detect_terminal():
    if platform.system() == "Darwin":
        return "iterm2"
    if os.environ.get("KDE_SESSION_VERSION") or shutil.which("konsole"):
        return "konsole"
    raise ValueError("Could not auto-detect terminal. Use -t konsole|iterm2|opencode.")


def config_dir():
    base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(base, "opencode", "themes")


def default_path(theme, terminal):
    cap = theme.capitalize()
    home = os.path.expanduser("~")
    if terminal == "konsole":
        return os.path.join(home, ".local/share/konsole", f"Spektra-{cap}.colorscheme")
    if terminal == "opencode":
        return os.path.join(config_dir(), f"spektra-{theme}.json")
    return os.path.join(home, ".local/share/spektra", f"Spektra-{cap}.itermcolors")


def apply(theme, terminal=None, out=None):
    terminal = terminal or detect_terminal()
    if terminal not in TARGETS:
        raise ValueError(f"Unknown terminal {terminal!r}. Choose from {TARGETS}.")
    themes = available_themes()
    if theme not in themes:
        raise ValueError(f"Unknown theme {theme!r}. Choose from {themes}.")
    cfg = load_config(theme)
    fn = {"konsole": to_konsole, "iterm2": to_iterm2, "opencode": to_opencode}[terminal]
    data = fn(cfg, theme)
    dest = os.path.expanduser(out) if out else default_path(theme, terminal)
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(dest, mode) as f:
        f.write(data)
    msg = FOLLOW_UPS[terminal].format(Name=theme.capitalize(), name=theme, path=dest)
    print(f"Wrote {dest}\n{msg}")
    return dest


def apply_all(terminal=None, out=None):
    terminal = terminal or detect_terminal()
    paths = []
    for theme in available_themes():
        dest = None
        if out:
            if terminal == "opencode":
                fname = f"spektra-{theme}.json"
            else:
                fname = f"Spektra-{theme.capitalize()}.{EXT[terminal]}"
            dest = os.path.join(os.path.expanduser(out), fname)
        paths.append(apply(theme, terminal=terminal, out=dest))
    return paths
