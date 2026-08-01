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

rng = np.random.default_rng(0)
params_2d = rng.random((200, 2))   # (N, 2) → routed to plot_2d
params_3d = rng.random((200, 3))   # (N, 3) → routed to plot_bubble_map

figs = visualise([params_2d, params_3d], labels=("x", "y", "size"))
figs[0].show()   # 2D scatter
figs[1].show()   # bubble map
```

---

## Package Structure

```text
ParaScout/
├── parascout/                    # Installable Python package
│   ├── __init__.py               # Public API and visualise() wrapper
│   ├── dispatcher.py             # Routes arrays to plotting functions
│   └── plotting_functions.py     # plot_1d, plot_2d, plot_bubble_map, plot_volumetric_density
├── scripts/                      # Utility scripts (reference only)
├── test_data_multi_dimension/    # Sample 1D–5D test datasets
├── docs/                         # Sphinx documentation source
├── demo_notebook.ipynb           # Worked examples for every API function
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
array using Gaussian KDE. The density volume is overlaid with the raw sample
points as a 3D scatter.

> **Note:** `visualise()` routes (N, 3+) arrays to `plot_bubble_map`, not
> `plot_volumetric_density`. Call this function directly when you want the
> volumetric view.

```python
from parascout import plot_volumetric_density

fig = plot_volumetric_density(params, labels=("mhalo", "rmfp", "nion"))
fig.show()
```

---

### `plot_dispatcher(data_list, labels=None)`

Low-level dispatcher called internally by `visualise()`. Can be used directly
if finer control is needed.

---

## Examples

The examples below use synthetic data generated with NumPy. All figures are
interactive Plotly visualisations; call `.show()` to open them in a browser.
Parameter names (`mhalo`, `rmfp`, `nion`) mirror the sample datasets in
`test_data_multi_dimension/`.

### 1D: parameter distribution

```python
import numpy as np
from parascout import plot_1d

rng = np.random.default_rng(42)
mhalo = rng.uniform(100, 500, 400)

fig = plot_1d(mhalo, labels=("mhalo",))
fig.show()
```

### 2D: scatter plot

```python
import numpy as np
from parascout import plot_2d

rng = np.random.default_rng(42)
params = rng.uniform(low=[100, 10], high=[500, 200], size=(400, 2))

fig = plot_2d(params, labels=("mhalo", "rmfp"))
fig.show()
```

### Bubble map: two-parameter plane with a third encoded dimension

Each bubble's position encodes two parameters; its size and colour encode a
third. This is the primary view for spotting gaps in 3-parameter projections.

```python
import numpy as np
from parascout import plot_bubble_map

rng = np.random.default_rng(42)
params = rng.uniform(low=[100, 10, 5], high=[500, 200, 50], size=(400, 3))

fig = plot_bubble_map(params, labels=("mhalo", "rmfp", "nion"))
fig.show()
```

### Volumetric density: 3D coverage map

```python
import numpy as np
from parascout import plot_volumetric_density

rng = np.random.default_rng(42)
params = rng.uniform(low=[100, 10, 5], high=[500, 200, 50], size=(400, 3))

fig = plot_volumetric_density(params, labels=("mhalo", "rmfp", "nion"))
fig.show()
```

### Comparing multiple campaigns with `visualise()`

Pass 2–5 arrays to get back one figure per campaign. Each array can have a
different shape — routing is automatic.

```python
import numpy as np
from parascout import visualise

rng = np.random.default_rng(0)

uniform   = rng.uniform(low=[100, 10, 5], high=[500, 200, 50], size=(200, 3))
clustered = rng.multivariate_normal([200, 50, 20], np.diag([2000, 400, 50]), size=200)

figs = visualise([uniform, clustered], labels=("mhalo", "rmfp", "nion"))
figs[0].update_layout(title="Uniform Sampling")
figs[1].update_layout(title="Clustered Sampling")

figs[0].show()
figs[1].show()
```

A fully worked walkthrough of every API function, including higher-dimensional
projections and real simulation data, is available in `demo_notebook.ipynb`.

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
