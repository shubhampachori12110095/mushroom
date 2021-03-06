import numpy as np


class Tiles:
    """
    Class implementing rectangular tiling. For each point in the state space,
    this class can be used to compute the index of the corresponding tile.

    """
    def __init__(self, x_range, n_tiles, state_components=None):
        """
        Constructor.

        Args:
            x_range (list): list of two-elements lists specifying the range of
                each state variable;
            n_tiles (list): list of the number of tiles to be used for each
                dimension.
            state_components (list, None): list of the dimensions of the input
                to be considered by the tiling. The number of elements must
                match the number of elements in ``x_range`` and ``n_tiles``.

        """
        if isinstance(x_range[0], list):
            self._range = x_range
        else:
            self._range = [x_range]

        if isinstance(n_tiles, list):
            assert(len(n_tiles) == len(self._range))

            self._n_tiles = n_tiles
        else:
            self._n_tiles = [n_tiles] * len(self._range)

        self._state_components = state_components

        if self._state_components is not None:
            assert(len(self._state_components) == len(self._range))

        self._size = 1

        for s in self._n_tiles:
            self._size *= s

    def __call__(self, x):
        if self._state_components is not None:
            x = x[self._state_components]

        multiplier = 1
        tile_index = 0

        for i, (r, N) in enumerate(zip(self._range, self._n_tiles)):
            if r[0] <= x[i] < r[1]:
                width = r[1] - r[0]
                component_index = int(np.floor(N * (x[i] - r[0]) / width))
                tile_index += component_index * multiplier
                multiplier *= N
            else:
                tile_index = None
                break

        return tile_index

    @staticmethod
    def generate(n_tilings, n_tiles, low, high):
        """
        Factory method to build ``n_tilings`` tilings of ``n_tiles`` tiles with
        a range between ``low`` and ``high`` for each dimension.

        Args:
            n_tilings (int): number of tilings;
            n_tiles (list): number of tiles for each tilings for each dimension;
            low (np.ndarray): lowest value for each dimension;
            high (np.ndarray): highest value for each dimension.

        Returns:
            The list of the generated tiles.

        """
        assert len(n_tiles) == len(low) == len(high)

        low = np.array(low, dtype=np.float)
        high = np.array(high, dtype=np.float)

        tilings = list()
        offset = (high - low) / (np.array(n_tiles) * n_tilings - n_tilings + 1.)
        for i in range(n_tilings):
            x_min = low - (n_tilings - 1 - i) * offset
            x_max = high + i * offset
            x_range = [[x, y] for x, y in zip(x_min, x_max)]
            tilings.append(Tiles(x_range, n_tiles))

        return tilings

    @property
    def size(self):
        return self._size
