from source.sprite import Sprite
from source.visual import Visual

class Entity(Sprite):
    def __init__(self, visual: Visual, scene_layer: int, health: int):
        super().__init__(visual, scene_layer)
        self.direction: tuple[float, float] = ()
        self.speed = 1
        self.health = health
        self.death_updates = []
        
    def new_position(self, dt) -> tuple[float, float]:
        return (self.position[i] + self.direction[i] * dt * self.speed for i in range(2))
    
    def update_position(self, position: tuple[float, float]):
        self.position = (position[i] if position[i] else self.position[i] for i in range(2))
        
    def take_damage(self, damage: int, source: Sprite, damage_type: str = None):
        self.health -= damage
        if self.health <= 0: 
            self.death_update(source, damage_type)
            self.kill = True
    
    def death_update(self, source: Sprite, damage_type: str):
        for death_update in self.death_updates:
            death_update(source, damage_type)

class Status_effect():
    pass