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
