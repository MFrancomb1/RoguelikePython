from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import MovementAction, EscapeAction
from input_handlers import EventHandler
from entity import Entity

class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity) -> None:
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_event(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(action.dx, action.dy)

                
            elif isinstance(action, EscapeAction):
                raise SystemExit()
    
    def render(self, console: Console, context: Context):
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, entity.color)
        
        context.present(console)

        console.clear()
