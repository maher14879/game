from source.sprite import Sprite
from source.sprite_types.entity import Entity

class Tile(Sprite):
    def __init__(self, position, visual, scene_layer = 1, box=None):
        super().__init__(position, visual, scene_layer, box)
        self.collision_updates = []
    
    def collision_update(self, collider: Entity):
        for collision_update in self.collision_updates:
            collision_update(collider)