import pygame as pg
import logging
import sys
import json

from source.sounds import sounds
from source.loader import Loader
from source.graphics import Graphics
from source.visual import font_dict_setup, image_dict_setup
from source.sprite import Sprite
from source.sprite_types.entity import Entity
from source.sprite_types.tile import Tile
from source.sprite_types.sub.player import Player

from source.functions import test_collision, Random, Vec
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
        self.loader = Loader(random=self.random, chunk_size=self.settings["chunk_size"])
        self.tick = Tick()
        self.graphics = Graphics(self.settings["scale"])
        
        font_dict_setup(self.settings["scale"])
        self.graphics.setup()
        
        self.graphics.intro_text(self.random.choice(intro_text))
        sounds.setup()
        
        self.graphics.intro_text(self.random.choice(intro_text))
        image_dict_setup(self.settings["scale"])
        
        self.graphics.intro_text(self.random.choice(intro_text))
        self.loader.setup(self.settings["load"])
        
    def read_settings(self):
        try: 
            with open("save\\settings.json", "r") as file: return json.load(file)
        except:
            logging.warning("Game: could not find settings")
            return start_settings
    
    def save_settings(self):
        try: 
            with open("save\\settings.json", "w") as file: json.dump(self.settings, file)
        except: logging.warning("Game: could not save settings")
    
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

        sprites = self.loader.get_sprites()

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
            for spawn_sprite in sprite.spawn_list: self.loader.add_sprite(spawn_sprite)
            if tick_update: sprite.tick_update()

        for entity in entities:
            target = entity.new_position(dt)
            x_collide, y_collide = False, False
            for tile in tiles:
                x, y = test_collision(entity.position, target, entity.box, tile.position, tile.box)
                if x or y: tile.collision_update(entity)
                x_collide = x_collide or x
                y_collide = y_collide or y
            
            target.x = target.x if not x_collide else None
            target.y = target.y if not y_collide else None
            entity.position.update(target.to_tuple())

        self.graphics.update(dt, self.average_position, sprites)