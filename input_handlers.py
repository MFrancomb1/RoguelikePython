from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import tcod

import tcod.event

import actions
from actions import (
    Action,
    BumpAction,
    WaitAction,
    PickupAction
)
import color
from entity import Item
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Item 

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

CONFIRM_KEYS = {
    tcod.event.K_RETURN,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}

class EventHandler(tcod.event.EventDispatch[Action]):

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self, event: tcod.event.Event) -> None:
        self.handle_action(self.dispatch(event))

    def handle_action(self, action: Optional[Action]) -> bool:
        """Handle actions returned from event methods."""

        if action is None:
            return False
        
        try:
            action.perform()
        except exceptions.Impossible as e:
            self.engine.message_log.add_message(e.args[0], color.impossible)
            return False
        
        self.engine.handle_enemy_turns()

        self.engine.update_fov()
        return True

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def ev_mousemotion(self, event: tcod.event.MouseMotion) -> Action | None:
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = event.tile.x, event.tile.y
    
    def on_render(self, console: tcod.Console) -> None:
        self.engine.render(console)

class AskUserEventHandler(EventHandler):
    """Handles user input for actions which require special input"""
    def handle_action(self, action: Optional[Action]) -> bool:
        if super().handle_action(action):
            self.engine.event_handler = MainGameEventHandler(self.engine)
            return True
        return False
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """by default any key exits this input handler"""
        if event.sym in {
            tcod.event.K_LSHIFT,
            tcod.event.K_RSHIFT,
            tcod.event.K_LCTRL,
            tcod.event.K_RCTRL,
            tcod.event.K_LALT,
            tcod.event.K_RALT,
        }:
            return None
        return self.on_exit()
    
    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """By default any mousr click exits this input handler"""
        return self.on_exit()
    
    def on_exit(self) -> Optional[Action]:
        """ Called when the user is trying to exit or cancel an action.
        by default this returns to the main event handler."""
        self.engine.event_handler = MainGameEventHandler(self.engine)
        return None

class InventoryEventHandler(AskUserEventHandler):
    """This handler lets the user select an item.
    What happens afterwards depends on the subclass"""

    TITLE = "<missing title>"

    def on_render(self, console: tcod.Console) -> None:
        """Render an inventory menu, which displays the items in the inventory and the key to select them.
        Will move to a different position based on where the player is located, so the player can always see where they are"""
        super().on_render(console=console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)
        height = number_of_items_in_inventory + 2

        if height<=3:
            height = 3

        if self.engine.player.x <=30:
            x=40
        else:
            x=0
        
        y=0

        width = len(self.TITLE) +4

        console.draw_frame(
            x=x,y=y,width=width,height=height,title=self.TITLE,clear=True,fg=(255,255,255),bg=(0,0,0)
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord("a")+i)
                console.print(x+1,y+i+1, f"({item_key}) {item.name}")
        else:
            console.print(x+1, y+1, "(Empty)")

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        player = self.engine.player
        key = event.sym
        index = key - tcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message("Invalid entry.", color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)
    
    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Called when the user selects a valid item"""
        raise NotImplementedError()

class InventoryActivateHandler(InventoryEventHandler):
    """Handle using an inventory item"""

    TITLE = "Select an item to use"
    
    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Return the action for the selected item."""
        return item.consumable.get_action(self.engine.player)

class InventoryDropHandler(InventoryEventHandler):
    """Handle dropping an inventory item"""
    
    TITLE = "Select an item to drop."

    def on_item_selected(self, item: Item) -> Optional[Action]:
        """Drop this item."""
        return actions.DropItem(self.engine.player, item)
    
class SelectIndexHandler(AskUserEventHandler):
    """Handles asking the user for an index on the map."""

    def __init__(self, engine: Engine) :
        """Sets the cursor to the player when this handler is constructed."""
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = player.x, player.y

    def on_render(self, console: tcod.Console) -> None:
        """Highlight the tile under cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb["bg"][x,y] = color.white
        console.tiles_rgb["fg"][x,y] = color.black

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        """Check for key movement or confirmation keys."""
        key = event.sym
        if key in MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement.
            if event.mod & (tcod.event.KMOD_LSHIFT | tcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (tcod.event.KMOD_LCTRL | tcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (tcod.event.KMOD_LALT | tcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Clamp the cursor index to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = x, y
            return None
        elif key in CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> Optional[Action]:
        """Left click confirms a selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> Optional[Action]:
        """Called when an index is selected."""
        raise NotImplementedError()


class LookHandler(SelectIndexHandler):
    """Lets the player look around using the keyboard."""

    def on_index_selected(self, x: int, y: int) -> None:
        """Return to main handler."""
        self.engine.event_handler = MainGameEventHandler(self.engine)


class MainGameEventHandler(EventHandler):
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        player = self.engine.player

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = WaitAction(player)

        elif key == tcod.event.K_ESCAPE:
            raise SystemExit()

        elif key == tcod.event.K_g:
            action = PickupAction(player)
        
        elif key == tcod.event.K_i:
            self.engine.event_handler = InventoryActivateHandler(self.engine)
        elif key == tcod.event.K_d:
            self.engine.event_handler = InventoryDropHandler(self.engine)
        elif key == tcod.event.K_SLASH:
            self.engine.event_handler = LookHandler(self.engine)

        # No valid key was pressed
        return action

class GameOverEventHandler(EventHandler):

    def ev_keydown(self, event: tcod.event.KeyDown) -> None:
        if event.sym == tcod.event.K_ESCAPE:
            raise SystemExit()