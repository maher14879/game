import pygame as pg
import logging
import sys
import json

from source.loader import Loader
from source.graphics import Graphics
from source.sounds import Sounds
from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sprite_types.tile import Tile
from source.sprite_types.sub.player import Player

from source.functions import create_new_pos, Random, Vec
from assets.data.misc import intro_text, start_settings

class Tick():
    def __init__(self, tick_speed = 30):
        self.tick_speed = tick_speed
        self.current_tick = tick_speed
    
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
        self.settings = self.read_settings()
        self.clock = pg.time.Clock()
        self.random = Random(self.settings["seed"])
        self.loader = Loader(random=self.random)
        self.tick = Tick()
        self.graphics = Graphics()
        self.sounds = Sounds()
        
        self.graphics.setup()
        
        self.graphics.intro_text(self.random.choice(intro_text))
        self.sounds.setup()
        
        self.graphics.intro_text(self.random.choice(intro_text))
        self.loader.setup()
        
    def read_settings(self):
        try: 
            with open("save\\settings.json", "r") as file: return json.load(file)
        except:
            logging.warning("Game: could not find settings")
            return start_settings
    
    def save_settings(self):
        try:
            with open("save\\settings.json", "w") as file: json.dump(file, self.settings)
        except:
            logging.warning("Game: could not save settings")
    
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

        sprites: list[Sprite] = []
        for id, chunk in self.loader.chunks.items():
            if not chunk:
                logging.warning(f"Loader: chunk with id {id} is empty")
                continue
            for sprite in chunk:
                if not isinstance(sprite, Sprite):
                    logging.warning(f"Game: sprite removed due to being sprite {sprite}")
                    continue
                if isinstance(sprite, Entity) and sprite.kill:
                    self.loader.chunks[id].remove(sprite)
                    continue
                sprites.append(sprite)
                
        entities = [sprite for sprite in sprites if isinstance(sprite, Entity) or issubclass(type(sprite), Entity)]
        tiles = [sprite for sprite in sprites if isinstance(sprite, Tile) or issubclass(type(sprite), Tile)]
        players = [entity for entity in entities if isinstance(entity, Player) or issubclass(type(sprite), Player)]
        
        if players: 
            new_average = Vec((0,0))
            for player in players:
                new_average = new_average.add(player.position)  
            self.average_position = new_average.mul(1 / len(players))
        
        if tick_update: self.loader.chunk_update(self.average_position)
        for sprite in sprites:
            sprite.update(dt)
            sprite.interact_update(sprites)
            if tick_update: sprite.tick_update()

        for entity in entities:
            new_position = entity.new_position(dt)
            for tile in tiles:
                collide_update = create_new_pos(new_position, entity.box, tile.position, entity.box)
                if not all(collide_update): 
                    tile.collision_update(entity)
                    entity.update_position(collide_update)
                    break
            entity.update_position(new_position)

        self.graphics.update(dt, self.average_position, sprites)