import numpy as np
import os
from tools.utils import *


class Material:
    def __init__(self, file_name="default_mtl"):
        self.file = file_name
        self.name = ''  # name : newmtl
        self.map_Kd = ''  # texture : map_Kd
        self.Ns = -1
        self.Ka = []
        self.Kd = []
        self.Ks = []
        self.Ke = []
        self.Ni = -1
        self.d = -1
        self.illum = -1

    def save(self, file_path):
        with open(file_path, 'w') as ofile:
            ofile.write("#generated with MeshPyIO\n")
            ofile.write(self.to_string(formatted=True))

    def to_string(self, formatted=False):
        msg = ""
        if not formatted:
            msg += "______Begin: {}_____".format(self.file)
        msg += "\nnewmtl {}".format(self.name)
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
            msg += "\n______End: {}_____".format(self.file)
        return msg

    @staticmethod
    def form_material(*args, **keywds):
        if "newmtl" not in keywds:
            print("Error: Could not form material: newmtl was not provided")
            return None

    @staticmethod
    def load(filename):
        mtl = Material(file_name=os.path.basename(filename))
        try:
            with open(filename, 'r') as mtlf:
                for line in mtlf:
                    s_line = line.split()
                    #print(s_line)
                    if not s_line:
                        continue
                    if s_line[0] == 'newmtl':
                        mtl.name = s_line[1]
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
            print("Error when loading material {}".format(filename))
        return mtl


file_1 = os.path.join(os.path.expanduser("~/Documents/DATAs/Tibi/Reconstruction/energie/energie_seq_new"), "frame-0001.mtl")
file_3 = "test/untitled.mtl"

mtl = Material.load(file_1)
print(mtl.to_string())
mtl.save('test/saved.mtl')
