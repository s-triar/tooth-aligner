from vedo import *
from utility.landmarking_lib import getEigen, draw_eigen_vec, getEigenAttachment
import numpy as np
# def func(event):  # callback function
#     p = event.picked3d
#     if p is None:
#         return
#     pts = msh.closestPoint(p, N=1,returnPointId=True)
#     print(pts)
    
#     # N = msh.NCells()
#     points = vtk2numpy(msh.polydata().GetPoints().GetData()) #vertices (coordinate)
#     # ids = vtk2numpy(msh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] 
#     # print(ids[pts])
#     # j = Mesh([points,[ids[pts]]],c="red")
#     # plt.add(j)
#     pp = Point(points[pts])
#     plt.add(pp)
#     # sph = fitSphere(pts).alpha(0.1)
#     # pts.name = "mypoints"   # we give it a name to make it easy to
#     # sph.name = "mysphere"   # remove the old and add the new ones
#     # txt.text(f'Radius : {sph.radius}\nResidue: {sph.residue}')
#     # plt.remove("mypoints", "mysphere").add(pts, sph)

# txt = Text2D(bg='yellow', font='Calco')

# msh = Mesh(dataurl+'290.vtk').subdivide()
# msh.addCurvatureScalars(method=2)
# msh.cmap('PRGn', vmin=-0.02).addScalarBar()

# plt = Plotter(axes=1)
# plt.addCallback('mouse click', func)
# plt.show(msh, txt, viewup='z')
# plt.close()

state={
    'eigen_index':[],
    'face_index':-1
}

def on_choose_new_space(face_id):
    ps = b.points()[ids[face_id]]
    c = np.mean(ps,axis=0)
    cb = b.centerOfMass()
    chosen_eig = -1
    temp=99999999
    for i in range(len(eig_vec)):
        t = cb-eig_vec[i]
        tot = np.dot( np.transpose(c),t)
        if(tot<temp):
            chosen_eig=i
            temp=tot
        t = cb+eig_vec[i]
        tot = np.dot( np.transpose(c),t)
        if(tot<temp):
            chosen_eig=i
            temp=tot
    return chosen_eig

def on_choose_face(event):
    state={
        'eigen_index':[],
        'face_index':-1
    }
    print(event)
    if(event.actor):
        p = event.picked3d
        face_id = b.closestPoint(p, N=1,returnCellId=True)
        eigen_vec_id = on_choose_new_space(face_id)
        print('eigen_vec_id',eigen_vec_id)
        state={
            'eigen_index':np.delete(eig_vec,eigen_vec_id,0),
            'face_index':face_id
        }
    print(eig_vec)
    print(state)


def on_move_object(dir):
    if(len(state['eigen_index'])==2):
        ab = state['eigen_index'][0]
        kk = state['eigen_index'][1]


        

def on_key_released(event):
    cur = plt.interactor.GetInteractorStyle()
    # print(cur)
    # if isinstance(cur, vtk.vtkInteractorStyleTrackballCamera):
    if event.actor==b and isinstance(cur, vtk.vtkInteractorStyleTrackballActor):
        vsty = vtk.vtkInteractorStyleTrackballCamera()
        plt.interactor.SetInteractorStyle(vsty)
        print('aaaaaaaaa')
        return

global tto
tto = 0

b = Box((0,0,0),length=2,width=4,height=2).alpha(0.4)
points = b.points()
points_nor = []
center= b.centerOfMass()
for i in range(len(points)):
    points_nor.append(points[i]-center)
b.points(points_nor)
N = b.NCells()
pts = vtk2numpy(b.polydata().GetPoints().GetData()) #vertices (coordinate)
ids = vtk2numpy(b.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
b = b.tomesh()#Mesh([pts,ids])
print(ids)
print(N)


eig_val, eig_vec = getEigenAttachment(pts)
eig_obj = draw_eigen_vec(eig_vec,b.centerOfMass())
pts_obj=[]

for pt in pts:
    pts_obj.append(Point(pt))
plt = Plotter(axes=1)
plt.addCallback('mouse click', on_choose_face)
# plt.removeCallback('KeyPress')
plt.addCallback('LeftButtonPressEvent', on_key_released)
plt.show(b,Cube((0.3,0.2,0.6),2),viewup='z', mode=tto)
plt.close()