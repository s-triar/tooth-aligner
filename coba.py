from vedo import *

def func(event):  # callback function
    p = event.picked3d
    if p is None:
        return
    pts = msh.closestPoint(p, N=1,returnPointId=True)
    print(pts)
    
    # N = msh.NCells()
    points = vtk2numpy(msh.polydata().GetPoints().GetData()) #vertices (coordinate)
    # ids = vtk2numpy(msh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] 
    # print(ids[pts])
    # j = Mesh([points,[ids[pts]]],c="red")
    # plt.add(j)
    pp = Point(points[pts])
    plt.add(pp)
    # sph = fitSphere(pts).alpha(0.1)
    # pts.name = "mypoints"   # we give it a name to make it easy to
    # sph.name = "mysphere"   # remove the old and add the new ones
    # txt.text(f'Radius : {sph.radius}\nResidue: {sph.residue}')
    # plt.remove("mypoints", "mysphere").add(pts, sph)

txt = Text2D(bg='yellow', font='Calco')

msh = Mesh(dataurl+'290.vtk').subdivide()
msh.addCurvatureScalars(method=2)
msh.cmap('PRGn', vmin=-0.02).addScalarBar()

plt = Plotter(axes=1)
plt.addCallback('mouse click', func)
plt.show(msh, txt, viewup='z')
plt.close()