import pygame as pg
import logging
import sys

from source.loader import Loader
from source.graphics import Graphics
from source.sounds import Sounds
from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sprite_types.tile import Tile
from source.sprite_types.sub.player import Player

from source.functions import create_new_pos

class Tick():
    def __init__(self):
        self.tick_speed = int()
        self.current_tick = float()
    
    def update(self, dt: float) -> bool:
        self.current_tick += dt
        if self.current_tick >= self.tick_speed:
            self.current_tick -= self.tick_speed
            return True
        else: return False

class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
    
    def setup(self):
        self.clock = pg.time.Clock()
        self.loader = Loader()
        self.tick = Tick()
        self.graphics = Graphics()
        self.sounds = Sounds()
        
        self.sounds.setup()
        self.graphics.setup()
        self.loader.setup()
        
        sprites: list[Sprite] = []
        for id, chunk in self.loader.chunks.items():
            if not chunk:
                logging.warning(f"Loader: chunk with id {id} is not loaded correctly")
                continue
            for sprite in chunk:
                if isinstance(sprite, Entity) and sprite.kill:
                    self.loader.chunks[id].remove(sprite)
                    continue
                sprites.append(sprite)
                
        self.players: list[Player] = [sprite for sprite in sprites if isinstance(sprite, Player)]
    
    def save_settings(self):
        pass
    
    def run(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_settings()
                self.loader.save()
                pg.quit()
                sys.exit()
                
        if pg.key.get_pressed()[pg.K_ESCAPE]:
            pg.display.iconify()
                
        dt = self.clock.tick() / 1000
        tick_update = self.tick.update(dt)
        
        if tick_update and self.players: 
            average_position = (sum([player.position[0] for player in self.players]) / self.players.count(), 
                                sum([player.position[1] for player in self.players]) / self.players.count())
            
            self.loader.chunk_update(average_position)
        
        sprites: list[Sprite] = []
        for id, chunk in self.loader.chunks.items():
            if not chunk:
                logging.warning(f"Loader: chunk with id {id} is not loaded correctly")
                continue
            for sprite in chunk:
                if isinstance(sprite, Entity) and sprite.kill:
                    self.loader.chunks[id].remove(sprite)
                    continue
                sprites.append(sprite)
                
        for sprite in sprites:
            sprite.update(dt)
            sprite.interact_update(sprites)
            if tick_update: sprite.tick_update()
            
        entities = [sprite for sprite in sprites if isinstance(sprite, Entity)]
        tiles = [sprite for sprite in sprites if isinstance(sprite, Tile)]
        
        for entity in entities:
            new_position = entity.new_position(dt)
            for tile in tiles:
                new_position = create_new_pos(new_position, entity.box, tile.position, entity.box)
                if not all(new_position): 
                    tile.collision_update(entity)
                    break
            entity.update_position(new_position)

        self.graphics.update(sprites)