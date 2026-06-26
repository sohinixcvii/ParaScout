import numpy as np

from .plotting_functions import plot_bubble_map

# plot_1d and plot_2d are expected to be defined in plotting_functions
# and imported here once available.


def plot_dispatcher(data_list, labels=None):
    """
    Route each array returned by decider() to the appropriate plotting
    function based on its dimensionality.

    Parameters
    ----------
    data_list : list of ndarray
        Output of decider(). Each element is one dataset to plot.
        Routing logic (applied when len(data_list) > 1):
            - 1-D array  or  (N, 1)  → plot_1d
            - (N, 2)                  → plot_2d
            - (N, 3+)                 → plot_bubble_map

    Returns
    -------
    figs : list of plotly.graph_objects.Figure
        One figure per array in data_list, in the same order.
    """
    if len(data_list) <= 1:
        raise ValueError(
            "data_list must contain more than one array. "
            "decider() returned fewer entries than expected."
        )
    elif len(data_list) >5:
        raise ValueError(
            "data_list contains too many parameters. "
        )

    figs = []

    for arr in data_list:
        arr = np.asarray(arr)

        if arr.ndim == 1 or (arr.ndim == 2 and arr.shape[1] == 1):
            fig = plot_1d(arr, labels)

        elif arr.ndim == 2 and arr.shape[1] == 2:
            fig = plot_2d(arr, labels)

        elif arr.ndim == 2 and arr.shape[1] >= 3:
            fig = plot_bubble_map(arr, labels)

        else:
            raise ValueError(
                f"Cannot route array with shape {arr.shape}: "
                "expected a 1-D array or a 2-D array with 1–3+ columns."
            )

        figs.append(fig)

    return figs
