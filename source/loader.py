import logging
import pickle
import os
import re
from copy import copy

from source.functions import Random, Vec

from source.visual import Animation, Visual, Image #testing
from source.sprite_types.sub.player import Player #testing
from assets.data.misc import start_settings #testing
from source.get_input import Input #testing
from source.sprite_types.tile import Tile #testing
from source.functions import read_folder #testing
from source.sprite_types.sub.instance.test import tile_test #testing

from source.sprite import Sprite
from source.sprite_types.entity import Entity

class Loader():
    def __init__(self, random: Random, render_distance = 5, chunk_size = 1000):
        self.random = random
        self.render_distance = render_distance
        self.chunks: dict[str, list[Sprite]] = {}
        self.chunk_size = chunk_size
        self.id_pattern = re.compile(r"\((-?\d+),\s*(-?\d+)\)")
    
    def load_chunk(self, id: str):
        path = "save\\chunks\\" + id + ".pkl"
        if not os.path.exists(path):
            self.chunks[id] = self.create_chunk(id)
            return None
        
        with open(path, "rb") as file: 
            try: 
                sprites: list[Sprite] = sprites_loaded if (sprites_loaded:=pickle.load(file)) else []
                for sprite in sprites: sprite.visual.setup()
                self.chunks[id] = sprites
            except:
                logging.warning(f"Loader: unable to load sprites in chunk {file}")
                self.chunks[id] = self.create_chunk(id)

    def save_chunk(self, id: str, chunk: list[Sprite]):
        if not chunk: chunk = []
        backup = [(sprite.visual.surface, sprite.visual.figure, sprite.visual.surfaces) for sprite in chunk]
        for sprite in chunk: 
            sprite.visual.surface = None
            sprite.visual.figure = None
            sprite.visual.surfaces = None
        try: 
            with open(f"save\\chunks\\{id}.pkl", "wb") as file: pickle.dump(chunk, file)
        except: logging.warning(f"Loader: unable to save chunk with id {id} and classes {set([type(sprite).__name__ for sprite in chunk])}")
        
        for i, sprite in enumerate(chunk):
            surface, figure, surfaces = backup[i]
            sprite.visual.surface = surface
            sprite.visual.figure = figure
            sprite.visual.surfaces = surfaces
    
    def setup(self, load):
        for i in range(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                id = str((i, j))
                if load: self.load_chunk(id)
                else: self.chunks[id] = self.create_chunk(id)
    
    def save(self):
        for id, chunk in self.chunks.items():
            if not chunk: continue
            self.save_chunk(id, [sprite for sprite in chunk if not sprite.kill])
    
    def chunk_update(self, center: Vec):
        center_scaled = center.mul(1 / self.chunk_size)
        
        self.sort_sprites()
        self.add_chunks(center_scaled)
        self.remove_chunks(center_scaled)
        
    def sort_sprites(self):
        sprites = self.get_sprites()
        self.chunks: dict[str, list[Sprite]] = {}
        for sprite in sprites: 
            i, j = sprite.position.mul(1 / self.chunk_size).to_tuple(True)
            id = str((i,j))
            try: self.chunks[id].append(sprite)
            except: self.chunks[id] = [sprite]
    
    def add_sprite(self, sprite: Sprite):
        i, j = sprite.position.mul(1 / self.chunk_size).to_tuple(True)
        id = str((i,j))
        try: self.chunks[id].append(sprite)
        except: self.chunks[id] = [sprite]
        
    def add_chunks(self, center_scaled: Vec):
        center_i, center_j = center_scaled.to_tuple(True)
        for i in range(center_i - self.render_distance, center_i + self.render_distance):
            for j in range(center_j - self.render_distance, center_j + self.render_distance):
                id = str((i, j))
                if id not in self.chunks.keys(): self.chunks[id] = self.load_chunk(id)
        
    def remove_chunks(self, center_scaled: Vec):
        to_remove = []
        for id in self.chunks.keys():
            if not Vec(self.id_to_int(id)).sub(center_scaled).abs().less(self.render_distance):
                self.save_chunk(id, self.chunks[id])
                to_remove.append(id)
                
        for id in to_remove:
            self.chunks.pop(id)
        
    def id_to_int(self, id: str):
        match = self.id_pattern.match(id)
        if not match: 
            logging.warning(f"Loader: could not match id {id}")
            return (0, 0)
        i, j = match.groups()
        return int(i), int(j)

    def get_sprites(self) -> list[Sprite]:
        sprites: list[Sprite] = []
        for id, chunk in self.chunks.items():
            if not chunk: continue
            self.chunks[id] = [sprite for sprite in self.chunks[id] if not sprite.kill]
            sprites.extend(self.chunks[id])
        return sprites
                
    def create_chunk(self, id: str):
        return self.test(id)
        
    def test(self, id): #all test
        i, j =  self.id_to_int(id)
        if i==0 and j==0: 
            visual = Image("assets\\images\\items\\NO_NAME.png", (16,16))
            return [Player(position=(0,0), visual=visual, name="player1", health=100, player_input=Input(start_settings["player_input"]))]
        sprite_visual = Animation(read_folder("assets\\images\\animation\\portal"))
        sprite = Sprite((i * self.chunk_size + 300, j * self.chunk_size + 300), sprite_visual)
    
        tiles = [copy(tile_test) for _ in range(10)]
        for n, tile in enumerate(tiles): tile.position = Vec((i * self.chunk_size + 16 * n, j * self.chunk_size + 16 * n))
        return tiles + [sprite]