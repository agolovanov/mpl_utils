from matplotlib import ticker


class ScientificScalarFormatter(ticker.ScalarFormatter):
    def __init__(self, useOffset=False, useMathText=True):
        """A formatter which formats each individual labels in the scientific notation.

        Parameters
        ----------
        useOffset : bool, optional
            Whether to use offset notation. See `.set_useOffset`, by default False
        useMathText : bool, optional
            Whether to use fancy math formatting. See `.set_useMathText`, by default True
        """
        super().__init__(useOffset=useOffset, useMathText=useMathText)

    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = 0

    def __call__(self, x, pos=None):
        if len(self.locs) == 0:
            return ''
        else:
            xp = x - self.offset

            if abs(xp) < 1e-8:
                xp = 0
                return self._format_maybe_minus_and_locale(self.format, xp)
            else:
                return f'${self.format_data(xp)}$'
