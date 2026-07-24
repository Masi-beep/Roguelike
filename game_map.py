# game map
from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np # type ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity

class GameMap:
    def __init__(self, width: int, height: int, Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        # fill the map with wall tiles
        self.tiles = np.full(
                (width, height), 
                fill_value=tile_types.wall, 
                order="F"
        )
        self.visible = np.full(
                (width, height),
                fill_value=False,
                order="F"
        )
        self.explored = np.full(
                (width, height),
                fill_value=False,
                order="F"
        )
    def in_bounds(self, x: int, y: int) -> bool:
        # return true if x and y are inside the bounds of this map
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in 'visible' array, then draw it with the light color
        If it isnt, but is in the 'explored array, draw it with dark color
        otherwise, default is 'SHROUD'
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=tile_types.SHROUD
        )
