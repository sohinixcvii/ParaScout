import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde


def plot_1d(
    params,
    labels=("x",),
    use_kde=True,
    padding_fraction=0.05,
):
    """
    Create a 1D distribution plot from a 1-D or (N, 1) parameter array.

    Parameters
    ----------
    params : ndarray, shape (N,) or (N, 1)
        Single parameter column.

    labels : tuple of str, optional
        Axis label for the parameter. Only the first element is used.

    use_kde : bool
        If True, overlay a Gaussian KDE curve on top of the histogram.

    padding_fraction : float
        Fractional padding added to the x-axis limits when using KDE.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    params = np.asarray(params, dtype=float).ravel()
    params = params[np.isfinite(params)]

    if labels is None:
        xlabel = "Parameter"
    elif isinstance(labels, (list, tuple)) and len(labels) >= 1:
        xlabel = str(labels[0])
    else:
        xlabel = str(labels)

    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=params,
            name="Count",
            opacity=0.6,
        )
    )

    if use_kde:
        x_min, x_max = params.min(), params.max()
        width = x_max - x_min if x_max != x_min else 1.0
        pad = padding_fraction * width
        x_grid = np.linspace(x_min - pad, x_max + pad, 300)
        kde = gaussian_kde(params)
        # Scale KDE to match histogram area
        bin_width = width / max(int(np.sqrt(len(params))), 1)
        y_kde = kde(x_grid) * len(params) * bin_width
        fig.add_trace(
            go.Scatter(
                x=x_grid,
                y=y_kde,
                mode="lines",
                name="KDE",
                line=dict(width=2),
            )
        )

    fig.update_layout(
        title=f"1D Distribution of {xlabel}",
        margin=dict(l=60, r=20, b=60, t=60),
        xaxis_title=xlabel,
        yaxis_title="Count",
        barmode="overlay",
    )

    return fig


def plot_2d(
    params,
    labels=("x", "y"),
    opacity=0.7,
    colorscale="Viridis",
    padding_fraction=0.05,
):
    """
    Create a 2D scatter plot from an (N, 2) parameter array.

    Parameters
    ----------
    params : ndarray, shape (N, 2)
        Two parameter columns. Column 0 → x axis, column 1 → y axis.

    labels : tuple of str
        Axis labels for x and y.

    opacity : float
        Opacity of scatter markers.

    colorscale : str
        Plotly colorscale used to colour points by y value.

    padding_fraction : float
        Fractional padding added to axis limits.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    params = np.asarray(params, dtype=float)

    if params.ndim == 1:
        raise ValueError("params must be a 2D array with shape (N, 2)")

    if params.shape[1] < 2:
        raise ValueError("params must have at least 2 columns")

    params = params[np.all(np.isfinite(params[:, :2]), axis=1)]

    x = params[:, 0]
    y = params[:, 1]

    if labels is None:
        xlabel, ylabel = "x", "y"
    elif isinstance(labels, (list, tuple)) and len(labels) >= 2:
        xlabel, ylabel = str(labels[0]), str(labels[1])
    else:
        xlabel, ylabel = "x", "y"

    def compute_limits(arr):
        arr_min, arr_max = arr.min(), arr.max()
        width = arr_max - arr_min if arr_max != arr_min else 1.0
        pad = padding_fraction * width
        return arr_min - pad, arr_max + pad

    xlim = compute_limits(x)
    ylim = compute_limits(y)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                color=y,
                colorscale=colorscale,
                opacity=opacity,
                colorbar=dict(title=ylabel),
                line=dict(width=0.5, color="white"),
            ),
            name="Points",
        )
    )

    fig.update_layout(
        title="2D Scatter Plot",
        margin=dict(l=60, r=20, b=60, t=60),
        xaxis=dict(title=xlabel, range=list(xlim)),
        yaxis=dict(title=ylabel, range=list(ylim)),
    )

    return fig


