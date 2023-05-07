from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory

player = Actor(char="@", color=(255, 255, 255), name="Player", ai_cls=HostileEnemy, fighter=Fighter(hp=25, defense=1, power=4), inventory=Inventory(capacity=26))

orc = Actor(char="o", color=(63, 127, 63), name="Orc", ai_cls=HostileEnemy, fighter=Fighter(hp=10, defense=0, power=3), inventory=Inventory(capacity=0))

troll = Actor(char="T", color=(0, 127, 0), name="Troll", ai_cls=HostileEnemy, fighter=Fighter(hp=16, defense=1, power=4), inventory=Inventory(capacity=0))

health_potion = Item(
    char="!",
    color=(127, 0, 255), name="Health Potion", consumable=consumable.HealingConsumable(amount=4),
)

lightning_scroll = Item(
    char="~",
    color=(255,255,0), name = "Lightning Scroll", consumable=consumable.LightningDamaageConsumable(damage=20, range=5),

)
