from source.sprite import Sprite
from source.sprite_types.tile import Tile
from source.sprite_types.particle import Particle
from source.visual import Image

from copy import copy

from source.visual import Animation, Visual, Image 
from source.sprite_types.sub.player import Player
from assets.data.misc import start_settings
from source.get_input import Input
from source.functions import read_folder
import math

def destroy_update(self: Tile, dt):
    if self.play_sound > 0:
        self.spawn_list = [sprite for sprite in self.spawn_list if not sprite.kill_on_update]
        self.kill_on_update = True
        particle = copy(test_particle)
        particle.position = self.position
        self.spawn_list.append(particle)

particle_visual = Image("assets\\images\\status_effects\\wet.png", (16, 16))
test_particle = Particle(
    position = (0,0),
    visual = particle_visual,
    scene_layer = 0,
    box = None,
    direction = (-10, -10),
    speed = 10,
    max_age = 10,
    rotation = 1,
    spawn = None,
    spawn_speed = 1,
)

tile_visual = Image("assets\\images\\tile\\square.png", (16,16))

def tile_test(tile_position, layer): 
    tile = Tile(tile_position, tile_visual, layer=layer, collision_sound="assets\\sound\\effects\\test_1.ogg")
    tile.updates.append(
        destroy_update
    )
    return tile

def test(self, id): #all test
    i, j = self.id_to_int(id)
    all_tiles = []

    if i==0 and j==0: 
        all_tiles.append(Player(
            position=(0,0), 
            visual=Image("assets\\images\\items\\NO_NAME.png", (16,16)), 
            name="player1", 
            health=100, 
            player_input=Input(start_settings["player_input"])))
    else: 
        for n in range(10):
            for m in range(10):
                for layer in range(4 if n % 4 == 0 and m % 4 == 0 else 1):
                    tile = tile_test((n + i * 10, m + j * 10), layer)
                    tile.collision = layer == 1
                    all_tiles.append(tile)
        
    all_tiles.append(Sprite(
        (i * self.chunk_size + 300, j * self.chunk_size + 300), 
        Animation(read_folder("assets\\images\\animation\\portal"))))
    
    all_tiles.append(Sprite(
        (i * self.chunk_size, j * self.chunk_size), 
        Visual(text=id)))

    return all_tiles