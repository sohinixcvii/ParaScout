# ParaScout

ParaScout is a tool for evaluating and visualising how well a parameter space has been explored.

Simulation campaigns often involve running models across a high-dimensional parameter space. As the number of parameters increases, it becomes difficult to determine which regions have been densely sampled, which regions remain unexplored, and where future simulations would provide the greatest benefit.

ParaScout aims to provide a lightweight framework for:

* Loading parameter-space data from simulation campaigns
* Automatically identifying the dimensionality of the parameter space
* Generating appropriate visualisations for the data
* Exploring parameter-space coverage through 1D, 2D, and 3D projections
* Providing the foundations for future gap-finding and coverage metrics

---

## Installation

```bash
pip install parascout
```

### Dependencies

* `numpy` — array handling
* `plotly` — interactive visualisations
* `scipy` — Gaussian KDE for density estimation

---

## Quick Start

```python
import numpy as np
from parascout import visualise

# Each array in the list is one parameter-space projection
rng = np.random.default_rng(0)
data = rng.random((100, 3))          # (N, 3): x, y, size

figs = visualise([data, data], labels=("x", "y", "z"))
figs[0].show()
```

---

## Package Structure

```text
parascout/
├── parascout/                    # Installable Python package
│   ├── __init__.py               # Public API and visualise() wrapper
│   ├── dispatcher.py             # Routes arrays to plotting functions
│   └── plotting_functions.py     # plot_1d, plot_2d, plot_bubble_map, plot_volumetric_density
├── scripts/                      # Utility scripts (reference only)
├── test_data_multi_dimension/    # Sample 1D–5D test datasets
├── pyproject.toml                # Build configuration and metadata
└── README.md
```

---

## Public API

### `visualise(data_list, labels=None)`

Top-level entry point. Accepts a list of NumPy arrays and dispatches each to
the appropriate plotting function based on its shape.

```python
from parascout import visualise

figs = visualise(data_list, labels=("param_a", "param_b", "param_c"))
```

| Array shape | Routed to |
| ----------- | --------- |
| 1-D or (N, 1) | `plot_1d` |
| (N, 2) | `plot_2d` |
| (N, 3+) | `plot_bubble_map` |

`data_list` must contain between 2 and 5 arrays.

---

### `plot_1d(params, labels=("x",), use_kde=True, ...)`

Create a 1-D distribution plot from a 1-D or (N, 1) parameter array. Renders
a histogram with an optional Gaussian KDE curve scaled to match histogram area.

```python
from parascout import plot_1d

fig = plot_1d(params, labels=("temperature",))
fig.show()
```

---

### `plot_2d(params, labels=("x", "y"), ...)`

Create a 2-D scatter plot from an (N, 2) parameter array. Points are coloured
by their y-value using a configurable Plotly colorscale.

```python
from parascout import plot_2d

fig = plot_2d(params, labels=("alpha", "beta"))
fig.show()
```

---

### `plot_bubble_map(params, labels=("x", "y", "size"), ...)`

Create a 2D bubble map from an (N, 3) parameter array. Bubble position is set
by the first two columns; bubble size is proportional to the third column.

```python
from parascout import plot_bubble_map

fig = plot_bubble_map(params, labels=("alpha", "beta", "gamma"))
fig.show()
```

---

### `plot_volumetric_density(params, labels=("x", "y", "z"), ...)`

Create an interactive 3D volumetric density field from an (N, 3) parameter
array using Gaussian KDE.

```python
from parascout import plot_volumetric_density

fig = plot_volumetric_density(params, labels=("T", "rho", "Z"))
fig.show()
```

---

### `plot_dispatcher(data_list, labels=None)`

Low-level dispatcher called internally by `visualise()`. Can be used directly
if finer control is needed.

---

## Loading Data

ParaScout does not auto-scan directories. Load your data with NumPy and pass it directly to the plotting functions.

Text files with a header row of column labels can be loaded like this:

```python
import numpy as np

def load_labelled_txt(path):
    with open(path) as f:
        labels = f.readline().split()
    data = np.loadtxt(path, skiprows=1)
    return labels, data

labels, data = load_labelled_txt("my_simulations.txt")
```

---

## Roadmap

Planned features for future releases:

* Automatic data discovery and loading from a `data/` directory
* HDF5 file support (`.h5`, `.hdf5`)
* Coverage metrics and quantitative gap-finding algorithms
* `pytest`-based test suite

---

## Motivation

As simulation campaigns continue to grow in size and complexity, understanding where simulations have already been performed becomes increasingly important. ParaScout is designed to provide a simple and extensible framework for exploring parameter-space coverage and identifying regions that may benefit from additional sampling.
