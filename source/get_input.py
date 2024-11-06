import pygame as pg

key_map = {
    'a': pg.K_a, 'b': pg.K_b, 'c': pg.K_c, 'd': pg.K_d, 'e': pg.K_e, 
    'f': pg.K_f, 'g': pg.K_g, 'h': pg.K_h, 'i': pg.K_i, 'j': pg.K_j,
    'k': pg.K_k, 'l': pg.K_l, 'm': pg.K_m, 'n': pg.K_n, 'o': pg.K_o, 
    'p': pg.K_p, 'q': pg.K_q, 'r': pg.K_r, 's': pg.K_s, 't': pg.K_t, 
    'u': pg.K_u, 'v': pg.K_v, 'w': pg.K_w, 'x': pg.K_x, 'y': pg.K_y, 
    'z': pg.K_z
}

class Input():
    def __init__(self, key_binds: dict):
        self.key_binds = key_binds
    
    def get_pos_mouse():
        return pg.mouse.get_pos()
    
    def left_click():
        return pg.mouse.get_pressed()[0]

    def right_click():
        return pg.mouse.get_pressed()[1]

    def get_pressed(self, input_type: str) -> bool:
        keys = pg.key.get_pressed()
        key = self.key_binds[input_type]
        pg_key = key_map[key]
        return keys[pg_key]