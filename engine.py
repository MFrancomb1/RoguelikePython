from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from input_handlers import EventHandler
from entity import Entity
from game_map import GameMap

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler,game_map: GameMap, player: Entity) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

    def handle_event(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(engine=self, player=self.player)
    
    def render(self, console: Console, context: Context):
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, entity.color)
        
        context.present(console)

        console.clear()
