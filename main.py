from Wavefront import WavefrontOBJ
import os
import pymesh
import numpy as np

file_1 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Reconstruction/energie/energie_seq_new"), "frame-0001.obj")
file_2 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Reconstruction/male/Fitted/fitted"), "smoothed-0000.obj")
file_3 = "test/cube.obj"
obj = WavefrontOBJ.load_obj(file_1)
print(obj.to_string())
print(len(obj.mtlid))
print(obj.mtllibs)
print(obj.mtls)

#obj.save_obj("test/saved.obj")
#print(obj.vertices[0])
#print(obj.faces[0])
#print(obj.faces_norm_indices[0])
#print(obj.faces_coordinates_indices[0])
#print(obj.num_vertices)
#print(obj.num_faces)
#print(obj.vertex_per_face)

#print(obj.mesh.num_vertices)
#obj.set_vertices(obj.mesh.vertices)
#obj.save_obj("test/obj1.obj")
#obj_2 = pymesh.load_mesh(file_1)
#obj_2 = WavefrontOBJ.form_mesh(vertices=obj.vertices, faces=obj.faces)
#print(obj.to_string())

#print(obj_2.vertices[0])
#print(obj_2.faces[0])
#print(obj_2.num_vertices)
#print(obj_2.num_faces)
#print(obj_2.vertex_per_face)

#obj_2.save_obj("test/saved.obj")



