from constant.enums import ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices, get_mesial_distal_anterior, get_pit
from vedo import Plotter, load, Mesh, Point
import os
import numpy as np


path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\KEC LowerJawScan_d_predicted_refined.vtp')
mesh = load(path)
label = 13

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
# center_tooth = np.mean(points_tooth,axis=0)
# center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)

point_tooth_index_map = map_point_index(points_tooth_index)
cells_tooth_mapped = mapping_point_index(point_tooth_index_map, cells_tooth)


tooth_mesh = Mesh([points_tooth, cells_tooth_mapped]).lc("black").lw(0.5)
tooth_mesh_subdivided = Mesh([points_tooth, cells_tooth_mapped]).subdivide(1, method=0).lc("black").lw(0.5)


points_tooth_normalized = tooth_mesh_subdivided.points()-center_mesh
center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)

# mesial, distal = get_mesial_distal_anterior(False, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
# mesial_index = get_index_point_from_mesh_vertices(mesial, points_tooth_normalized)
# print(mesial[0],mesial[1],mesial[2])
# pt_mesial = Point(tooth_mesh_subdivided.points()[mesial_index],r=30)
# pt_distal = Points(distal)

pit, ponten_pits = get_pit(eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)

pt_pits = []
for p in ponten_pits:
    pt_pits.append(Point(tooth_mesh_subdivided.points()[p],r=15, c="gray"))
pit_index = get_index_point_from_mesh_vertices(pit, points_tooth_normalized)
pt_pit = Point(tooth_mesh_subdivided.points()[pit_index],r=22, c="black")

plt = Plotter(axes=1,N=4)
plt.show(tooth_mesh, at=0)
plt.show(tooth_mesh_subdivided,  at=1)
plt.show(tooth_mesh_subdivided,pt_pits,  at=2)
plt.show(tooth_mesh_subdivided,pt_pit,  at=3)

plt.interactive()
