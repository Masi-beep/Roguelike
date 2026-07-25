from __future__ import annotations

from typing import List, Tuple

import numpy as np # type: ignore
import tcod

from actions import Action
from components.base_components import BaseComponent


class BaseAI(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x:int, dest_y:int) -> List[Tuple[int,int]]:
        """compute and return a path to the target position

        if there is no valid path then returns an empty list
        """
        # copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"],dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # check that an entitiy blocks movement and the cost isn't zero
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # add to the cost of a blocked position
                # a lower number means more enemies will crowd behind 
                # eachother in hallways. A higher number means enemies will
                # take longer paths in order to surround the player.
                cost[entity.x, entity.y] += 10

        # create graph from cost array & pass that graph to a new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        
        # start position
        pathfinder.add_root((self.entity.x, self.entity.y))

        # compute path to destination & remove starting point
        path:List[List[int]]=pathfinder.path_to((dest_x, dest_y))[1:].tolist()
        return [(index[0], index[1]) for index in path]
