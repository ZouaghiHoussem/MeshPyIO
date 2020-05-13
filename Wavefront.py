import numpy as np
import os
import sys
import pymesh
from tools.utils import *


class WavefrontOBJ:
    def __init__(self, default_mtl='default_mtl'):
        """
        initialise an empty mesh
        :param default_mtl: default material
        """
        self.path      = None               # path of loaded object
        self.name      = None
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [default_mtl]      # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        # Face elements
        self.faces  = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)
        self.faces_coordinates_indices   =[]
        self.faces_norm_indices          = []
        self.mesh = None            # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)
        self.num_vertices = 0
        self.num_faces = 0
        self.vertex_per_face = 0

    def to_string(self):
        """
        export mesh information.
        """
        return "Mesh: {}, {} vertices, {} faces, {} vertices per face".format(self.name,
                                                                              self.vertices.shape[0],
                                                                              self.faces.shape[0],
                                                                              len(self.faces[0]))

    def set_vertices(self, new_vertices: np.ndarray):
        """
        update mesh vertices and pymesh mesh attribute.
        :param new_vertices: the new vertices
        """
        self.vertices = new_vertices.copy()
        self.mesh = self.export_pymesh()

    def export_pymesh(self):
        """
        export a pymesh instance of the current mesh object.
        """
        return pymesh.form_mesh(self.vertices, self.faces)

    def save_obj(self, filename: str):
        """
        save the current mesh object in a file.
        :param filename: export file path
        """
        with open(filename, 'w') as ofile:
            ofile.write("#generated with MeshPyIO\n")
            # Materials
            for mlib in self.mtllibs:
                ofile.write('mtllib {}\n'.format(mlib))
            # Vertices
            for vtx in self.vertices:
                vertex_position = 'v '+' '.join(['{}'.format(v) for v in vtx])
                # TODO ADD Vertex color later
                ofile.write(vertex_position+'\n')
            # Texture coordinates
            for tex in self.texcoords:
                ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
            # vertices normals
            for nrm in self.normals:
                ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
            # Material IDs
            if not self.mtlid:
                self.mtlid = [-1] * len(self.faces)
            poly_idx = np.argsort( np.array( self.mtlid ) )
            cur_mat = -1
            for pid in poly_idx:
                if self.mtlid[pid] != cur_mat and len(self.mtllibs)>0:
                    cur_mat = self.mtlid[pid]
                    ofile.write('usemtl {}\n'.format(self.mtls[cur_mat]))
                pstr = 'f'
                vstr = ''
                for index in range(self.vertex_per_face):
                    # face index
                    vstr += " {}".format(self.faces[pid][index]+1)

                    # faces_coordinates_indices
                    if len(self.faces_coordinates_indices) > 0 and self.faces_coordinates_indices[pid][0] >= 0:
                        vstr += "/{}".format(self.faces_coordinates_indices[pid][index]+1)

                    # faces_norm_indices
                    if len(self.faces_norm_indices) > 0 and self.faces_norm_indices[pid][0] >= 0:
                        if len(self.faces_coordinates_indices) < 0 or self.faces_coordinates_indices[pid][0] < 0:
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
        obj_file = WavefrontOBJ(default_mtl ="default_mtl")
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

        if "faces_coordinates_indices" in keywds:
            obj_file.faces_coordinates_indices = keywds["faces_coordinates_indices"]
        if "faces_norm_indices" in keywds:
            obj_file.faces_norm_indices = keywds["faces_norm_indices"]

        obj_file.mesh = obj_file.export_pymesh()
        return obj_file

    @staticmethod
    def load_obj(filename: str, default_mtl='default_mtl', triangulate=False):
        """
        Load a mesh object from an obj file.
        """
        # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
        # and returns a 3-tuple where unparsed values are replaced with -1
        obj_file = WavefrontOBJ(default_mtl=default_mtl)
        try:
            with open(filename, 'r') as objf:
                obj_file.path = filename
                obj_file.name = os.path.basename(filename)
                cur_mat = obj_file.mtls.index(default_mtl)
                for line in objf:
                    toks = line.split()
                    if not toks:
                        continue
                    if toks[0] == 'v':
                        obj_file.vertices.append([float(v) for v in toks[1:]])
                    elif toks[0] == 'vn':
                        obj_file.normals.append([float(v) for v in toks[1:]])
                    elif toks[0] == 'vt':
                        obj_file.texcoords.append([float(v) for v in toks[1:]])
                    elif toks[0] == 'f':
                        poly = [parse_vertex(vstr) for vstr in toks[1:]]
                        if triangulate:
                            for i in range(2, len(poly)):
                                obj_file.mtlid.append(cur_mat)
                                obj_file.faces.append((poly[0], poly[i - 1], poly[i]))
                        else:
                            obj_file.mtlid.append(cur_mat)
                            obj_file.faces.append(poly)
                    elif toks[0] == 'mtllib':
                        obj_file.mtllibs.append(toks[1])
                    elif toks[0] == 'usemtl':
                        if toks[1] not in obj_file.mtls:
                            obj_file.mtls.append(toks[1])
                        cur_mat = obj_file.mtls.index(toks[1])

            obj_file.vertices = np.array(obj_file.vertices)[:, :3]
            _faces = np.array(obj_file.faces)
            obj_file.faces = _faces[:, :, 0]
            obj_file.faces_coordinates_indices = _faces[:, :, 1]
            obj_file.faces_norm_indices = _faces[:, :, 2]
            obj_file.num_vertices = obj_file.vertices.shape[0]
            obj_file.num_faces = obj_file.faces.shape[0]
            obj_file.vertex_per_face = obj_file.faces[0].shape[0]
            obj_file.mesh = obj_file.export_pymesh()
            return obj_file
        except:
            print("Error when loading file {}".format(filename))