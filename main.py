from Wavefront import WavefrontOBJ
import os
import pymesh
import numpy as np

file_1 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Energie/energie_aligned_male"), "frame-0000.obj")
file_2 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Male/Fitted/fitted"), "smoothed-0000.obj")

obj = WavefrontOBJ.load_obj(file_1, triangulate=False)
print(obj.to_string())
print(obj.vertices[0])


print(obj.mesh.num_vertices)
obj.set_vertices(obj.mesh.vertices)
obj.save_obj("test/obj1.obj")
obj_2 = pymesh.load_mesh(file_1)
print(obj_2.faces[0])



