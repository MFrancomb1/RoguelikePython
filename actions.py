from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, engine, entity) -> None:
        # perform action with objects needed to determine its scope
        # 'engine' is the scope the action is being performed in
        # 'entity' is the object perfroming the action
        #this method must be overwritten by Action subclasses
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine, entity):
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine, entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return # destination is out of bounds, do not move
        elif not engine.game_map.tiles["walkable"][dest_x,dest_y]:
            return # destination is not walkable, do not move
        else:
            entity.move(self.dx, self.dy)