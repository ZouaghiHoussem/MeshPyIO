# MeshPyIO
A python library for 3d mesh management.
## Requirements
1. Numpy
## Documentation
This package load, form and save a Wavefront object (.obj). It loads the following information:
* vertices: Ndarray of the shape: *N*x*D*, where N is number of vertices and *D* in [2, 3]
* faces: Ndarray of the shape: *N*x*D*, where N is number of faces and *D* in [3, 4]
* texcoords: Ndarray of the shape: *N*x*2*, where N is number of vertices.
* ...
### basic operations
```python
from Wavefront import WavefrontOBJ
# Load mesh
obj = WavefrontOBJ.load_obj("test/cube.obj")

# debug information
print(obj.to_string())

# create a new mesh
# we can form a new mesh with at least vertices and faces and any other attributes
obj_new = WavefrontOBJ.form_mesh(vertices=obj.vertices, faces=obj.faces)

# save mesh
# saving a mesh include saving the texture and materials.
obj_new.save_obj("test/new_cube.obj", save_textures=True, save_materials=True)

# export the mesh to a pymesh instance
# You can export to mesh to get use of the geometry processing methods
# offered by PyMesh
obj_pymesh = obj.export_pymesh()

# Set the mesh attributes
obj_new.set_attributes()
```