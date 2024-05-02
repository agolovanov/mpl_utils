import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap

colormaps = {}
colormaps['white_red'] = LinearSegmentedColormap.from_list("laser", ['#ffffff', '#b00707'])
colormaps['white_green'] = LinearSegmentedColormap.from_list("bunch", ['#ffffff', '#1f8742'])

for name in colormaps:
    mpl.colormaps.register(colormaps[name], name=name)


def mix_images(image_array):
    """
    Calculates a new image by mixing several images.

    Parameters
    ----------
    image_array
        Array of matplotlib.image.AxesImage

    Returns
    -------
    An array of the RGBA values of the resulting image.
    """
    def get_rgb_data(image):
        return image.cmap(image.norm(image.get_array()))

    rgb_array = map(get_rgb_data, image_array)

    # mixing of colors is based on x = (x1 + x2) / (1 + x1 x2) formula for 1 - R, 1 - G, 1 - B.
    from functools import reduce
    return reduce(lambda x, y: x * y / (2 - x - y + x * y), rgb_array)


def axes_mix_images(ax, **kwargs):
    """Take images from the axis and mix their colors.

    Usage:
    - Plot several pictures of the same shape with `ax.imshow` without using opacity in the colormaps.
    - Call axis_mix_images(ax).

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        the axes to apply the transformation to.
    **kwargs :
        any parameters for the imshow call, like extent, origin, etc.
    """

    import matplotlib as mpl
    import numpy as np
    from warnings import warn

    imgs = [x for x in ax.get_children() if isinstance(x, mpl.image.AxesImage)]
    rgb_values = mix_images(imgs)

    auto_kwargs = {}
    for img in imgs:
        extent = img.get_extent()
        if 'extent' not in auto_kwargs:
            auto_kwargs['extent'] = extent
        elif not np.all(np.equal(auto_kwargs['extent'], extent)):
            warn(f'Extents [{extent}] and [{auto_kwargs["extent"]}] are not the same')

        origin = img.origin
        if 'origin' not in auto_kwargs:
            auto_kwargs['origin'] = origin
        elif origin != auto_kwargs['origin']:
            warn(f'Origins [{origin}] and [{auto_kwargs["origin"]}] are not the same')

        img.remove()
    auto_kwargs['aspect'] = ax.get_aspect()

    auto_kwargs.update(kwargs)

    ax.imshow(rgb_values, **auto_kwargs)


def calculate_extent(xdata, ydata, add_pixel_pad=False):
    """Calculates extent for the data on x-y grid for the imshow method.

    Parameters
    ----------
    xdata : np.array or similar
        data to be used to determine the x-axis extent
    ydata : np.array or similar
        data to be used to determine the y-axis extent
    add_pixel_pad : bool, optional
        adds a padding to the ranges, so that the centers of the imshow pixels will be exactly in the middle
        of the data point, default False
        Assumes that the data arrays are equally spaced arrays.
        Mostly relevant for arrays with a small number of points.
    Returns
    -------
    tuple
        4 numbers representing the extent as expected by the plt.imshow method.
    """
    import numpy as np
    if add_pixel_pad:
        dx = 0.5 * (xdata[1] - xdata[0])
        dy = 0.5 * (ydata[1] - ydata[0])
        return np.min(xdata) - dx, np.max(xdata) + dx, np.min(ydata) - dy, np.max(ydata) + dy
    else:
        return np.min(xdata), np.max(xdata), np.min(ydata), np.max(ydata)


DEFAULT_DASHES = [[], [3, 1], [1, 1], [3, 1, 1, 1], [3, 1, 1, 1, 1, 1], [5, 1]]


def setup_dash_cycle(dash_styles=DEFAULT_DASHES):
    """Updates the current matplotlib cycler to include line dashes

    Parameters
    ----------
    dash_styles : list, optional
        the list of dash lists, by default DEFAULT_DASHES
    """
    from cycler import cycler
    import itertools
    import matplotlib.pyplot as plt

    default_cycler = plt.rcParams['axes.prop_cycle']
    cycler_dict = default_cycler.by_key()

    cycler_dict['dashes'] = list(itertools.islice(itertools.cycle(dash_styles), len(default_cycler)))

    new_cycler = cycler(**cycler_dict)

    plt.rc('axes', prop_cycle=new_cycler)


def remove_grid(ax=None, tick_params: dict = {'direction': 'in', 'length': 2}):
    """Removes the grid from the axes and changes tick style.

    Useful for imshow and similar plots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes, optional
        the affected axes. By default, the current axis will be used
    tick_params : dict, optional
        ax.tick_params arguments, by default {'direction': 'in', 'length': 2}
    """
    if ax is None:
        import matplotlib.pyplot as plt
        ax = plt.gca()
    ax.grid(False)
    ax.set_axisbelow(False)
    ax.tick_params(**tick_params)


def add_label(ax, text: str, xpos: float = 0.02, ypos: float = 0.95, *, fontsize: str = 'small', ha: str = 'left',
              va: str = 'center', **kwargs):
    """Puts a text label on the graph

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        axes to apply the label to
    text : str
        text of the label
    xpos : float, optional
        x position, by default 0.02
    ypos : float, optional
        y position, by default 0.95
    fontsize : str, optional
        font size, by default 'small'
    ha : str, optional
        horizontal alignment, by default 'left'
    va : str, optional
        vertical alignment, by default 'center'
    kwargs : dict
        will be passed to the ax.text() call
    """
    ax.text(xpos, ypos, text, horizontalalignment=ha, verticalalignment=va, transform=ax.transAxes, fontsize=fontsize, **kwargs)
    