from source.sprite_types.tile import Tile
from source.sprite_types.particle import Particle
from source.visual import Image

from copy import copy

def destroy_update(self: Tile, dt):
    if self.play_sound > 0:
        self.kill = True
        particle = copy(test_particle)
        particle.position = self.position
        self.spawn_list.append(particle)
        

particle_visual = Image("assets\\images\\status_effects\\wet.png", (16, 16))
test_particle = Particle((0,0), particle_visual, 2, None, (1,1), 10, 100, 10)

tile_visual = Image("assets\\images\\tile\\flame_brick.png", (16,16))
tile_test = Tile((0,0), tile_visual, collision_sound="assets\\sound\\effects\\test_1.ogg")
tile_test.updates.append(
    destroy_update
)