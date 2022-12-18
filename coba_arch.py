from constant.enums import ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices
from vedo import Plotter, load, Mesh, Points
import os
import numpy as np


path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\MNF LowerJawScan_d_predicted_refined a.vtp')
path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\MNF LowerJawScan_d_predicted_refined.vtp')
mesh = load(path)
label = 9

incisor_teeth = [
            ToothType.INCISOR_UL2_LR2.value, 
            ToothType.INCISOR_UL1_LR1.value,
            ToothType.INCISOR_UR1_LL1.value,
            ToothType.INCISOR_UR2_LL2.value
        ]
N = mesh.NCells()
labels = np.unique(mesh.celldata['Label'])
# points = vtk2numpy(mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
# ids = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)

center_mesh = mesh.centerOfMass()
points_mesh = np.array(mesh.points())
idx_faces_mesh = np.array(mesh.cells())
points_mesh_normalized = points_mesh-center_mesh
# print(points_mesh[:10], points_mesh_normalized[:10])
# print(idx_faces_mesh)
eigen_val_mesh, eigen_vec_mesh = getEigen(points_mesh_normalized, idx_faces_mesh, mesh.celldata['Label'], incisor_teeth)
right_left_vec = eigen_vec_mesh[0]
forward_backward_vec = eigen_vec_mesh[1]
upward_downward_vec = eigen_vec_mesh[2]

cells_tooth_index = np.where(mesh.celldata['Label'] == label)

cells_tooth = idx_faces_mesh[cells_tooth_index]
points_tooth_index = np.unique(cells_tooth)
points_tooth = points_mesh[points_tooth_index]
points_tooth_normalized = points_mesh_normalized[points_tooth_index]
center_tooth = np.mean(points_tooth,axis=0)
center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)

point_tooth_index_map = map_point_index(points_tooth_index)
cells_tooth_mapped = mapping_point_index(point_tooth_index_map, cells_tooth)



tooth_mesh = Mesh([points_tooth, cells_tooth_mapped]) #.subdivide(1, method=0)
print(tooth_mesh.points())
non_mani = tooth_mesh.boundaries(boundaryEdges=False, nonManifoldEdges=True, returnCellIds=False)
pt_non=non_mani.points()

i_nons=[]
for p in pt_non:
    print(p)
    i_non = get_index_point_from_mesh_vertices(p,tooth_mesh.points())
    i_nons.append(i_non)
    
print(i_nons)
print(tooth_mesh.cells())

for i in i_nons:
    g = np.argwhere(tooth_mesh.cells()==i)
    print(g)

# non_mani_ids = tooth_mesh.boundaries(boundaryEdges=False, nonManifoldEdges=True, returnPointIds=True)
# pts = Points(tooth_mesh.points(non_mani_ids))
# eigen_val, eigen_vec = getEigen(arch.points(), arch.cells())
# print(eigen_val)
# print(eigen_vec)
# eigen_drawing = draw_eigen_vec(eigen_vec, arch.centerOfMass())

# temp = convert_to_2d(FaceTypeConversion.LEFT.value, eigen_vec,arch.points())
# print(temp)
# new_mesh = Mesh([temp, arch.cells()])
plt = Plotter(axes=1)
plt.show(tooth_mesh, non_mani)
