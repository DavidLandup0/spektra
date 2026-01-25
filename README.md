![](header/headers.gif)

<div align="center">
<p><i>Styles for Matplotlib, Seaborn and Plotly.</i></p>
</div>

<div align="center">
<a href="/examples">Examples</a>
</div>
<hr>


## Quickstart

```bash
pip install spektra
```

## Usage

```python
import spektra as sk
import matplotlib.pyplot as plt

# One of ['ember', 'neon', 'ash', 'raiden', 'sakura']
sk.style('ember')  

plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```


Quickview:

```python
print(sk.get_available_themes())
# ['sakura', 'neon', 'ash', 'raiden', 'ember']

print(sk.get_theme())
# ember

print(sk.get_cmap())
# <matplotlib.colors.LinearSegmentedColormap object at 0x10d6ae750>

print(sk.get_palette(n=5))
# ['#FF003C', '#FF00FF', '#00F3FF', '#FFEA00', '#00FF41']

# Theme config is in this dict.
print(sk.get_config())
# {'bg': '#050505',
# 'accent': '#FF003C',
# 'secondary': '#9D0025',
# 'text': '#FF003C',
# 'grid': '#1A0006',
# 'alpha': 0.4,
# 'op': 0.4,
# ...
```

## Theme Files

All theme files are stored under their respective `spektra/themes/{THEME_NAME}.json` file.
They're stored as JSON for ease of reusability between Maplotlib/Seaborn and Plotly.
`spektra` scans the directory, so adding a `.json` file to it will register a new theme.

## License
[Apache 2.0](LICENSE.md)