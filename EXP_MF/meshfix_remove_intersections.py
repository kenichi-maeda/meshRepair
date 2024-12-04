import numpy as np
from pymeshfix import _meshfix
import open3d as o3d

infile = "../before.ply"
outfile = "no-intersections.ply"

tin = _meshfix.PyTMesh()
tin.load_file(infile)

vertices, faces = tin.return_arrays()
intersecting_faces = tin.select_intersecting_triangles()


valid_faces_mask = np.ones(len(faces), dtype=bool)
valid_faces_mask[intersecting_faces] = False

cleaned_faces = faces[valid_faces_mask]

# Save
mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(vertices)
mesh.triangles = o3d.utility.Vector3iVector(cleaned_faces)
o3d.io.write_triangle_mesh(outfile, mesh)

print(f"Cleaned mesh saved to {outfile}")
