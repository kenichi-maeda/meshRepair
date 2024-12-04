import numpy as np
import pymesh
from scipy.spatial.distance import euclidean


mesh = pymesh.load_mesh("/app/before.ply")

mesh, _ = pymesh.remove_isolated_vertices(mesh)
mesh, _ = pymesh.remove_degenerated_triangles(mesh)
mesh, _ = pymesh.remove_duplicated_faces(mesh)
mesh, _ = pymesh.remove_duplicated_vertices(mesh)

intersections = pymesh.detect_self_intersection(mesh)
intersecting_faces = np.unique(intersections.flatten())
face_mask = np.array([i not in intersecting_faces for i in range(len(mesh.faces))])

print(f"Number of faces: {len(mesh.faces)}")
print(f"Number of intersecting face pairs: {len(intersections)}")



"""
# Idea1:
# Remove self-intersecting faces
pymesh.save_mesh("/app/result/resolved_mesh.ply", mesh, ascii=True)
"""



"""
#Idea 2
non_intersecting_faces = mesh.faces[face_mask]

# Extract intersecting faces and vertices
intersecting_faces_data = mesh.faces[~face_mask]
intersecting_vertices = np.unique(intersecting_faces_data.flatten())
new_vertices = mesh.vertices[intersecting_vertices]
vertex_map = {old_idx: new_idx for new_idx, old_idx in enumerate(intersecting_vertices)}
new_faces = np.array([[vertex_map[idx] for idx in face] for face in intersecting_faces_data])

# Create a mesh for the intersecting region
intersecting_mesh = pymesh.form_mesh(new_vertices, new_faces)

# Resolve self-intersections only in this part
intersecting_mesh = pymesh.resolve_self_intersection(intersecting_mesh)

# Combine vertices and faces
combined_vertices = np.vstack([mesh.vertices, intersecting_mesh.vertices])
combined_faces = np.vstack([non_intersecting_faces, intersecting_mesh.faces + len(mesh.vertices)])

final_mesh = pymesh.form_mesh(combined_vertices, combined_faces)

final_mesh, info = pymesh.remove_degenerated_triangles(final_mesh)
final_mesh, info = pymesh.remove_duplicated_faces(final_mesh)
final_mesh = pymesh.resolve_self_intersection(final_mesh)
pymesh.save_mesh("/app/Idea2.ply", final_mesh, ascii=True)

"""

"""
# Idea3
# Step 1: Separate the mesh into disconnected components
# Step 2: Process each component separately
# Step 3: Merge the repaired components back together
components = pymesh.separate_mesh(mesh, connectivity_type="auto")
print(f"Number of components: {len(components)}")


repaired_components = []
for i, component in enumerate(components):

    component, _ = pymesh.remove_degenerated_triangles(component)
    component, _ = pymesh.remove_duplicated_faces(component)
    component, _ = pymesh.remove_duplicated_vertices(component)
    component = pymesh.resolve_self_intersection(component)
    repaired_components.append(component)


repaired_mesh = pymesh.merge_meshes(repaired_components)
pymesh.save_mesh("/app/idea3.ply", repaired_mesh, ascii=True)
"""






"""
# Intersection visualization
face_mask = np.zeros(len(mesh.faces), dtype=bool)
face_mask[intersecting_faces] = True

# Extract intersecting faces and corresponding vertices
intersecting_faces_data = mesh.faces[face_mask]
intersecting_vertices = np.unique(intersecting_faces_data.flatten())
new_vertices = mesh.vertices[intersecting_vertices]
vertex_map = {old_idx: new_idx for new_idx, old_idx in enumerate(intersecting_vertices)}
new_faces = np.array([[vertex_map[idx] for idx in face] for face in intersecting_faces_data])

# Create a new highlighted mesh
highlighted_mesh = pymesh.form_mesh(new_vertices, new_faces)

# Save the highlighted mesh
pymesh.save_mesh("/app/highlighted_intersections.ply", highlighted_mesh)
"""