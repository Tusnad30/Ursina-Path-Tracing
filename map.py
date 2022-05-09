from ursina import *
from panda3d.core import PNMImage
from direct.showbase.Loader import Loader
from panda3d.core import SamplerState

class Map(Entity):
    def __init__(self):
        frag = open("shaders/frag.glsl", "r"); vert = open("shaders/vert.glsl", "r")
        shader = Shader(vertex = vert.read(), fragment = frag.read())
        frag.close(); vert.close()


        map = [PNMImage(), PNMImage(), PNMImage(), PNMImage(), PNMImage()]

        map[0].read("map/mapy0.png")
        map[1].read("map/mapy1.png")
        map[2].read("map/mapy2.png")
        map[3].read("map/mapy3.png")
        map[4].read("map/mapy4.png")


        verts = []
        tris = []
        colors = []
        norms = []

        trisNumb = 0

        def makePlane(x, y, z, verts_coords, normal, color):
            nonlocal trisNumb

            verts.append((verts_coords[0][0] + x, y + verts_coords[0][1], verts_coords[0][2] + z))
            verts.append((verts_coords[1][0] + x, y + verts_coords[1][1], verts_coords[1][2] + z))
            verts.append((verts_coords[2][0] + x, y + verts_coords[2][1], verts_coords[2][2] + z))
            verts.append((verts_coords[3][0] + x, y + verts_coords[3][1], verts_coords[3][2] + z))
            tris.append(1 + trisNumb)
            tris.append(2 + trisNumb)
            tris.append(0 + trisNumb)
            tris.append(1 + trisNumb)
            tris.append(3 + trisNumb)
            tris.append(2 + trisNumb)
            trisNumb += 4

            colors.append(Vec4(color, 1.0))
            colors.append(Vec4(color, 1.0))
            colors.append(Vec4(color, 1.0))
            colors.append(Vec4(color, 1.0))
            norms.append(normal)
            norms.append(normal)
            norms.append(normal)
            norms.append(normal)

        def getMapVal(x, y, z):
            if x < 0 or x > 5 or z < 0 or z > 5 or y < 0 or y > 4:
                return 1
            elif map[y].getXel(x, z) == (0, 0, 0):
                return 0

        for y in range(5):
            for x in range(6):
                for z in range(6):
                    if not getMapVal(x, y, z) == 0:
                        cur_color = map[y].getXel(x, z)
                        px = getMapVal(x + 1, y, z)
                        nx = getMapVal(x - 1, y, z)
                        pz = getMapVal(x, y, z + 1)
                        nz = getMapVal(x, y, z - 1)
                        py = getMapVal(x, y + 1, z)
                        ny = getMapVal(x, y - 1, z)

                        if px == 0:
                            makePlane(x, y, z, [(1,0,0), (1,0,1), (1,1,0), (1,1,1)], (1, 0, 0), cur_color)
                        if nx == 0:
                            makePlane(x, y, z, [(0,0,1), (0,0,0), (0,1,1), (0,1,0)], (-1, 0, 0), cur_color)
                        if pz == 0:
                            makePlane(x, y, z, [(1,0,1), (0,0,1), (1,1,1), (0,1,1)], (0, 0, 1), cur_color)
                        if nz == 0:
                            makePlane(x, y, z, [(0,0,0), (1,0,0), (0,1,0), (1,1,0)], (0, 0, -1), cur_color)
                        if py == 0:
                            makePlane(x, y, z, [(0,1,0), (1,1,0), (0,1,1), (1,1,1)], (0, 1, 0), cur_color)
                        if ny == 0:
                            makePlane(x, y, z, [(0,0,1), (1,0,1), (0,0,0), (1,0,0)], (0, -1, 0), cur_color)

        super().__init__(
            shader = shader,
            model = Mesh(vertices = verts, triangles = tris, colors = colors, normals = norms),
            position = (0, 0, 0),
            collider = "mesh"
        )

        mapTex = Loader.load3DTexture(None, "map/mapy#.png", minfilter = SamplerState.FT_nearest, magfilter = SamplerState.FT_nearest)
        self.set_shader_input("map_tex", mapTex)