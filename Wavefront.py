import numpy as np
import os
import  sys
import pymesh


from tools.utils import *

class WavefrontOBJ:
    def __init__(self, default_mtl='default_mtl'):
        self.path      = None               # path of loaded object
        self.name      = None
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [ default_mtl ]    # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        self.faces  = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)
        self.mesh = None            # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)

    def to_string(self):
        return "Mesh: {}, {} vertices, {} faces, {} vertices per face".format(self.name,
                                                                              len(self.vertices),
                                                                              len(self.faces),
                                                                              len(self.faces[0]))

    def set_vertices(self, new_vertices : np.ndarray):
        self.vertices = new_vertices.tolist()
        self.mesh = self.export_pymesh()

    def export_pymesh(self):
        verts= np.array(self.vertices)[:, :3]
        return pymesh.form_mesh(verts, self.get_faces())

    def get_faces(self):
        return np.array(self.faces)[:, :, 0]

    def get_texture_coordinates(self):
        return np.array(self.faces)[:, :, 1]

    def save_obj(self, filename: str ):
        """Saves a WavefrontOBJ object to a file

        Warning: Contains no error checking!

        """
        with open( filename, 'w' ) as ofile:
            for mlib in self.mtllibs:
                ofile.write('mtllib {}\n'.format(mlib))
            for vtx in self.vertices:
                ofile.write('v '+' '.join(['{}'.format(v) for v in vtx])+'\n')
            for tex in self.texcoords:
                ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
            for nrm in self.normals:
                ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
            if not self.mtlid:
                self.mtlid = [-1] * len(self.faces)
            poly_idx = np.argsort( np.array( self.mtlid ) )
            cur_mat = -1
            for pid in poly_idx:
                if self.mtlid[pid] != cur_mat:
                    cur_mat = self.mtlid[pid]
                    ofile.write('usemtl {}\n'.format(self.mtls[cur_mat]))
                pstr = 'f '
                for v in self.faces[pid]:
                    # UGLY!
                    vstr = '{}/{}/{} '.format(v[0]+1,v[1]+1 if v[1] >= 0 else 'X', v[2]+1 if v[2] >= 0 else 'X' )
                    vstr = vstr.replace('/X/','//').replace('/X ', ' ')
                    pstr += vstr
                ofile.write( pstr+'\n')

    @staticmethod
    def load_obj(filename: str, default_mtl='default_mtl', triangulate=False):
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
            obj_file.mesh = obj_file.export_pymesh()
            return obj_file
        except:
            print("Error when loading file {}".format(filename))