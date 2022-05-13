from ursina import *
from panda3d.core import PNMImage
from direct.showbase.Loader import Loader
from panda3d.core import SamplerState

class Map(Entity):
    def __init__(self, per_vertex, map_size):
        if per_vertex == False: frag = open("shaders/frag.glsl", "r");            vert = open("shaders/vert.glsl", "r")
        else:                   frag = open("shaders/frag_per_vertex.glsl", "r"); vert = open("shaders/vert_per_vertex.glsl", "r")

        shader = Shader(vertex = vert.read(), fragment = frag.read())
        frag.close(); vert.close()


        map_a = [PNMImage() for i in range(map_size[1])]
        for i, img in enumerate(map_a):
            img.read(f"map/map_a_y{i}.tiff")

        map_e = [PNMImage() for i in range(map_size[1])]
        for i, img in enumerate(map_e):
            img.read(f"map/map_e_y{i}.tiff")


        verts = []
        tris = []
        colors = []
        norms = []

        trisNumb = 0

        def makePlane(x, y, z, verts_coords, normal, color, emmisive):
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

            colors.append(Vec4(color, emmisive))
            colors.append(Vec4(color, emmisive))
            colors.append(Vec4(color, emmisive))
            colors.append(Vec4(color, emmisive))
            norms.append(normal)
            norms.append(normal)
            norms.append(normal)
            norms.append(normal)

        def getMapVal(x, y, z):
            if x < 0 or x > (map_size[0] - 1) or z < 0 or z > (map_size[2] - 1) or y < 0 or y > (map_size[1] - 1):
                return 1
            elif map_a[y].getXel(x, z) == (0, 0, 0):
                return 0

        for y in range(map_size[1]):
            for x in range(map_size[0]):
                for z in range(map_size[2]):
                    if not getMapVal(x, y, z) == 0:
                        cur_color = map_a[y].getXel(x, z)

                        emmisive = 0
                        if map_e[y].getRed(x, z) != 0.0:
                            emmisive = 1

                        px = getMapVal(x + 1, y, z)
                        nx = getMapVal(x - 1, y, z)
                        pz = getMapVal(x, y, z + 1)
                        nz = getMapVal(x, y, z - 1)
                        py = getMapVal(x, y + 1, z)
                        ny = getMapVal(x, y - 1, z)

                        if px == 0:
                            makePlane(x, y, z, [(1,0,0), (1,0,1), (1,1,0), (1,1,1)], (1, 0, 0), cur_color, emmisive)
                        if nx == 0:
                            makePlane(x, y, z, [(0,0,1), (0,0,0), (0,1,1), (0,1,0)], (-1, 0, 0), cur_color, emmisive)
                        if pz == 0:
                            makePlane(x, y, z, [(1,0,1), (0,0,1), (1,1,1), (0,1,1)], (0, 0, 1), cur_color, emmisive)
                        if nz == 0:
                            makePlane(x, y, z, [(0,0,0), (1,0,0), (0,1,0), (1,1,0)], (0, 0, -1), cur_color, emmisive)
                        if py == 0:
                            makePlane(x, y, z, [(0,1,0), (1,1,0), (0,1,1), (1,1,1)], (0, 1, 0), cur_color, emmisive)
                        if ny == 0:
                            makePlane(x, y, z, [(0,0,1), (1,0,1), (0,0,0), (1,0,0)], (0, -1, 0), cur_color, emmisive)

        super().__init__(
            shader = shader,
            model = Mesh(vertices = verts, triangles = tris, colors = colors, normals = norms),
            position = (0, 0, 0)
        )

        map_tex_a = Loader.load3DTexture(None, "map/map_a_y#.tiff", minfilter = SamplerState.FT_nearest, magfilter = SamplerState.FT_nearest)
        self.set_shader_input("map_a", map_tex_a)

        map_tex_e = Loader.load3DTexture(None, "map/map_e_y#.tiff", minfilter = SamplerState.FT_nearest, magfilter = SamplerState.FT_nearest)
        self.set_shader_input("map_e", map_tex_e)

        self.set_shader_input("map_size", map_size)