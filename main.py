from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from map import *

per_vertex_path_tracing = False

map_size = (16, 6, 16)

app = Ursina()

map = Map(per_vertex_path_tracing, map_size)

player = FirstPersonController(position = (1.5, 0, 1.5), scale = 0.8)
player.jump_height = 0
camera.fov = 90

window.borderless = False
window.exit_button.enabled = False

def update():
    player.world_position = (player.world_position.x, 1, player.world_position.z)
    player.air_time = 0

app.run()