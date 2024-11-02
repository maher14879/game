import os
import logging

def read_folder(path: str, type: None) -> list[str]:
    return os.listdir(path)

def create_new_pos(pos_1: tuple[float], box_1: tuple[float], pos_2: tuple[float], box_2: tuple[float]) -> tuple[float|None]:
    new_pos: tuple[float|None] = ()
    for i in range(min(len(pos_1), len(pos_2))):
        collision = abs(pos_1[i] - pos_2[i]) < abs(box_1[i] + box_2[i]) / 2
        new_pos[i] = pos_1[i] if not collision else None
    return new_pos