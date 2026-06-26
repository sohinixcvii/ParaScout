API Reference
=============

.. contents:: Contents
   :local:
   :depth: 2


Overview
--------

**ParaScout** is a lightweight Python library for evaluating and visualising
how well a parameter space has been explored during simulation campaigns.
Given a collection of NumPy arrays — each representing a set of simulation
samples in some projection of the full parameter space — ParaScout dispatches
each array to an appropriate interactive `Plotly <https://plotly.com/python/>`_
visualisation and returns the figures for inspection or export.

The library currently targets parameter-space projections of two or three
dimensions, with one- and two-dimensional plots planned for a future release.


Installation
------------

Install directly from the repository using ``pip``::

    git clone https://github.com/sohinixcvii/ParaScout.git
    cd ParaScout
    pip install .

**Runtime dependencies** (installed automatically):

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Package
     - Purpose
   * - ``numpy``
     - Array manipulation and finite-value filtering
   * - ``plotly``
     - Interactive HTML figures (2-D and 3-D)
   * - ``scipy``
     - Gaussian KDE for the volumetric density plot

Python 3.10 or later is required.


Quick Start
-----------

.. code-block:: python

    import numpy as np
    from parascout import visualise

    rng = np.random.default_rng(0)

    # Two (100, 3) arrays — each column is one parameter
    data_a = rng.random((100, 3))
    data_b = rng.random((100, 3))

    figs = visualise([data_a, data_b], labels=("alpha", "beta", "gamma"))

    figs[0].show()   # opens an interactive bubble map in the browser
    figs[1].show()


Input Data Format
-----------------

Each array passed to :func:`visualise` or :func:`plot_dispatcher` must be a
2-D ``numpy.ndarray`` of shape ``(N, D)``, where:

* ``N`` — number of simulation samples (rows).
* ``D`` — number of parameters in the projection (columns); currently 3 is
  the supported value for the implemented plots.

Rows containing ``NaN`` or infinite values are silently dropped before
plotting.

If you store parameter data in text files, the expected layout is::

    label_1  label_2  label_3
    0.142    0.853    0.219
    0.437    0.021    0.764
    ...

The first row contains space- or tab-separated column labels; subsequent rows
contain the numeric values.


Dispatch Routing
----------------

:func:`visualise` and :func:`plot_dispatcher` inspect the shape of each array
and select a plotting function automatically:

.. list-table::
   :header-rows: 1
   :widths: 30 40 30

   * - Array shape
     - Function called
     - Status
   * - 1-D or ``(N, 1)``
     - ``plot_1d``
     - Planned — not yet implemented
   * - ``(N, 2)``
     - ``plot_2d``
     - Planned — not yet implemented
   * - ``(N, 3)`` or wider
     - :func:`plot_bubble_map`
     - Available

The list passed to :func:`visualise` must contain **between 2 and 5 arrays**
(inclusive); fewer than 2 or more than 5 raise a ``ValueError``.


Public API
----------

visualise
~~~~~~~~~

.. code-block:: python

    parascout.visualise(data_list, labels=None)

Top-level entry point for ParaScout. Wraps :func:`plot_dispatcher` and
returns one interactive Plotly figure per input array.

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Name
     - Type
     - Description
   * - ``data_list``
     - ``list[numpy.ndarray]``
     - List of 2–5 parameter arrays. Each element is dispatched independently
       to the appropriate plotting function based on its shape.
   * - ``labels``
     - ``list[str] | None``
     - Axis labels forwarded to the underlying plotting function.
       ``None`` falls back to the per-function defaults (``"x"``, ``"y"``,
       ``"size"`` / ``"z"``).

**Returns**

``list[plotly.graph_objects.Figure]`` — one figure per array in
``data_list``, in the same order.

**Raises**

* ``ValueError`` — if ``len(data_list)`` is less than 2 or greater than 5.
* ``ValueError`` — if an array has an unsupported shape.

**Example**

.. code-block:: python

    import numpy as np
    from parascout import visualise

    rng = np.random.default_rng(42)
    data = rng.random((200, 3))

    figs = visualise([data, data], labels=("x", "y", "z"))
    figs[0].show()


----

plot_dispatcher
~~~~~~~~~~~~~~~

.. code-block:: python

    parascout.plot_dispatcher(data_list, labels=None)

Low-level dispatcher. Iterates over ``data_list``, inspects each array's
shape, and calls the matching plotting function. This function is called
internally by :func:`visualise`; use it directly when you want finer control
without the :func:`visualise` wrapper.

**Parameters** and **Returns** are identical to :func:`visualise`.


----

plot_bubble_map
~~~~~~~~~~~~~~~

.. code-block:: python

    parascout.plot_bubble_map(
        params,
        labels=("x", "y", "size"),
        max_marker_size=40,
        opacity=0.7,
        colorscale="Viridis",
        padding_fraction=0.05,
    )