def plot_volumetric_density(
    params,
    labels=("x", "y", "z"),
    grid_size=40,
    opacity=0.12,
    surface_count=15,
    bandwidth=None,
    padding_fraction=0.05,
):
    """
    Create a 3D volumetric density plot from an (N,3) parameter array.

    Parameters
    ----------
    params : ndarray, shape (N,3)
        Three parameter columns.

    labels : tuple(str, str, str)
        Axis labels.

    grid_size : int
        Number of grid cells per dimension.

    opacity : float
        Opacity of density volume.

    surface_count : int
        Number of density contours.

    bandwidth : float or None
        KDE bandwidth passed to scipy.stats.gaussian_kde.

    padding_fraction : float
        Fractional padding added to axis limits.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """

    params = np.asarray(params)

    if params.ndim != 2:
        raise ValueError("params must be a 2D array")

    if params.shape[1] != 3:
        raise ValueError("params must have shape (N,3)")

    params = params[np.all(np.isfinite(params), axis=1)]

    x = params[:, 0]
    y = params[:, 1]
    z = params[:, 2]

    def compute_limits(arr):
        arr_min = arr.min()
        arr_max = arr.max()

        width = arr_max - arr_min

        # Prevent zero-width axes
        if width == 0:
            width = 1.0

        pad = padding_fraction * width

        return arr_min - pad, arr_max + pad

    xlim = compute_limits(x)
    ylim = compute_limits(y)
    zlim = compute_limits(z)

    x_grid = np.linspace(*xlim, grid_size)
    y_grid = np.linspace(*ylim, grid_size)
    z_grid = np.linspace(*zlim, grid_size)

    X, Y, Z = np.meshgrid(
        x_grid,
        y_grid,
        z_grid,
        indexing="ij"
    )

    grid_points = np.vstack([
        X.ravel(),
        Y.ravel(),
        Z.ravel()
    ])

    kde = gaussian_kde(
        params.T,
        bw_method=bandwidth
    )

    density = kde(grid_points)

    fig = go.Figure()

    fig.add_trace(
        go.Volume(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            value=density,
            opacity=opacity,
            surface_count=surface_count,
            caps=dict(
                x_show=False,
                y_show=False,
                z_show=False
            ),
            colorbar=dict(
                title="Density"
            ),
            name="Density field"
        )
    )

    fig.add_trace(
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode="markers",
            marker=dict(
                size=4,
                color="black"
            ),
            name="Simulation points"
        )
    )

    fig.update_layout(
        title="3D Parameter-Space Density",
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=40
        ),
        scene=dict(
            xaxis=dict(
                title=labels[0],
                range=list(xlim)
            ),
            yaxis=dict(
                title=labels[1],
                range=list(ylim)
            ),
            zaxis=dict(
                title=labels[2],
                range=list(zlim)
            ),
        )
    )

    return fig


def plot_bubble_map(
    params,
    labels=("x", "y", "size"),
    max_marker_size=40,
    opacity=0.7,
    colorscale="Viridis",
    padding_fraction=0.05,
):
    """
    Create a 2D bubble map from an (N, 3) parameter array.

    Bubble positions are determined by the first two columns; bubble size is
    proportional to the third column.

    Parameters
    ----------
    params : ndarray, shape (N, 3)
        Three parameter columns. Column 0 → x position, column 1 → y
        position, column 2 → bubble size.

    labels : tuple(str, str, str)
        Axis and colorbar labels for x, y, and the size parameter.

    max_marker_size : int or float
        Maximum marker diameter in pixels. Sizes are scaled linearly so that
        the largest value maps to this size.

    opacity : float
        Opacity of the bubble markers.

    colorscale : str
        Plotly colorscale used to colour bubbles by their size value.

    padding_fraction : float
        Fractional padding added to axis limits.

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """

    params = np.asarray(params)

    if params.ndim != 2:
        raise ValueError("params must be a 2D array")

    if params.shape[1] < 3:
        raise ValueError("params must have at least 3 columns")

    params = params[np.all(np.isfinite(params[:, :3]), axis=1)]

    x = params[:, 0]
    y = params[:, 1]
    s = params[:, 2]

    def compute_limits(arr):
        arr_min = arr.min()
        arr_max = arr.max()
        width = arr_max - arr_min
        if width == 0:
            width = 1.0
        pad = padding_fraction * width
        return arr_min - pad, arr_max + pad

    xlim = compute_limits(x)
    ylim = compute_limits(y)

    s_min = s.min()
    s_max = s.max()
    s_range = s_max - s_min if s_max != s_min else 1.0
    marker_sizes = (s - s_min) / s_range * max_marker_size

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="markers",
            marker=dict(
                size=marker_sizes,
                color=s,
                colorscale=colorscale,
                opacity=opacity,
                colorbar=dict(
                    title=labels[2]
                ),
                line=dict(
                    width=0.5,
                    color="white"
                ),
            ),
            name="Bubbles"
        )
    )

    fig.update_layout(
        title="2D Bubble Map",
        margin=dict(l=60, r=20, b=60, t=60),
        xaxis=dict(
            title=labels[0],
            range=list(xlim)
        ),
        yaxis=dict(
            title=labels[1],
            range=list(ylim)
        ),
    )

    return fig
