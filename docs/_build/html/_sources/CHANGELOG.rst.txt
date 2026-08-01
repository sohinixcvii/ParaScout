Changelog
=========

All notable changes to ParaScout are documented here.
The format follows `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_.

----

0.1.1 — 2026-06-26
-------------------

1-D and 2-D plotting functions implemented; utility scripts reorganised.

Added
~~~~~

- :func:`~parascout.plot_1d` — interactive 1-D distribution plot
  (``plotly.graph_objects.Histogram`` + ``go.Scatter`` KDE overlay) for
  1-D or ``(N, 1)`` parameter arrays. A Gaussian KDE curve scaled to match
  histogram area is overlaid by default; it can be disabled via
  ``use_kde=False``.
- :func:`~parascout.plot_2d` — interactive 2-D scatter plot
  (``plotly.graph_objects.Scatter``) for ``(N, 2)`` parameter arrays.
  Points are coloured by their y-value using a configurable Plotly
  colorscale.
- ``scripts/`` directory containing ``combinations.py`` and
  ``generating_test_data_module.py``, preserved for reference.

Changed
~~~~~~~

- :func:`~parascout.plot_dispatcher` now routes 1-D / ``(N, 1)`` arrays to
  :func:`~parascout.plot_1d` and ``(N, 2)`` arrays to
  :func:`~parascout.plot_2d`. Previously these shapes raised a
  ``NameError``; all shapes in the 1–3+ column range are now handled.
- ``__init__.py`` updated to export :func:`~parascout.plot_1d` and
  :func:`~parascout.plot_2d` as part of the public API.
- ``combinations.py`` and ``generating_test_data_module.py`` moved from the
  repository root into the new ``scripts/`` directory.

Removed
~~~~~~~

- ``plotting1D2D.py`` — legacy ``matplotlib``/``seaborn`` prototype for 1-D
  and 2-D plots, superseded by the new Plotly implementations above.

----

0.1.0 — 2026-06-25
-------------------

First public release. The repository was restructured into an installable
package, core plotting functions were implemented, and Sphinx documentation
was added.

Added
~~~~~

- ``parascout/`` package directory with ``__init__.py`` exposing the public
  API: :func:`~parascout.visualise`, :func:`~parascout.plot_dispatcher`,
  :func:`~parascout.plot_bubble_map`, and
  :func:`~parascout.plot_volumetric_density`.
- :func:`~parascout.plot_bubble_map` — interactive 2-D bubble map
  (``plotly.graph_objects.Scatter``) for ``(N, 3)`` parameter arrays.
  Bubble position is set by the first two columns; bubble size and colour are
  driven by the third column with linear normalisation.
- :func:`~parascout.plot_volumetric_density` — interactive 3-D volumetric
  density plot (``plotly.graph_objects.Volume``) for ``(N, 3)`` arrays.
  Uses a Gaussian KDE (``scipy.stats.gaussian_kde``) evaluated on a
  configurable voxel grid; raw sample points are overlaid as a
  ``Scatter3d`` trace.
- :func:`~parascout.plot_dispatcher` — shape-based routing function that
  dispatches each array in a list to the appropriate plotting function.
  Validates that the list contains 2–5 arrays.
- :func:`~parascout.visualise` — top-level wrapper around
  :func:`~parascout.plot_dispatcher`.
- ``pyproject.toml`` with project metadata, MIT licence declaration, and
  runtime dependencies (``numpy``, ``plotly``, ``scipy``).
- ``.gitignore`` covering Python caches, virtual environments, Jupyter
  checkpoints, distribution artefacts, and generated HTML plots.
- ``docs/`` directory with a Sphinx configuration (RTD theme, ``autodoc``,
  ``napoleon`` extensions) and initial API reference page.
- Comprehensive ``README.md`` with installation instructions, quick-start
  example, full API table, routing table, and four-stage development roadmap.

Changed
~~~~~~~

- Source files moved from ``src/`` into the ``parascout/`` package directory.
- Repository cleaned up for publication: removed development notebooks
  (``combination_of_parameters.ipynb``, ``data_test.ipynb``,
  ``dev_tests/sohini_dev.ipynb``), scratch files (``Data_Reading.py``,
  ``hello_kutay.txt``, ``hello_sohini.txt``), and cached ``.DS_Store``
  binaries.

----

0.0.3 — 2026-06-24
-------------------

Combination-generation logic extracted from a notebook into importable
Python modules.

Added
~~~~~

- ``combinations.py`` — ``make_column_combinations()`` and
  ``make_all_column_combinations()`` functions for generating dimension-wise
  projections (grouped as ``"1D"``, ``"2D"``, ``"3D"``, etc.) from a
  multi-dimensional dataset.
- ``generating_test_data_module.py`` — ``read_txt_with_labels()`` helper
  that parses labelled text files (first row = column names, remaining rows =
  numeric values) and returns labels and data separately.
- ``make_column_combinations()`` extended to accept a dictionary mapping
  dimension labels to arrays, replacing the earlier positional interface.

Changed
~~~~~~~

- ``combination_of_parameters.ipynb`` replaced by the standalone Python
  modules above, keeping logic reusable outside a notebook environment.

----

0.0.2 — 2026-06-23
-------------------

Core plotting infrastructure added; multi-dimensional test data committed;
project renamed.

Added
~~~~~

- ``src/plotting_functions.py`` with initial implementations of
  ``plot_volumetric_density`` and ``plot_bubble_map`` (later promoted to the
  ``parascout`` package in 0.1.0).
- ``src/dispatcher.py`` with shape-based routing logic for 1-D, 2-D, and
  3-D+ arrays.
- ``test_data_multi_dimension/`` directory containing five labelled text
  files (``1D.txt`` – ``5D.txt``), each with ~6 800 rows of sample
  parameter data, for testing projections across one to five dimensions.
- ``data/params_reion`` — real reionisation parameter dataset used as a
  reference input during development.
- ``combination_of_parameters.ipynb`` — notebook prototype for generating
  column-wise parameter combinations (superseded in 0.0.3).

Changed
~~~~~~~

- Project renamed from **visualiser** to **ParaScout** (reflected in
  ``README.md``).
- ``README.md`` updated with project description and contributor information.

----

0.0.1 — 2026-06-22
-------------------

Repository initialised; early collaborative experimentation.

Added
~~~~~

- Initial repository created on GitHub (``sohinixcvii/visualiser``).
- Placeholder text files committed for branch and merge-conflict workflow
  practice (``hello_sohini.txt``).

----

Unreleased
----------

The items below are planned but not yet implemented.

Planned
~~~~~~~

- Coverage metrics — quantitative gap-finding scores to complement the visual
  outputs.
- ``pytest`` test suite exercising the public API against the existing test
  data files.
