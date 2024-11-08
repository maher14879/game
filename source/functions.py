import os
import logging
import math
import random

def read_folder(path: str, file_type: str = None) -> list[str]:
    if not os.path.exists(path):
        logging.warning(f"Functions: read_folder path does not exist {path}")
        return []
    
    path_list = []
    for file in os.listdir(path):
        joined_path = os.path.join(path, file)
        if not file_type or file.endswith(file_type): path_list.append(joined_path)
        elif os.path.isdir(path): path_list += read_folder(joined_path, file_type)
    return path_list

class Vec():
    def __init__(self, x_y= tuple[float, float]):
        if type(x_y) == Vec: x, y = x_y.to_tuple()
        else: x, y = x_y
        self.x = float(x)
        self.y = float(y)
        
    def to_tuple(self, integer: bool = False): return (round(self.x), round(self.y)) if integer else (self.x, self.y)
    
    def update(self, x_y: tuple[float|None, float|None]):
        x, y = x_y
        self.x = x if not x == None else self.x
        self.y = y if not y == None else self.y
    
    def mul(self, scale: float): 
        if type(scale) == Vec: scale_x, scale_y = scale.to_tuple()
        else: scale_x, scale_y = scale, scale
        return Vec((self.x * scale_x, self.y * scale_y))

    def add(self, vec: "Vec"): return Vec((self.x + vec.x, self.y + vec.y))
    
    def sub(self, vec: "Vec"): return Vec((self.x - vec.x, self.y - vec.y))

    def max(self, vec: "Vec"): return Vec((max(self.x, vec.x), max(self.y, vec.y)))

    def abs(self): return Vec((abs(self.x), abs(self.y)))
    
    def rot(self, rad): 
        rot_x = Vec(math.cos(rad),-math.sin(rad))
        rot_y = Vec(math.sin(rad), math.cos(rad))
        return Vec((self.dot(rot_x), self.dot(rot_y)))
    
    def relu(self): return Vec((max(0, self.x), max(0, self.y)))
    
    def less(self, scale: float): 
        if type(scale) == Vec: scale_x, scale_y = scale.to_tuple()
        else: scale_x, scale_y = scale, scale
        return self.x < scale_x and self.y < scale_y
    
    def len(self): return (self.x**2 + self.y**2)**0.5
    
    def len_sqr(self): return (self.x**2 + self.y**2)
    
    def dot(self, vec: "Vec"): return self.x * vec.x + self.y * vec.y
    
    def norm(self):
        length = self.len()
        if length == 0:
            return Vec(0, 0)
        return Vec((self.x / length, self.y / length))
    
    def collides_with(self, box: "Vec", obstacle: "Vec", obstacle_box: "Vec") -> bool:
        return (
            self.x < obstacle.x + obstacle_box.x and
            self.x + box.x > obstacle.x and
            self.y < obstacle.y + obstacle_box.y and
            self.y + box.y > obstacle.y
        )

    def collide_distance(self, box: "Vec", obstacle: "Vec", obstacle_box: "Vec") -> float:
        self = self.add(box.mul(0.5))
        obstacle = obstacle.add(obstacle_box.mul(0.5))
        distance = self.sub(obstacle).abs()
        overlap = distance.sub(box.mul(0.5).add(obstacle_box.mul(0.5))).relu()
        return overlap.len_sqr()

def test_collision(origin: Vec, target: Vec, box: Vec, obstacle: Vec, obstacle_box: Vec) -> tuple[float, float | None]:
    if not target.collides_with(box, obstacle, obstacle_box): return (False, False)

    origin_distance = origin.collide_distance(box, obstacle, obstacle_box)
    
    delta_x_distance = Vec((target.x, origin.y)).collide_distance(box, obstacle, obstacle_box)
    if 0 < delta_x_distance <= origin_distance: return (False, True)

    delta_y_distance = Vec((origin.x, target.y)).collide_distance(box, obstacle, obstacle_box)
    if 0 < delta_y_distance <= origin_distance: return (True, False)

    return (True, True)

class Random():
    def __init__(self, seed):
        self.seed = seed
    
    def integer(self, min: 0, max: 1) -> int:
        pass
    
    def floating(self, min: 0, max: 1) -> float:
        pass
    
    def choice(self, sequence: list|tuple):
        return sequence[random.randint(0, len(sequence) - 1)]

    def order(self, input_list: list[str]) -> list[int]:
        """Randomly reorder a list

        Args:
            input_list (list[str]): list of strings created from all relevant information at that index

        Returns:
            list[int]: Index list
        """
        pass