# ParaScout

ParaScout is a tool for evaluating and visualising how well a parameter space has been explored.

Simulation campaigns often involve running models across a high-dimensional parameter space. As the number of parameters increases, it becomes difficult to determine which regions have been densely sampled, which regions remain unexplored, and where future simulations would provide the greatest benefit.

ParaScout aims to provide a lightweight framework for:

* Loading parameter-space data from simulation campaigns
* Automatically identifying the dimensionality of the parameter space
* Generating appropriate visualisations for the data
* Exploring parameter-space coverage through 1D, 2D, and 3D projections
* Providing the foundations for future gap-finding and coverage metrics

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

Examples:

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

* Joint Scatter plots
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
ParaScout/
├── data/
│   ├── runs.csv
│   ├── simulations.txt
│   └── parameter_space.h5
├── src/
├── plots/
└── README.md
```

ParaScout will automatically scan the directory and identify compatible files.

---

## Motivation

As simulation campaigns continue to grow in size and complexity, understanding where simulations have already been performed becomes increasingly important. ParaScout is designed to provide a simple and extensible framework for exploring parameter-space coverage and identifying regions that may benefit from additional sampling.
