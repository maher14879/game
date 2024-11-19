from source.sprite_types.entity import Entity
from source.item import Item
from source.get_input import Input
from source.functions import Vec

quater_rad = 3.14159 / 4

down_right = Vec((1, 0)).rot(quater_rad)
down_left =down_right.rot(2 * quater_rad)
top_left = down_left.rot(2 * quater_rad)
top_right = top_left.rot(2 * quater_rad)

def update_direction(self: "Player", dt):    
    if self.player_input.get_pressed("up"): 
        if self.player_input.get_pressed("left"): movement = top_left
        elif self.player_input.get_pressed("right"): movement = top_right
        else: movement = movement = Vec((0, -1))
    elif self.player_input.get_pressed("down"): 
        if self.player_input.get_pressed("left"): movement = down_left
        elif self.player_input.get_pressed("right"): movement = down_right
        else: movement = movement = Vec((0, 1))
    elif self.player_input.get_pressed("left"): movement = Vec((-1, 0))
    elif self.player_input.get_pressed("right"): movement = Vec((1, 0))
    else: 
        self.visual.show_figure = False
        self.speed -= 2 * self.acceleration * dt
        self.speed = min(self.speed, self.acceleration)
        self.speed = max(self.speed, 0)
        return None
    
    self.visual.show_figure = True
    self.speed += self.acceleration * dt
    self.direction = movement
    self.speed = min(self.speed, self.acceleration)
    self.speed = max(self.speed, 0)

class Player(Entity):
    def __init__(self, position, visual, name, health, player_input: Input, scene_layer = 1, acceleration: float = 300.):
        super().__init__(position, visual, name, health, scene_layer)
        self.updates.append(update_direction)
        self.player_input = player_input
        self.acceleration = acceleration
        self.direction = Vec((0,0))
        self.inventory: list[Item] = []