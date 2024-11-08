from source.sprite_types.entity import Entity
from source.item import Item
from source.get_input import Input
from source.functions import Vec

class Player(Entity):
    def __init__(self, position, visual, name, health, player_input: Input, status_effect = None, scene_layer=1, box=None, speed: float = 200.):
        super().__init__(position, visual, name, health, status_effect, scene_layer, box)
        self.updates.append(self.update_direction)
        self.player_input = player_input
        self.speed = speed
        self.direction = Vec((0,0))
        self.inventory: list[Item] = []
    
    def update_direction(self, dt):
        self.direction = Vec((0,0))
        
        if self.player_input.get_pressed("up"): 
            self.direction.update((None, -1))
            
        elif self.player_input.get_pressed("down"): 
            self.direction.update((None, 1))
            
        if self.player_input.get_pressed("left"): 
            self.direction.update((-1, None))
            
        elif self.player_input.get_pressed("right"): 
            self.direction.update((1, None))
