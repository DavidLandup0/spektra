"""Spektra command line interface."""

import argparse
import os

HELP_EPILOG = """examples:
  spektra list themes
  spektra apply sakura
  spektra apply --all -t konsole

  konsole: ~/.local/share/konsole/ (then pick it under Appearance)
  iterm2: ~/.local/share/spektra/ (then Import as Color Preset)
  opencode: ~/.config/opencode/themes/ (then /theme inside opencode)
"""


def build_parser():
    p = argparse.ArgumentParser(
        prog="spektra",
        description="Apply spektra themes to your terminal.",
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    lp = sub.add_parser("list", help="List themes or targets.")
    lp.add_argument("what", choices=["themes", "targets"], help="What to list.")

    ap = sub.add_parser("apply", help="Apply a theme to your terminal.")
    ap.add_argument(
        "theme",
        nargs="?",
        default=None,
        help="Theme name (see `spektra list themes`). Omit with --all.",
    )
    ap.add_argument("--all", action="store_true", help="Install every theme at once.")
    ap.add_argument(
        "-t",
        "--target",
        default=None,
        choices=["konsole", "iterm2", "opencode"],
        help="Target (default: auto-detect).",
    )
    ap.add_argument(
        "-o",
        "--out",
        default=None,
        help="Write file to DIR or exact path instead of installing.",
    )
    return p


def main(argv=None):
    from .terminals import apply, apply_all, available_targets, available_themes

    args = build_parser().parse_args(argv)
    if args.cmd == "list":
        items = available_themes() if args.what == "themes" else available_targets()
        print("\n".join(items))
        return 0
    if args.cmd == "apply":
        out = os.path.expanduser(args.out) if args.out else None
        if args.all:
            if out and not os.path.isdir(out):
                os.makedirs(out, exist_ok=True)
            apply_all(terminal=args.target, out=out)
            return 0
        if not args.theme:
            raise SystemExit(
                "error: give a theme name or use --all (see `spektra list themes`)"
            )
        from .terminals import EXT, detect_terminal

        dest = out
        if dest and os.path.isdir(dest):
            term = args.target or detect_terminal()
            if term == "opencode":
                fname = f"spektra-{args.theme}.json"
            else:
                fname = f"Spektra-{args.theme.capitalize()}.{EXT[term]}"
            dest = os.path.join(dest, fname)
        apply(args.theme, terminal=args.target, out=dest)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
