import tcod
from actions import MovementAction, EscapeAction
from input_handlers import EventHandler

def main() -> None:
    sWidth = 80
    sHeight = 50

    player_x = int(sWidth/2)
    player_y = int(sHeight/2)
    event_handler = EventHandler()

    tileset = tcod.tileset.load_tilesheet("charset.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new_terminal(
        sWidth,sHeight,tileset=tileset,title="Python Roguelike Tutorial", vsync=True
    ) as context:
        root_console = tcod.Console(sWidth, sHeight, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)

            root_console.clear()

            for event in tcod.event.wait():
                action = event_handler.dispatch(event)

                if action is None:
                    continue

                if isinstance(action, MovementAction):
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):
                    raise SystemExit()


if __name__ == "__main__":
    main()