from source.sprite import Sprite
from source.functions import Vec

class Status_effect():
    def __init__(self):
        self.updates = []
        self.tick_updates = []
        self.take_damage_updates = []
        self.death_updates = []

class Entity(Sprite):
    def __init__(self, position, visual, name: str, health: int, scene_layer = 1):
        super().__init__(position, visual, scene_layer)
        self.direction: Vec = Vec((0, 0))
        self.speed = 0
        self.name = name
        self.health = health
        self.take_damage_updates = []
        self.death_updates = []
        
    def get_new_position(self, dt) -> Vec:
        return self.position.add(self.direction.mul(self.speed).mul(dt))
        
    def take_damage(self, damage: int, source: Sprite, damage_type: str = None):
        self.health -= damage
        if self.health <= 0: 
            self.death_update(source, damage_type)
        
        for take_damage_update in self.take_damage_updates:
            take_damage_update(source, damage_type)
    
    def death_update(self, source: Sprite, damage_type: str):
        self.kill = True
        for death_update in self.death_updates:
            death_update(self, source, damage_type)
    
    def add_status_effect(self, status_effect: Status_effect):
        self.updates.append(status_effect.updates)
        self.tick_updates.append(status_effect.tick_updates)
        self.take_damage_updates.append(status_effect.take_damage_updates)
        self.death_updates.append(status_effect.death_updates)

    def remove_status_effect(self, status_effect: Status_effect):
        self.updates.remove(status_effect.updates)
        self.tick_updates.remove(status_effect.tick_updates)
        self.take_damage_updates.remove(status_effect.take_damage_updates)
        self.death_updates.remove(status_effect.death_updates)