import copy
import tcod
from engine import Engine
from input_handlers import EventHandler
from game_map import GameMap
from procgen import generate_dungeon
import entity_factories

def main() -> None:
    sWidth = 80
    sHeight = 50

    mapWidth = 80
    mapHeight = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    event_handler = EventHandler()
    player = copy.deepcopy(entity_factories.player)

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min=room_min_size,
        room_max=room_max_size,
        map_width=mapWidth,
        map_height=mapHeight,
        max_monsters=max_monsters_per_room,
        player=player
    )
    engine = Engine(event_handler=event_handler, game_map=game_map, player=player)

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new_terminal(sWidth,sHeight,tileset=tileset,title="Python Roguelike Tutorial", vsync=True) as context:
        root_console = tcod.Console(sWidth, sHeight, order="F")
        while True:
            #drawing the screen
            engine.render(root_console, context)
            #getting the events
            events = tcod.event.wait()
            #handle the events
            engine.handle_event(events)

if __name__ == "__main__":
    main()