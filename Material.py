import numpy as np
import os
from tools.utils import *
from shutil import copyfile


class Material:
    def __init__(self, newmtl='default_mtl'):
        # material name
        self.newmtl = newmtl
        # texture map info
        self.map_Kd = ''
        # color and illunination info
        self.Ns = -1        # Ns exponent , Specifies the specular exponent for the current material.
        self.Ka = []        # The Ka statement specifies the ambient reflectivity using RGB values.
        self.Kd = []        # The Kd statement specifies the diffuse reflectivity using RGB values.
        self.Ks = []        # The Ks statement specifies the specular reflectivity using RGB values.
        self.Ke = []
        self.Ni = -1
        self.d = -1         # Specifies the dissolve for the current material.
        self.illum = -1     # The illum statement specifies the illumination model to use in the material.
        self.face_indices = [] # indices of associated faces of the object

    def append_face(self, face_index):
        self.face_indices.append(face_index)

    def to_string(self):
        """
        convert the material to string.
        :param formatted: if True the returned sting respects the standard of MTL files.
        """
        msg = "\n\nnewmtl {}".format(self.newmtl)
        if not(self.map_Kd == ''):
            msg += "\nmap_Kd {}".format(self.map_Kd)
        if not(self.Ns == -1):
            msg += "\nNs {}".format(self.Ns)
        if not(len(self.Ka) == 0):
            msg += "\n"+format_data(np.array(self.Ka), 'Ka')
        if not(len(self.Kd) == 0):
            msg += "\n"+format_data(np.array(self.Kd), 'Kd')
        if not(len(self.Ks) == 0):
            msg += "\n"+format_data(np.array(self.Ks), 'Ks')
        if not(len(self.Ke) == 0):
            msg += "\n"+format_data(np.array(self.Ke), 'Ke')
        if not(self.Ni == -1):
            msg += "\nNi {}".format(self.Ni)
        if not(self.d == -1):
            msg += "\nd {}".format(self.d)
        if not(self.illum == -1):
            msg += "\nillum {}".format(self.illum)

        return msg

    def set_material(self, **keywds):
        if "newmtl" in keywds:
            self.newmtl = keywds["newmtl"]
        if "map_Kd" in keywds:
            self.map_Kd = keywds["map_Kd"]
        if "Ns" in keywds:
            self.Ns = keywds["Ns"]
        if "Ka" in keywds:
            self.Ka = keywds["Ka"]
        if "Kd" in keywds:
            self.Kd = keywds["Kd"]
        if "Ks" in keywds:
            self.Ks = keywds["Ks"]
        if "Ke" in keywds:
            self.Ke = keywds["Ke"]
        if "Ni" in keywds:
            self.Ni = keywds["Ni"]
        if "d" in keywds:
            self.d = keywds["d"]
        if "illum" in keywds:
            self.illum = keywds["illum"]

    @staticmethod
    def default_color(material_name="Default"):
        mtl = Material.form_material(newmtl=material_name,
                                     Ns=0,
                                     illum=0,
                                     d=1,
                                     Kd=[0.8, 0.8, 0.8],
                                     Ka=[0.8, 0.8, 0.8],
                                     Ks=[0.8, 0.8, 0.8])
        return mtl

    @staticmethod
    def form_material(**keywds):
        """
        form a material using the provided attributes
        """
        mtl = Material()
        mtl.set_material(**keywds)
        return mtl


class MaterialLibrary:
    def __init__(self, default_name="materials"):
        self.path = ""                  # file path
        self.name = default_name        # file name
        self.mtls = []                  # material list

    def load(self, file_path):
        self.path = os.path.dirname(file_path)
        self.name = os.path.basename(file_path)
        curr_mtl = -1
        try:
            with open(file_path, 'r') as mtlf:
                for idex, line in enumerate(mtlf):
                    s_line = line.split()
                    if not s_line:
                        continue
                    if s_line[0] == 'newmtl':
                        curr_mtl = self.insert(Material(s_line[1]))

                    if s_line[0] == 'map_Kd' and curr_mtl >= 0:
                        self.mtls[curr_mtl].map_Kd = s_line[1]
                    if s_line[0] == 'Ns' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Ns = float(s_line[1])
                    if s_line[0] == 'Ka' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Ka = np.array([float(v) for v in s_line[1:]], dtype=np.float_)
                    if s_line[0] == 'Kd' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Kd = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ks' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Ks = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ke' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Ke = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ni' and curr_mtl >= 0:
                        self.mtls[curr_mtl].Ni = float(s_line[1])
                    if s_line[0] == 'd' and curr_mtl >= 0:
                        self.mtls[curr_mtl].d = float(s_line[1])
                    if s_line[0] == 'illum' and curr_mtl >= 0:
                        self.mtls[curr_mtl].illum = int(s_line[1])
        except FileNotFoundError:
            print("Error 02: no file found, check path: {}".format(file_path))
            sys.exit()

    def to_string(self):
        msg = "___{}___".format(self.name)
        for mtl in self.mtls:
            msg += "{}".format(mtl.to_string())
        return msg

    def get_mtl_names(self):
        names = []
        for mtl in self.mtls:
            names.append(mtl.newmtl)
        return names

    def save(self, file_path, save_texture=True):
        """
        save the material file
        :param file_path: the saving path
        :param save_texture:
        """
        with open(file_path, 'w') as ofile:
            ofile.write("# Generated with MeshPyIO\n# Material Count: {}\n".format(len(self.mtls)))
            for mtl in self.mtls:
                # adding material to the file
                ofile.write(mtl.to_string())
                # coping texture
                if (mtl.map_Kd != '') and save_texture:
                    if os.path.exists(os.path.join(file_path, mtl.map_Kd)):
                        print("Warning: texture file was not copied, a copy exist already")
                    else:
                        copyfile(os.path.join(self.path, mtl.map_Kd),
                                 os.path.join(os.path.dirname(file_path), mtl.map_Kd))

    def insert(self, material: Material):
        if self.index_of(material.newmtl) >= 0:
            return -1
        else:
            self.mtls.append(material)
            return len(self.mtls)-1

    def index_of(self, material_name):
        for index, mtl in enumerate(self.mtls):
            if material_name == mtl.newmtl:
                return index
        return -1

    @staticmethod
    def load_mtlib(path):
        mtllib = MaterialLibrary()
        mtllib.load(path)
        return mtllib

    @staticmethod
    def default_mtlib(file_name="Default_mtl"):
        mtllib = MaterialLibrary(file_name)
        mtllib.mtls.append(Material.default_color())
        return mtllib


if __name__ == "__main__":
    # form material
    # mat = Material.form_material(newmtl=mat[0].newmtl, map_Kd=mat[0].map_Kd, file_name=mat[0].file_name))

    # load mtlib
    path = os.path.expanduser("~/Documents/These/FaceFitting_FWHSE/testCode/export/frame-0174.mtl")
    mtlibs = MaterialLibrary.load_mtlib(path)

    # add a new material
    mtlibs.insert(Material.default_color("white"))
    # remove material
    #mtlibs.mtls.pop(1)
    # print mtlib data
    print(mtlibs.to_string())
    # sae mtlib file
    mtlibs.save(os.path.expanduser("~/Documents/These/FaceFitting_FWHSE/testCode/export/frame-0174_2.mtl"))

    #print(mtlibs.index_of("white_"))
    #mtllib = MaterialLibrary.default_mtlib()
    #print(mtllib.to_string())
    #mtllib.save("test/save/tt/default.mtl")
