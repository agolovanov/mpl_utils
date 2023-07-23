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


def calculate_extent(xdata, ydata):
    """Calculates extent for the data on x-y grid for the imshow method.

    Parameters
    ----------
    xdata : np.array or similar
        data to be used to determine the x-axis extent
    ydata : np.array or similar
        data to be used to determine the y-axis extent

    Returns
    -------
    tuple
        4 numbers representing the extent as expected by the plt.imshow method.
    """
    import numpy as np
    return np.min(xdata), np.max(xdata), np.min(ydata), np.max(ydata)
