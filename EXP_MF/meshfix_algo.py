from pymeshfix import _meshfix

infile = "../before.ply"
tin = _meshfix.PyTMesh()
tin.load_file(infile)

v, f = tin.return_arrays()
print(v)
print(f[::-1])
faces = tin.select_intersecting_triangles()
print(faces)