from vedo import Mesh, Plotter, Sphere


a = Sphere((0,2,3),r=4).triangulate()
# b = Sphere((0,4,3),r=3,c="k4")

a.computeNormals(points=False,cells=True).print()
print(a.celldata["Normals"], len(a.celldata["Normals"]))

plt = Plotter(axes=7)
plt.show(a)

