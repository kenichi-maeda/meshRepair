import pymesh
import numpy as np


mesh = pymesh.load_mesh("/app/before.ply")

#####################################################
# Self-intersections

#pymesh.detect_self_intersection(mesh)
#Detect all self-intersections
intersections = pymesh.detect_self_intersection(mesh)

print(f"Detected {len(intersections)} intersections.")

with open("/app/result/intersections.txt", "w") as f:
    for pair in intersections:
        f.write(f"{pair[0]}, {pair[1]}\n")


#pymesh.resolve_self_intersection(mesh, engine='auto')
#Resolve all self-intersections.
resolved_mesh = pymesh.resolve_self_intersection(mesh)
pymesh.save_mesh("/app/result/resolved_mesh.ply", resolved_mesh, ascii=True)

####################################################
# Remove isolated verticies

#pymesh.remove_isolated_vertices
isolated_verticies_removed_mesh, info = pymesh.remove_isolated_vertices(mesh)
pymesh.save_mesh("/app/result/isolated_verticies_removed_mesh.ply", isolated_verticies_removed_mesh, ascii=True)

####################################################
# Remove duplicate verticies

#pymesh.remove_duplicated_vertices
duplicated_verticies_removed_mesh, info = pymesh.remove_duplicated_vertices(mesh)
pymesh.save_mesh("/app/result/duplicated_verticies_removed_mesh.ply", duplicated_verticies_removed_mesh, ascii=True)

####################################################
# Remove duplicate faces

#pymesh.remove_duplicated_faces
duplicated_faces_removed_mesh, info = pymesh.remove_duplicated_faces(mesh)
pymesh.save_mesh("/app/result/duplicated_faces_removed_mesh.ply", duplicated_faces_removed_mesh, ascii=True)

####################################################
# Remove obtuse triangles

#remove_obtuse_triangles
obtuse_triangles_removed_mesh, info = pymesh.remove_obtuse_triangles(mesh)
pymesh.save_mesh("/app/result/obtuse_triangles_removed_mesh.ply", obtuse_triangles_removed_mesh, ascii=True)

####################################################
# Remove degenerate triangles

#remove_degenerated_triangles
degenerated_triangles_removed_mesh, info = pymesh.remove_degenerated_triangles(mesh)
pymesh.save_mesh("/app/result/degenerated_triangles_removed_mesh.ply", degenerated_triangles_removed_mesh, ascii=True)

####################################################
# Separate mesh into disconnected components

#pymesh.separate_mesh
#separate_mesh = pymesh.separate_mesh(mesh)
#pymesh.save_mesh("/app/result/separate_mesh.ply", separate_mesh, ascii=True)

####################################################
# Merge multiple meshes

#pymesh.merge_meshes
# ...
