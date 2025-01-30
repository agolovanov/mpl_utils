import pint
import typing

if typing.TYPE_CHECKING:
    import matplotlib as mpl


def format_label_units(label: str, units: pint.Unit | None, units_format: str = None) -> str:
    """Format a label with units.

    Parameters
    ----------
    label : str
        the label
    units : pint.Unit | None
        the units
    units_format : str, optional
        format to be used for units, by default None

        If None, the default format of the units registry will be used.

        An example of a format string is '{:~P}'.

    Returns
    -------
    str
        the formatted label
    """
    if units is None:
        return label
    else:
        if units_format is None:
            units_format = units._REGISTRY.mpl_formatter
        units_label = units_format.format(units)

        return f'{label}, {units_label}'


def set_xlabel(ax: 'mpl.axes.Axes', label: str):
    """Set the x-axis label with automatically determined units.

    Parameters
    ----------
    ax : mpl.axes.Axes
        the axes
    label : str
        the base label (without units)
    """
    ax.set_xlabel(format_label_units(label, ax.xaxis.units))


def set_ylabel(ax: 'mpl.axes.Axes', label: str):
    """Set the y-axis label with automatically determined units.

    Parameters
    ----------
    ax : mpl.axes.Axes
        the axes
    label : str
        the base label (without units)
    """

    ax.set_ylabel(format_label_units(label, ax.yaxis.units))
