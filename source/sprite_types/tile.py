from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sounds import sounds
from source.functions import Vec

tile_size = Vec((16, 8))
tile_size_half = tile_size.mul(0.5)

def play_collision_sound(self: "Tile", collider: Entity):
    if self.play_sound == 0 and collider.speed > self.min_speed_sound:
        sounds.play(self.collision_sound)
        self.play_sound = sounds.len(self.collision_sound) + 0.1
        
def play_sound_update(self: "Tile", dt):
    if self.play_sound > 0: self.play_sound -= dt
    else: self.play_sound = 0

class Tile(Sprite):
    def __init__(self, tile_position: Vec, visual, layer = 1, box=None, collision_sound: str = None):
        self.tile_position = Vec(tile_position)
        position = Vec((self.tile_position.x - self.tile_position.y, self.tile_position.x + self.tile_position.y - 2 * layer)).mul(tile_size_half)
        super().__init__(position, visual, layer, box)
        self.collision_sound = collision_sound
        self.play_sound = 0
        self.min_speed_sound = 100
        self.collision = True
        self.collision_updates = [play_collision_sound]
        self.updates.append(play_sound_update)
    
    def anchor(self, anchor_position: Vec):
        anchor_position = Vec(anchor_position)
        self.tile_position.y = ((anchor_position.y / tile_size_half.y) - (anchor_position.x / tile_size_half.x)) * 0.5
        self.tile_position.x = self.tile_position.y + (anchor_position.x / tile_size_half.x)
        self.position = Vec((self.tile_position.x - self.tile_position.y, self.tile_position.x + self.tile_position.y)).mul(tile_size_half)
    
    def collision_update(self, collider: Entity):
        for collision_update in self.collision_updates:
            collision_update(self, collider)
        collider.speed = 0