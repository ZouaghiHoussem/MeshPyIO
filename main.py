from Wavefront import  *
import os
import pymesh


file_1 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Energie/energie_aligned_male"), "frame-0000.obj")
file_2 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Male/Fitted/fitted"), "smoothed-0000.obj")

obj = load_obj(file_1, triangulate=False)
print(obj.to_string())
print(obj.faces[0])
print(obj.mtls[obj.mtlid[0]])

#save_obj(obj, "test/obj1.obj")
obj_2 = pymesh.load_mesh(file_1)
print(obj_2.faces[0])



