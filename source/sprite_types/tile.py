from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sounds import sounds

def play_collision_sound(self: "Tile", collider: Entity):
    if self.play_sound == 0 and collider.speed > self.min_speed_sound:
        sounds.play(self.collision_sound)
        self.play_sound = sounds.len(self.collision_sound) + 0.1
        
def play_sound_update(self: "Tile", dt):
    if self.play_sound > 0: self.play_sound -= dt
    else: self.play_sound = 0

class Tile(Sprite):
    def __init__(self, position, visual, scene_layer = 1, box=None, collision_sound: str = None):
        super().__init__(position, visual, scene_layer, box)
        self.collision_sound = collision_sound
        self.play_sound = 0
        self.min_speed_sound = 100
        self.collision_updates = [play_collision_sound]
        self.updates.append(play_sound_update)
    
    def collision_update(self, collider: Entity):
        for collision_update in self.collision_updates:
            collision_update(self, collider)
        
        collider.speed = 0