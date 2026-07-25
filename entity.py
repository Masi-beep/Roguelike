# entity class eoeoeo
import copy

from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    # generic object to represent players, enemies, items, etc.

    gamemap: GameMap

    def __init__(
        self,
        gamemap: Optional[GameMap] = None,
        x:int = 0, 
        y:int = 0, 
        char:str = "?", 
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name 
        self.blocks_movement = blocks_movement
        if gamemap:
            # if its not provided now then it will be set later
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        # spawn a copy of this instance at the given location
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone
    
    def place(
        self,
        x: int,
        y: int,
        gamemap: Optional[GameMap] = None
    ) -> None:
        # place this entity at a new location. handles moving across GameMap
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"): # possibly unintialized
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx:int, dy:int) -> None:
        # Move entity by given amount
        self.x += dx
        self.y += dy
