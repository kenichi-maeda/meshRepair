import trimesh
import numpy as np
from scipy.spatial import Delaunay
from sklearn.decomposition import PCA

def stitch_disconnected_components(mesh):
    """
    Stitch disconnected components of a mesh by triangulating the boundary edges.
    """
    # Step 1: Identify boundary edges
    edges = {}
    for face in mesh.faces:
        for i in range(3):  # Each face has 3 edges
            edge = tuple(sorted([face[i], face[(i + 1) % 3]]))
            if edge in edges:
                edges[edge] += 1
            else:
                edges[edge] = 1

    # Boundary edges are those that appear only once
    boundary_edges = [edge for edge, count in edges.items() if count == 1]

    if not boundary_edges:
        print("No disconnected components found.")
        return mesh

    # Step 2: Group boundary edges into loops
    loops = []
    while boundary_edges:
        loop = []
        edge = boundary_edges.pop()
        loop.extend(edge)
        while True:
            # Find the next edge in the loop
            for e in boundary_edges:
                if e[0] == loop[-1]:
                    loop.append(e[1])
                    boundary_edges.remove(e)
                    break
                elif e[1] == loop[-1]:
                    loop.append(e[0])
                    boundary_edges.remove(e)
                    break
            else:
                break
        loops.append(loop)

    # Step 3: Triangulate boundary loops
    new_faces = []
    new_vertices = mesh.vertices.copy()
    for loop in loops:
        boundary_coords = new_vertices[loop]

        # Skip loops with fewer than 3 points (invalid for triangulation)
        if len(loop) < 3:
            continue

        # Align to a local plane using PCA for better triangulation
        pca = PCA(n_components=2)
        boundary_coords_2d = pca.fit_transform(boundary_coords)

        try:
            tri = Delaunay(boundary_coords_2d)
            for simplex in tri.simplices:
                new_faces.append([loop[s] for s in simplex])
        except Exception as e:
            print(f"Failed to triangulate loop with {len(loop)} points: {e}")
            continue

    # Step 4: Add new faces to the mesh
    new_faces = np.array(new_faces)
    stitched_mesh = trimesh.Trimesh(vertices=new_vertices, faces=np.vstack([mesh.faces, new_faces]))

    # Step 5: Clean up and merge
    stitched_mesh.remove_duplicate_faces()
    stitched_mesh.remove_degenerate_faces()
    stitched_mesh.remove_infinite_values()

    return stitched_mesh


# Load the PLY file
input_ply = "tetgen_removal.ply"
output_ply = "tetgen_final.ply"

# Step 1: Load the mesh
mesh = trimesh.load_mesh(input_ply)

# Step 2: Stitch the disconnected components
stitched_mesh = stitch_disconnected_components(mesh)

# Step 3: Smooth the stitched areas
stitched_mesh = stitched_mesh.smoothed()

# Step 4: Export the stitched mesh
stitched_mesh.export(output_ply)
print(f"Stitched mesh saved to {output_ply}")
