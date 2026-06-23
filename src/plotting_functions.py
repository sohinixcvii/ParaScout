import numpy as np
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

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