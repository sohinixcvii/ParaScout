"""
ParaScout
=========
A lightweight tool for evaluating and visualising how well a parameter space
has been explored during simulation campaigns.

Public API
----------
visualise(data_list, labels=None)
    Top-level entry point. Routes a list of parameter arrays to the
    appropriate plotting functions and returns Plotly figures.

plot_dispatcher(data_list, labels=None)
    Low-level dispatcher that routes arrays by dimensionality.

plot_1d(params, labels=..., ...)
    1-D histogram / KDE distribution plot for 1-D parameter arrays.

plot_2d(params, labels=..., ...)
    2-D scatter plot for (N, 2) parameter arrays.

plot_bubble_map(params, labels=..., ...)
    2-D bubble map for (N, 3) parameter arrays.

plot_volumetric_density(params, labels=..., ...)
    3-D volumetric density plot for (N, 3) parameter arrays.
"""

from .plotting_functions import (
    plot_1d,
    plot_2d,
    plot_bubble_map,
    plot_volumetric_density,
)
from .dispatcher import plot_dispatcher


def visualise(data_list, labels=None):
    """
    Visualise a collection of parameter arrays.

    This is the top-level wrapper for ParaScout. It accepts a list of NumPy
    arrays (one per parameter-space projection) and dispatches each one to the
    appropriate plotting function based on its shape, returning a list of
    interactive Plotly figures.

    Routing rules
    -------------
    - 1-D array or (N, 1)  → plot_1d
    - (N, 2)               → plot_2d
    - (N, 3+)              → plot_bubble_map

    Parameters
    ----------
    data_list : list of numpy.ndarray
        Each element is one dataset to visualise. The list must contain
        between 2 and 5 arrays (inclusive).

    labels : list of str, optional
        Axis labels forwarded to the individual plotting functions.

    Returns
    -------
    figs : list of plotly.graph_objects.Figure
        One figure per array in *data_list*, in the same order.

    Examples
    --------
    >>> import numpy as np
    >>> from parascout import visualise
    >>> rng = np.random.default_rng(0)
    >>> data = rng.random((100, 3))
    >>> figs = visualise([data, data])
    >>> figs[0].show()
    """
    return plot_dispatcher(data_list, labels=labels)


__all__ = [
    "visualise",
    "plot_dispatcher",
    "plot_1d",
    "plot_2d",
    "plot_bubble_map",
    "plot_volumetric_density",
]
