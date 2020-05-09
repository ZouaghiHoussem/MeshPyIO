def parse_vertex(vstr):
    vals = vstr.split('/')
    vid = int(vals[0]) - 1
    tid = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else -1
    nid = int(vals[2]) - 1 if len(vals) > 2 else -1
    return (vid, tid, nid)