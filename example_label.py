import open3d as o3d
import open3d.visualization.gui as gui


if __name__ == "__main__":
    app = gui.Application.instance
    app.initialize()

    w = app.create_window("Open3D - 3D Labels", 1024, 768)
    widget3d = gui.SceneWidget()
    w.add_child(widget3d)
    widget3d.scene = o3d.visualization.rendering.Open3DScene(w.renderer)

    axis = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=[0, 0, 0])
    mat = o3d.visualization.rendering.Material()
    mat.shader = "defaultLit"
    widget3d.scene.add_geometry("Axis", axis, mat)

    mesh_sphere = o3d.geometry.TriangleMesh.create_sphere(radius=1)
    mesh_sphere.compute_vertex_normals()
    mesh_sphere.translate([5, 5, 5])
    mesh_sphere.paint_uniform_color([255/255, 255/255, 255/255])
    mat = o3d.visualization.rendering.Material()
    widget3d.add_3d_label([5, 5, 5], "1")
    mat.shader = "defaultLit"
    widget3d.scene.add_geometry("Sphere", mesh_sphere, mat)


    # # Add 3D labels
    # for i in range(0, len(torus.vertices)):
    #     widget3d.add_3d_label(torus.vertices[i], str(i))

    bounds = widget3d.scene.bounding_box
    widget3d.setup_camera(60, bounds, bounds.get_center())

    app.run()