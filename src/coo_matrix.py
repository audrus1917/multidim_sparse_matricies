# -*- coding: utf-8 -*-

"""The sparse matricies class (coordinates method)."""


class DataError(Exception):
    """Data type error."""


class DimensionError(Exception):
    """Dimension size error."""


class CooMatrix:
    """Sparse matrix class."""

    def __init__(self, shape):
        self.shape = tuple(shape)
        self._nonzero = dict()

    @property
    def dimensions(self):
        """The size of matrix shape."""
        return len(self.shape)

    def check_coords(self, coords: tuple):
        """Check if cell coords are valid."""

        if len(coords) != self.dimensions:
            raise DimensionError(
                'The cell coordinates length are invalid: '
                '{0:d} != {1:d}'.format(len(coords), self.dimensions)
            )

        for _idx, _coord in enumerate(coords):
            if not isinstance(_coord, int) or _coord < 0 or \
                    _coord > self.shape[_idx]:
                raise DimensionError(
                    'The cell {0:d}-th coordinate is invalid: <{1}>'\
                        .format(_idx, _coord)
                )

    def update(self, coords, value):
        """Update cell value."""

        try:
            self.check_coords(coords)
        except DimensionError as exc:
            msg(str(exc))
        else:
            if not value and coords in self._nonzero:
                del self._nonzero[coords]
            else:
                self._nonzero[coords] = value

    def get_nonzero(self):
        """Return the nonzero cell values."""
        for coords, value in self._nonzero.items():
            yield (', '.join(coords), value)

    def get_value(self, coords):
        return self._nonzero.get(coords, 0)
