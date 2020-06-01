import numpy as np
import re
import sys

def parse_vertex(vstr):
    vals = vstr.split('/')
    vid = int(vals[0]) - 1
    tid = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else -1
    nid = int(vals[2]) - 1 if len(vals) > 2 else -1
    return vid, tid, nid

def format_data(array, key:str, conv_str=False):
    np.set_printoptions(threshold=sys.maxsize)
    arr = array.astype('str')
    if len(arr.shape) == 1:
        row_data = np.append(key, arr)
    else:
        row_data = np.append(np.tile(key, (len(arr), 1)), arr, axis=0)
    str_data = np.array2string(row_data, separator=' ')
    str_data = re.sub('[\[\'\]]', '', str_data).replace(' {}'.format(key), '{}'.format(key))
    return str_data