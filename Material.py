import numpy as np
import os
from tools.utils import *
from shutil import copyfile

class Material:
    def __init__(self, file_name="default_mtl"):
        self.path = os.path.dirname(file_name)
        self.file_name = os.path.basename(file_name)
        self.newmtl = ''
        self.map_Kd = ''
        self.Ns = -1
        self.Ka = []
        self.Kd = []
        self.Ks = []
        self.Ke = []
        self.Ni = -1
        self.d = -1
        self.illum = -1

    def save(self, file_path, save_texture=False):
        """
        save the material file
        :param file_path: the saving path
        """
        with open(file_path, 'w') as ofile:
            ofile.write("#generated with MeshPyIO\n")
            ofile.write(self.to_string(formatted=True))
        if (self.map_Kd != '') and save_texture:
            copyfile(os.path.join(self.path, self.map_Kd),
                     os.path.join(os.path.dirname(file_path), self.map_Kd))

    def to_string(self, formatted=False):
        """
        convert the material to string.
        :param formatted: if True the returned sting respects the standard of MTL files.
        """
        msg = ""
        if not formatted:
            msg += "______Begin: {}_____".format(self.file_name)
        msg += "\nnewmtl {}".format(self.newmtl)
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
        if not formatted:
            msg += "\n______End: {}_____".format(self.file_name)
        return msg

    @staticmethod
    def form_material(*args, **keywds):
        """
        form a material using the provided attributes
        """
        mtl = Material()
        if "newmtl" not in keywds:
            print("Error: Could not form material: newmtl was not provided")
            return mtl
        if "file_name" in keywds:
            mtl.file_name = keywds["file_name"]
        mtl.newmtl = keywds["newmtl"]
        if "map_Kd" in keywds:
            mtl.map_Kd = keywds["map_Kd"]
        if "Ns" in keywds:
            mtl.Ns = keywds["Ns"]
        if "Ka" in keywds:
            mtl.Ns = keywds["Ka"]
        if "Kd" in keywds:
            mtl.Ns = keywds["Kd"]
        if "Ks" in keywds:
            mtl.Ns = keywds["Ks"]
        if "Ke" in keywds:
            mtl.Ns = keywds["Ke"]
        if "Ni" in keywds:
            mtl.Ns = keywds["Ni"]
        if "d" in keywds:
            mtl.Ns = keywds["d"]
        if "illum" in keywds:
            mtl.Ns = keywds["illum"]
        return mtl

    @staticmethod
    def load(filename):
        """
        Load a material file.
        """
        mtl = Material(file_name=filename)
        try:
            with open(filename, 'r') as mtlf:
                for line in mtlf:
                    s_line = line.split()
                    if not s_line:
                        continue
                    if s_line[0] == 'newmtl':
                        mtl.newmtl = s_line[1]
                    if s_line[0] == 'map_Kd':
                        mtl.map_Kd = s_line[1]
                    if s_line[0] == 'Ns':
                        mtl.Ns = float(s_line[1])
                    if s_line[0] == 'Ka':
                        mtl.Ka = np.array([float(v) for v in s_line[1:]], dtype=np.float_)
                    if s_line[0] == 'Kd':
                        mtl.Kd = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ks':
                        mtl.Ks = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ke':
                        mtl.Ke = np.array(([float(v) for v in s_line[1:]]), dtype=np.float_)
                    if s_line[0] == 'Ni':
                        mtl.Ni = float(s_line[1])
                    if s_line[0] == 'd':
                        mtl.d = float(s_line[1])
                    if s_line[0] == 'illum':
                        mtl.illum = int(s_line[1])
        except:
            print("Error 02: no file found, check path: {}".format(filename))
            sys.exit()
        return mtl


if __name__ == "__main__":
    file_1 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Reconstruction/energie/energie_seq_new"), "frame-0001.mtl")
    file_3 = "/home/houssem/Documents/DATAs/Tibi/Reconstruction/energie/energie_seq_new/frame-0001.mtl"
    mat = []
    mat.append(Material.load(file_1))
    mat.append(Material.load(file_3))

    #mtl_2 = Material.form_material(newmtl=mtl.newmtl, map_Kd=mtl.map_Kd, file_name=mtl.file_name)
    print(mat[1].to_string())
    #mtl_2.save('test/saved.mtl')