Create a 2-D bubble map from an ``(N, 3)`` parameter array. The first two
columns determine each bubble's position on the x- and y-axes; the third
column determines bubble size and colour.

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Name
     - Type / Default
     - Description
   * - ``params``
     - ``ndarray (N, 3)``
     - Parameter array. Column 0 → x position, column 1 → y position,
       column 2 → bubble size and colour. Rows with non-finite values are
       dropped automatically. Must have at least 3 columns; extra columns
       beyond index 2 are ignored.
   * - ``labels``
     - ``tuple[str, str, str]``
       ``("x", "y", "size")``
     - Labels for the x-axis, y-axis, and the colorbar (size parameter).
   * - ``max_marker_size``
     - ``int | float``
       ``40``
     - Maximum bubble diameter in pixels. Sizes are scaled linearly so that
       the row with the largest third-column value maps exactly to this
       diameter.
   * - ``opacity``
     - ``float``
       ``0.7``
     - Opacity of the bubble markers (0 = transparent, 1 = opaque).
   * - ``colorscale``
     - ``str``
       ``"Viridis"``
     - Any named
       `Plotly colorscale <https://plotly.com/python/builtin-colorscales/>`_,
       e.g. ``"Plasma"``, ``"Cividis"``, ``"RdBu"``.
   * - ``padding_fraction``
     - ``float``
       ``0.05``
     - Fractional whitespace added to each axis limit so that edge points
       are not clipped. A value of ``0.05`` pads by 5 % of the data range.

**Returns**

``plotly.graph_objects.Figure`` — interactive 2-D scatter plot with a
Plotly ``Scatter`` trace.

**Raises**

* ``ValueError`` — if ``params`` is not 2-D.
* ``ValueError`` — if ``params`` has fewer than 3 columns.

**Example**

.. code-block:: python

    import numpy as np
    from parascout import plot_bubble_map

    rng = np.random.default_rng(0)
    data = rng.random((150, 3))

    fig = plot_bubble_map(
        data,
        labels=("Temperature", "Pressure", "Luminosity"),
        max_marker_size=50,
        colorscale="Plasma",
    )
    fig.show()


----

plot_volumetric_density
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    parascout.plot_volumetric_density(
        params,
        labels=("x", "y", "z"),
        grid_size=40,
        opacity=0.12,
        surface_count=15,
        bandwidth=None,
        padding_fraction=0.05,
    )

Create a 3-D volumetric density plot from an ``(N, 3)`` parameter array.
A Gaussian kernel density estimate (KDE) is evaluated on a regular
``grid_size × grid_size × grid_size`` voxel grid. The resulting density
field is rendered as a semi-transparent isosurface volume, with the original
sample points overlaid as black markers.

**Parameters**

.. list-table::
   :header-rows: 1
   :widths: 22 20 58

   * - Name
     - Type / Default
     - Description
   * - ``params``
     - ``ndarray (N, 3)``
     - Parameter array. Each row is one simulation sample; the three columns
       correspond to the x, y, and z axes. Rows with non-finite values are
       dropped automatically.
   * - ``labels``
     - ``tuple[str, str, str]``
       ``("x", "y", "z")``
     - Labels for the x-, y-, and z-axes of the 3-D scene.
   * - ``grid_size``
     - ``int``
       ``40``
     - Number of equally spaced grid points along each axis. Higher values
       produce smoother density fields at the cost of increased memory and
       compute time (memory scales as ``grid_size ** 3``).
   * - ``opacity``
     - ``float``
       ``0.12``
     - Global opacity of the density volume. Low values (0.05–0.20) work
       well for revealing interior structure.
   * - ``surface_count``
     - ``int``
       ``15``
     - Number of isosurface contours drawn inside the volume. More contours
       give finer density resolution in the visualisation.
   * - ``bandwidth``
     - ``float | None``
       ``None``
     - KDE bandwidth passed to ``scipy.stats.gaussian_kde``. ``None`` uses
       Scott's rule (the SciPy default), which is appropriate for most cases.
       Pass a positive float to override.
   * - ``padding_fraction``
     - ``float``
       ``0.05``
     - Fractional whitespace added to each axis limit (identical semantics to
       the same parameter in :func:`plot_bubble_map`).

**Returns**

``plotly.graph_objects.Figure`` — interactive 3-D figure containing a
``go.Volume`` density trace and a ``go.Scatter3d`` trace of the raw
sample points.

**Raises**

* ``ValueError`` — if ``params`` is not 2-D.
* ``ValueError`` — if ``params`` does not have exactly 3 columns.

**Example**

.. code-block:: python

    import numpy as np
    from parascout import plot_volumetric_density

    rng = np.random.default_rng(7)
    # Clustered sample in 3-D parameter space
    data = np.vstack([
        rng.normal(loc=[0.3, 0.3, 0.3], scale=0.1, size=(80, 3)),
        rng.normal(loc=[0.7, 0.7, 0.7], scale=0.08, size=(60, 3)),
    ])

    fig = plot_volumetric_density(
        data,
        labels=("alpha", "beta", "gamma"),
        grid_size=30,
        surface_count=10,
        bandwidth=0.15,
    )
    fig.show()


Development Roadmap
-------------------

The following features are planned for future releases:

* **1-D histogram** (``plot_1d``) — frequency distribution for single-column
  projections.
* **2-D scatter / heatmap** (``plot_2d``) — coverage view for two-column
  projections.
* **Coverage metrics** — quantitative gap-finding and coverage scores to
  complement the visual outputs.
* **Test suite** — ``pytest``-based unit and integration tests.


Authors
-------

Sohini Dutta, Kutay Arinc COKLUK, Julius Chuhwak Matthew, Sethulakshmi Vazhayil

License: MIT
