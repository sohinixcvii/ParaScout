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
git clone https://github.com/sohinixcvii/ParaScout.git
cd ParaScout
pip install -e .
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
visualiser/
├── parascout/                    # Installable Python package
│   ├── __init__.py               # Public API and visualise() wrapper
│   ├── dispatcher.py             # Routes arrays to plotting functions
│   └── plotting_functions.py     # plot_bubble_map, plot_volumetric_density
├── data/                         # Place input data files here
├── dev_tests/                    # Developer notebooks
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
| 1-D or (N, 1) | `plot_1d` *(planned)* |
| (N, 2) | `plot_2d` *(planned)* |
| (N, 3+) | `plot_bubble_map` |

`data_list` must contain between 2 and 5 arrays.

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

## Project Workflow

The current development plan consists of four stages.

### 1. Data Discovery and Loading

ParaScout scans the `data/` directory and automatically identifies supported data files.

Tasks:

* Search the `data/` directory
* Identify file type
* Load supported file formats
* Extract parameter labels
* Store parameter values in a standard internal format

Supported file formats:

* Text files (`.txt`, `.csv`, `.dat`)
* HDF5 files (`.h5`, `.hdf5`)

### 2. Parameter-Space Analysis

Once the data are loaded, ParaScout determines the dimensionality of the parameter space.

| Number of Parameters | Action                                                                    |
| -------------------- | ------------------------------------------------------------------------- |
| 1                    | Create 1D visualisations                                                  |
| 2                    | Create 2D visualisations                                                  |
| 3                    | Create 3D visualisations                                                  |
| >3                   | Create sets of parameter combinations containing at most three parameters |

### 3. Plot Selection

ParaScout automatically determines which visualisation methods are appropriate for the dimensionality of the data.

Possible plot types include:

#### 1D

* Kernel density estimates

#### 2D

* Joint scatter plots
* Hexbin plots

#### 3D

* Volumetric density fields
* Bubble maps
* Interactive parameter-space visualisations

### 4. Plot Generation

The plotting module generates visualisations using the selected plotting strategy.

Responsibilities include:

* Axis labelling
* Parameter scaling
* Density estimation
* Interactive visualisation generation
* Figure export

Generated plots are saved to the output directory and may also be displayed interactively.

---

## User Instructions

### Supported File Types

Input files must be one of the following formats:

* `.txt`
* `.csv`
* `.dat`
* `.h5`
* `.hdf5`

### Parameter Labels

The first row of the input file must contain parameter labels.

These labels will be used automatically for axis titles and plot annotations.

### Data Location

All input files should be placed inside the `data/` directory:

```text
visualiser/
├── data/
│   ├── runs.csv
│   ├── simulations.txt
│   └── parameter_space.h5
├── parascout/
├── dev_tests/
└── README.md
```

ParaScout will automatically scan the directory and identify compatible files.

---

## Motivation

As simulation campaigns continue to grow in size and complexity, understanding where simulations have already been performed becomes increasingly important. ParaScout is designed to provide a simple and extensible framework for exploring parameter-space coverage and identifying regions that may benefit from additional sampling.
