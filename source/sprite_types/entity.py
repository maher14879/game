from source.sprite import Sprite
from source.visual import Visual

class Entity(Sprite):
    def __init__(self, visual: Visual, scene_layer: int):
        super().__init__(visual, scene_layer)
        self.direction = ()
        self.speed = 1
        
    def new_position(self, dt):
        new_position = ()
        for i in range(min(len(self.position), len(self.direction))):
            new_position[i] = self.position[i] + self.direction[i] * dt * self.speed
        return new_position
    
    def update_position(self, position: tuple[float]):
        for i in range(min(len(self.position), len(position))):
            self.position[i] = position[i] if position[i] else self.position[i]

class Status_effect():
    pass