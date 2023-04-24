import tcod
from engine import Engine
from input_handlers import EventHandler
from entity import Entity
from game_map import GameMap
from procgen import generate_dungeon

def main() -> None:
    sWidth = 80
    sHeight = 50

    mapWidth = 80
    mapheight = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    event_handler = EventHandler()
    player = Entity(int(sWidth)//2 + 5, int(sHeight)//2, "@", (255,255,255))

    game_map = generate_dungeon(max_rooms, room_min_size, room_max_size, mapWidth, mapheight, player)
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