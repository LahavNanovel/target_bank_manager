import open3d as o3d
import open3d.visualization.gui as gui


if __name__ == "__main__":
    app = gui.Application.instance
    app.initialize()

    w = app.create_window("Open3D - 3D Labels", 1024, 768)
    widget3d = gui.SceneWidget()
    w.add_child(widget3d)
    widget3d.scene = o3d.visualization.rendering.Open3DScene(w.renderer)


    # Add torus
    torus = o3d.geometry.TriangleMesh.create_torus()
    torus.compute_vertex_normals()
    mat = o3d.visualization.rendering.Material()
    mat.shader = "defaultLit"
    widget3d.scene.add_geometry("Torus", torus, mat)

    # Add torus vertices
    pts = o3d.geometry.PointCloud(torus.vertices)
    mat = o3d.visualization.rendering.Material()
    mat.shader = "defaultUnlit"
    mat.point_size = 5 * w.scaling
    mat.base_color = (0, 0, 0, 1)
    widget3d.scene.add_geometry("Points", pts, mat)


    # Add 3D labels
    for i in range(0, len(torus.vertices)):
        widget3d.add_3d_label(torus.vertices[i], str(i))

    bounds = widget3d.scene.bounding_box
    widget3d.setup_camera(60, bounds, bounds.get_center())

    app.run()