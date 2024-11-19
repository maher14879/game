import logging
import pickle
import json
import os
import re
from copy import copy

from source.functions import Random, Vec
from source.sprite import Sprite
from source.sprite_types.sub.instance.test import test

class Loader():
    def __init__(self, random: Random, render_distance = 5, chunk_size = 1000):
        self.random = random
        self.render_distance = render_distance
        self.chunks: dict[str, list[Sprite]] = {}
        self.sprites: list[Sprite] = []
        self.chunk_size = max(chunk_size, 100)
        self.id_pattern = re.compile(r"\((-?\d+),\s*(-?\d+)\)")
        self.chunk_center = (0, 0)
        
        self.chunk_folder = "save\\chunks\\"
        self.logs_path = "save\\chunk_id.json"
    
    def load_chunk(self, id: str):
        path = self.chunk_folder + id + ".pkl"
        if not os.path.exists(path):
            self.create_chunk(id)
            return None
        
        try: 
            with open(path, "rb") as file: sprites: list[Sprite] = sprites_loaded if (sprites_loaded:=pickle.load(file)) else []
        except:
                logging.warning(f"Loader: unable to load sprites in chunk {file}")
                self.create_chunk(id)
                return None
        
        self.chunks[id] = sprites
    
    def save_logs(self, id: str, chunk: list[Sprite]):    
        try: 
            with open(self.logs_path, "r") as file: chunk_id = json.load(file)
        except:
            logging.warning(f"Loader: unable to load {self.logs_path}")
            chunk_id = {}
                
        chunk_dict: dict[str, list[tuple[int, int]]] = {}

        for sprite in chunk:
            name = str(type(sprite).__name__)
            if name in chunk_dict.keys(): chunk_dict[name] += 1
            else: chunk_dict[name] = 1
        
        chunk_id[id] = chunk_dict
            
        try:
            with open(self.logs_path, "w") as file:
                json.dump(chunk_id, file, indent=4)
        except:
            logging.warning(f"Loader: unable to save {chunk_dict}")

    def save_chunk(self, id: str, chunk: list[Sprite]):
        if not os.path.exists(self.chunk_folder): os.mkdir(self.chunk_folder)
        path = self.chunk_folder + id + ".pkl"
          
        try: 
            with open(path, "wb") as file: pickle.dump(chunk, file)
        except: 
            logging.warning(f"Loader: unable to save chunk with id {id} and classes {set([type(sprite).__name__ for sprite in chunk])}")
    
    def setup(self, load: bool):
        for i in range(-self.render_distance, self.render_distance + 1):
            for j in range(-self.render_distance, self.render_distance + 1):
                id = str((i, j))
                if load: self.load_chunk(id)
                else: self.create_chunk(id)
        
        self.update_sprites()
        
        if not load: return None      
        try:
            with open(self.logs_path, "w") as file:
                json.dump({}, file, indent=4)
        except: logging.warning(f"Loader: unable to reset {self.logs_path}")
    
    def save(self):
        self.sort_sprites()
        for id, chunk in self.chunks.items(): self.save_logs(id, [sprite for sprite in chunk if not sprite.kill_on_update])
        self.remove_chunks()
    
    def chunk_update(self, center: Vec):
        if not self.chunk_center == (new_center := center.mul(1 / self.chunk_size).to_tuple(True)):
            self.chunk_center = new_center
            print("updating", (self.chunk_center))
            self.add_chunks()
            self.update_sprites()
        
    def sort_sprites(self):
        self.chunks: dict[str, list[Sprite]] = {key: [] for key in self.chunks}
        for sprite in self.sprites: 
            if sprite.kill_on_update: continue
            i, j = sprite.position.mul(1 / self.chunk_size).to_tuple(True)
            id = str((i,j))
            if id not in self.chunks: self.load_chunk(id)
            self.chunks[id].append(sprite)
    
    def add_sprite(self, sprite: Sprite):
        i, j = sprite.position.mul(1 / self.chunk_size).to_tuple(True)
        id = str((i,j))
        if id not in self.chunks: self.chunks[id] = [sprite]
        self.chunks[id].append(sprite)
        
    def add_chunks(self):
        center_i, center_j = self.chunk_center
        for i in range(-self.render_distance, self.render_distance + 1):
            for j in range(-self.render_distance, self.render_distance + 1):
                id = str((i + center_i, j + center_j))
                if id not in self.chunks: self.load_chunk(id)
        
    def remove_chunks(self):
        to_remove = []
        for id in self.chunks.keys():
            if not Vec(self.id_to_int(id)).sub(Vec(self.chunk_center)).abs().less(self.render_distance):
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

    def update_sprites(self):
        self.sprites: list[Sprite] = []

        for id, chunk in self.chunks.items():
            if not chunk: continue
            live_sprites = []
            spawn_list = []
            
            for sprite in chunk:
                if sprite.kill_on_update: spawn_list.extend(sprite.spawn_list)
                else: live_sprites.append(sprite)
                
            self.chunks[id] = spawn_list + live_sprites
            self.sprites.extend(self.chunks[id])

    def create_chunk(self, id: str):
        self.chunks[id] = test(self, id)