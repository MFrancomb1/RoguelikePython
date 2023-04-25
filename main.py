import copy
import tcod
from engine import Engine
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

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min=room_min_size,
        room_max=room_max_size,
        map_width=mapWidth,
        map_height=mapHeight,
        max_monsters=max_monsters_per_room,
        engine=engine,
    )
    engine.update_fov()

    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new_terminal(sWidth,sHeight,tileset=tileset,title="Python Roguelike Tutorial", vsync=True) as context:
        root_console = tcod.Console(sWidth, sHeight, order="F")
        while True:
            #drawing the screen
            engine.render(root_console, context)
            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()