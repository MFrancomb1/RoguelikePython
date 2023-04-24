from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler
from entity import Entity
from game_map import GameMap

class Engine:
    def __init__(self, event_handler: EventHandler,game_map: GameMap, player: Entity) -> None:
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_event(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(engine=self, entity=self.player)

            self.update_fov()

    def update_fov(self) -> None:
        #compute the visible area from players field of view
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        #add visible tiles to explored array
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context):
        self.game_map.render(console)

        context.present(console)

        console.clear()
