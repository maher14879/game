import os
import logging

def read_folder(path: str, type: None) -> list[str]:
    return os.listdir(path)

def create_new_pos(origin: tuple[float, float], target: tuple[float, float], box: tuple[float, float], obstacle: tuple[float, float], obstacle_box: tuple[float, float]) -> tuple[float|None, float|None]:
    new_pos = target
    if not any(new_pos[i] < obstacle[i] + obstacle_box[i] and obstacle[i] < new_pos[i] + box[i] for i in range(2)): return target
    new_pos = (origin[0], target[1])
    if not any(new_pos[i] < obstacle[i] + obstacle_box[i] and obstacle[i] < new_pos[i] + box[i] for i in range(2)): return (None, target[1])
    new_pos = (target[0], origin[1])
    if not any(new_pos[i] < obstacle[i] + obstacle_box[i] and obstacle[i] < new_pos[i] + box[i] for i in range(2)): return (target[0], None)
    return (None, None)

def choose_type(type: str):
    pass

class random():
    def __init__(self, seed):
        self.seed = seed
    
    def integer(self, min: 0, max: 1) -> int:
        pass
    
    def floating(self, min: 0, max: 1) -> float:
        pass

    def order(self, input_list: list[str]) -> list[int]:
        """Randomly reorder a list

        Args:
            input_list (list[str]): list of strings created from all relevant information at that index

        Returns:
            list[int]: Index list
        """
        pass