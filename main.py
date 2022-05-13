from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

from map import *

app = Ursina(borderless=False)

def main() -> None:
    per_vertex_path_tracing = False

    map_size = (16, 6, 16)

    map = Map(per_vertex_path_tracing, map_size)

    player = FirstPersonController(position = (1.5, 0, 1.5), scale = 0.8)
    player.jump_height = 0
    player.gravity = 0
    player.y = 1

    camera.fov = 90

    window.exit_button.enabled = False

    app.run()

if __name__ == '__main__':
    main()