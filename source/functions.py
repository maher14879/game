import os
import logging

def read_folder(path: str, file_type: None) -> list[str]:
    if not os.path.exists(path):
        logging.warning(f"Functions: read_folder path does not exist {path}")
        return []
    
    path_list = []
    for file in os.listdir(path):
        joined_path = os.path.join(path, file)
        if file.endswith(file_type): path_list.append(joined_path)
        elif os.path.isdir(path): path_list += read_folder(joined_path, file_type)
    return path_list

class Vec():
    def __init__(self, x_y= tuple[float, float]):
        if type(x_y) == Vec: x, y = x_y.to_tuple()
        else: x, y = x_y
        self.x = float(x)
        self.y = float(y)
        
    def to_tuple(self, int: bool = False): return (round(self.x), round(self.y)) if round else (self.x, self.y)
    
    def update(self, vec: "Vec"):
        self.x = vec.x if vec.x else self.x
        self.y = vec.y if vec.y else self.y
    
    def mul(self, scale: float): 
        if type(scale) == Vec: scale_x, scale_y = scale.to_tuple()
        else: scale_x, scale_y = scale, scale
        return Vec((self.x * scale_x, self.y * scale_y))

    def add(self, vec: "Vec"): return Vec((self.x + vec.x, self.y + vec.y))
    
    def sub(self, vec: "Vec"): return Vec((self.x - vec.x, self.y - vec.y))

    def max(self, vec: "Vec"): return Vec((max(self.x, vec.x), max(self.y, vec.y)))
    
    def less(self, vec: "Vec"): return self.x < vec.x or self.y < vec.y
    
    def len(self): return (self.x**2 + self.y**2)**0.5
    
    def len_sqr(self): return (self.x**2 + self.y**2)
    
    def dot(self, vec: "Vec"): return self.x * vec.x + self.y * vec.y
    
    def norm(self):
        length = self.len()
        if length == 0:
            return Vec(0, 0)
        return Vec((self.x / length, self.y / length))

def create_new_pos(origin: Vec, target: Vec, box: Vec, obstacle: Vec, obstacle_box: Vec) -> tuple[float|None]:
    new_pos = target
    if not new_pos.less(obstacle.add(obstacle_box)) and obstacle.less(new_pos.add(box)):
        return (target.x, target.y)
    
    new_pos = Vec(origin.x, target.y)
    if not new_pos.less(obstacle.add(obstacle_box)) and obstacle.less(new_pos.add(box)): 
        return (None, target.y)
    
    new_pos = Vec(target.x, origin.y)
    if not new_pos.less(obstacle.add(obstacle_box)) and obstacle.less(new_pos.add(box)): 
        return (target.x, None)
    
    return (None, None)

class Random():
    def __init__(self, seed):
        self.seed = seed
    
    def integer(self, min: 0, max: 1) -> int:
        pass
    
    def floating(self, min: 0, max: 1) -> float:
        pass
    
    def choice(self, sequence: list|tuple):
        return sequence[0]

    def order(self, input_list: list[str]) -> list[int]:
        """Randomly reorder a list

        Args:
            input_list (list[str]): list of strings created from all relevant information at that index

        Returns:
            list[int]: Index list
        """
        pass