import trimesh
import pyvista as pv
import sys

def plot_with_clipping(mesh, filename):
    plotter = pv.Plotter()

    # Add the initial full mesh
    #mesh_actor = plotter.add_mesh(mesh, color="white", opacity=0.6, show_edges=True, label="Repaired Mesh")
    
    mesh_actor = plotter.add_mesh(
        mesh,
        color="white",
        show_edges=True,
        edge_color="black",
        label=filename
    )

    def update_clipping_plane(value):
        new_plane = pv.Plane(center=(value, 0, 0), direction=(1, 0, 0))
        clipped_mesh = mesh.clip_surface(new_plane, invert=False)

        mesh_actor.GetMapper().SetInputData(clipped_mesh)
        mesh_actor.Modified()


    plotter.add_slider_widget(
        update_clipping_plane,
        rng=[-100, 25], 
        value=0,
        title="Clip Plane",
        pointa=(.1, .1),
        pointb=(.4, .1),
    )

    plotter.add_legend()
    plotter.show()

filename = sys.argv[1]
trimesh_obj = trimesh.load(filename)
mesh = pv.wrap(trimesh_obj)
plot_with_clipping(mesh, filename)