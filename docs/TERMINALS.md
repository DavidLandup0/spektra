# Spektra terminal themes

Use your favorite spektra theme in your terminal.

```bash
pip install "spektra[plotly]"
spektra apply sakura
```

That's it. The theme is installed, then follow the one follow-up step printed for your terminal.

## Commands

```bash
spektra list themes       # sakura, ember, neon, ash, raiden, mitsuki, nightshade, sky
spektra list targets      # konsole, iterm2, opencode
spektra apply sakura                  # auto-detect your terminal
spektra apply sakura -t konsole       # pick explicitly
spektra apply --all -t konsole        # install every theme at once
spektra apply sakura -t opencode      # write to ~/.config/opencode/themes/
```

Run `spektra --help` or `spektra apply --help` anytime — the same guide below ships in the CLI.

## What happens per terminal

**Konsole (Linux / KDE)**
Installs to `~/.local/share/konsole/Spektra-<Name>.colorscheme`.
Then: restart Konsole → Settings → Edit Current Profile → Appearance → pick `Spektra <Name>`.

**iTerm2 (macOS — the macOS path)**
Writes `Spektra-<Name>.itermcolors` (to `~/.local/share/spektra/` or your `-o DIR`).
Then: iTerm2 → Settings → Profiles → Colors → Color Presets → Import the file.

**OpenCode**
Installs to `~/.config/opencode/themes/spektra-<name>.json`.
Then: set `"theme": "spektra-sakura"` in `tui.json`, or run `/theme` inside opencode.
Spektra themes are dark-only, so light mode shows the same colors.

## Tips

- Don't know your theme name? `spektra list themes`.
- Want them all? `spektra apply --all` (add `-t konsole` if auto-detect guesses wrong).
- Sakura is light pink on near-black and works best on dark backgrounds.
