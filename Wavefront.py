import numpy as np
import os
import sys
from Material import MaterialLibrary
from tools.utils import *
import pymesh


class WavefrontOBJ:
    def __init__(self):
        """
        initialise an empty mesh
        :param default_mtl: default material
        """
        self.path = None               # path of loaded object
        self.name = None
        self.mtllibs = []              # .mtl files references via mtllib
        self.mtls = []      # materials referenced
        self.mtlid = []                # indices into self.mtls for each polygon

        # Vertex data
        self.vertices = []             # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.vertices_normals = []     # vertices_normals
        self.vertices_texture = []     # texture coordinates

        # Elements data
        self.faces = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)
        self.faces_texture_indices = []
        self.faces_norm_indices = []

        # General information
        self.num_vertices = 0
        self.num_faces = 0
        self.vertex_per_face = 0

    def load(self, filename: str, triangulate=False):
        """
        Load a mesh object from an obj file.
        """
        # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
        # and returns a 3-tuple where unparsed values are replaced with -1
        try:
            with open(filename, 'r') as objf:
                self.path = filename
                self.name = os.path.basename(filename)
                cur_mat = 0
                for line in objf:
                    toks = line.split()
                    if not toks:
                        continue
                    if toks[0] == 'v':
                        self.vertices.append([float(v) for v in toks[1:]])
                        # TODO ADD Vertex color later
                    elif toks[0] == 'vn':
                        self.vertices_normals.append([float(v) for v in toks[1:]])
                    elif toks[0] == 'vt':
                        self.vertices_texture.append([float(v) for v in toks[1:]])
                    elif toks[0] == 'f':
                        poly = [parse_vertex(vstr) for vstr in toks[1:]]
                        if triangulate:
                            for i in range(2, len(poly)):
                                self.mtlid.append(cur_mat)
                                self.faces.append((poly[0], poly[i - 1], poly[i]))
                        else:
                            self.mtlid.append(cur_mat)
                            self.faces.append(poly)
                    elif toks[0] == 'mtllib':
                        _path = os.path.join(os.path.dirname(filename), toks[1])
                        mat = MaterialLibrary.load_mtlib(_path)
                        self.mtllibs.append(mat)
                    elif toks[0] == 'usemtl':
                        if toks[1] not in self.mtls:
                            self.mtls.append(toks[1])
                        cur_mat = self.mtls.index(toks[1])

            self.vertices = np.array(self.vertices)[:, :3]
            _faces = np.array(self.faces)
            self.faces = _faces[:, :, 0]
            self.faces_texture_indices = _faces[:, :, 1]
            self.faces_norm_indices = _faces[:, :, 2]
            self.num_vertices = self.vertices.shape[0]
            self.num_faces = self.faces.shape[0]
            self.vertex_per_face = self.faces[0].shape[0]
        except:
            print("Error 003: file {} not found".format(filename))
            sys.exit()
    def set_vertices(self, vertices_list):
        self.num_vertices = vertices_list.shape[0]
        self.vertices = vertices_list.copy()

    def set_faces(self, faces):
        self.faces = faces.copy()

    def set_attributes(self, **keywds):
        """
        update the current instance attributes.
        :params keywds:
            required parameter:
                + target_object: Wavefront_obj.
            possible parameters
                * vertices: bool: True to copy vertices positions.By default it copies also face texture coordinates indices.
                * vertices_texture: bool: True to copy texture coordiates. By default it copies also materials and face
                texture coordinates.
                * mtllibs: bool: True to copy material file and ids.
                * faces: bool: True to set faces

        """

        if "vertices" in keywds:
            self.set_vertices(keywds["vertices"])

        if "faces" in keywds:
            self.set_faces(keywds["faces"])

        if "vertices_texture" in keywds:
            if len(self.vertices) == len(keywds["vertices_texture"]):
                self.vertices_texture = keywds["vertices_texture"].copy()
            else:
                # TODO: if we have less vertices we should fill the gap (first idea: set all the rest of 0,0)
                print("Warning: 002a: Error of copying textcoords, target_object has different number vertices")

        if "faces_texture_indices" in keywds:
            if len(self.faces) == len(keywds["faces_texture_indices"]):
                self.faces_texture_indices = keywds["faces_texture_indices"].copy()
            else:
                # TODO: if we have less faces we should add a default mtl and assign it's value to the rest
                print("Warning: 002b: Error of copying faces_texture_indices, target_object has different nb faces")

        if "mtllibs" in keywds:
            self.mtllibs = keywds["mtllibs"].copy()

        if "mtls" in keywds:
            self.mtls = keywds["mtls"].copy()

        if "mtlid" in keywds:
            self.mtlid = keywds["mtlid"].copy()

    def export_pymesh(self):
        """
        export the current object instance to a pymesh object.
        """
        if len(self. vertices) > 0:
            return pymesh.form_mesh(self.vertices, self.faces)
        else:
            print("Error 010: Error of creating Pymesh object")
            return None

    def to_string(self):
        """
        export mesh information.
        """
        msg = "Mesh:\t{}, {} vertices, {} faces, {} vertices per face".format(self.name,
                                                                             self.vertices.shape[0],
                                                                             self.faces.shape[0],
                                                                             self.vertex_per_face)
        if len(self.mtllibs) > 0:
            msg += "\n\tmtls:"
            for mtl in self.mtllibs:
                msg += "[{}, {}]".format(mtl.name, mtl.get_mtl_names())

        if len(self.vertices_texture) > 0:
            msg += "\n\t{} vertices_texture".format(len(self.vertices_texture))

        if len(self.faces_norm_indices) > 0:
            msg += "\n\tFacevertices_normals included"

        if len(self.vertices_normals) > 0:
            msg += ", {} Vertices vertices_normals".format(len(self.vertices_normals))

        return msg

    def save_obj(self, filename: str, save_materials=False, save_textures=False):
        """
        save the current mesh object in a file.
        :param filename: export file path
        :param save_materials: save material files in the target folder
        :param save_textures: save texture image files in the target folder
        """
        with open(filename, 'w') as ofile:
            ofile.write("#generated with MeshPyIO\n")
            # Materials
            for mlib in self.mtllibs:
                ofile.write('mtllib {}\n'.format(mlib.name))
                if save_materials:
                    for mtl in self.mtllibs:
                        mtl.save(os.path.join(os.path.dirname(filename), mtl.name), save_texture=save_textures)
            # Vertices
            for vtx in self.vertices:
                vertex_position = 'v '+' '.join(['{}'.format(v) for v in vtx])
                # TODO ADD Vertex color later
                ofile.write(vertex_position+'\n')
            # Texture coordinates
            for tex in self.vertices_texture:
                ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
            # Vertices_normals
            for nrm in self.vertices_normals:
                ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')

            # Material IDs
            if not self.mtlid:
                self.mtlid = [-1] * len(self.faces)

            poly_idx = np.argsort(np.array(self.mtlid))
            cur_mat = -1
            for pid in poly_idx:
                if len(self.mtllibs) > 0 and len(self.mtlid) > 0 and self.mtlid[pid] != cur_mat:
                    cur_mat = self.mtlid[pid]
                    ofile.write('usemtl {}\n'.format(self.mtls[cur_mat]))
                pstr = 'f'
                vstr = ''
                for index in range(self.vertex_per_face):
                    # face index
                    vstr += " {}".format(self.faces[pid][index]+1)
                    # faces_texture_indices
                    if len(self.faces_texture_indices) > 0 and self.faces_texture_indices[pid][0] >= 0:
                        vstr += "/{}".format(self.faces_texture_indices[pid][index]+1)
                    # faces_norm_indices
                    if len(self.faces_norm_indices) > 0 and self.faces_norm_indices[pid][0] >= 0:
                        if len(self.faces_texture_indices) < 0 or self.faces_texture_indices[pid][0] < 0:
                            vstr += "/"
                        vstr += "/{}".format(self.faces_norm_indices[pid][index]+1)
                pstr += vstr
                ofile.write(pstr+'\n')
    @staticmethod
    def form_mesh(*args, **keywds):
        """
        create a mesh instance using some or all parameters. The vertices and faces are always required.
        :param keywds: the parameters could be used.
        """
        obj_file = WavefrontOBJ()
        if ("vertices" not in keywds) or ("faces" not in keywds):
            print("Error: Could not form mesh: Vertices or faces was not provided")
            return None

        if keywds["vertices"].shape[1] not in [2, 3]:
            print("Error: Could not form mesh: Vertices must be 2D or 3D")
            return None

        if keywds["faces"].shape[1] not in [3, 4]:
            print("Error: Could not form mesh: faces must be tri or quad")
            return None

        obj_file.vertices = keywds["vertices"]
        obj_file.faces = keywds["faces"]
        obj_file.num_vertices = obj_file.vertices.shape[0]
        obj_file.num_faces = obj_file.faces.shape[0]
        obj_file.vertex_per_face = obj_file.faces[0].shape[0]

        if "faces_texture_indices" in keywds:
            obj_file.faces_texture_indices = keywds["faces_texture_indices"]
        if "faces_norm_indices" in keywds:
            obj_file.faces_norm_indices = keywds["faces_norm_indices"]

        return obj_file

    @staticmethod
    def load_obj(filename: str, triangulate=False):
        """
        Load a mesh object from an obj file.
        """
        # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
        # and returns a 3-tuple where unparsed values are replaced with -1
        obj_file = WavefrontOBJ()
        obj_file.load(filename, triangulate=triangulate)
        return obj_file


if __name__ == "__main__":
    path = os.path.join(os.path.expanduser("files/input"), "smoothed-0000.obj")
    obj = WavefrontOBJ.load_obj(path)
    print(obj.to_string())
    #obj_pymesh = obj.export_pymesh()
    #print(obj_pymesh.num_vertices)2
    obj.save_obj("files/file_1.obj", save_materials=True, save_textures=True)

    #obj_2 = WavefrontOBJ.load_obj(file_2, triangulate=True)
    #print(obj_2.to_string())

    #obj_2.set_attributes(vertices=obj.vertices)
    #obj.set_attributes(target_object=obj_2, vertices=True, vertices_texture=True, mtllibs=True)#, faces=True)
    #print(obj_2.to_string())
    #obj_2.save_obj("test/save/file_2_triangulate.obj", save_materials=True, save_textures=True)


