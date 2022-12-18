from constant.enums import ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices
from vedo import Plotter, load, Mesh, Points, Point
import os
import numpy as np
from utility.colors import convert_labels_to_colors
from utility.neighboring_lib import get_bottom

path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\KEC LowerJawScan_d_predicted_refined.vtp')
mesh = load(path)

center_mesh = mesh.centerOfMass()
center_mesh_pt = Point(center_mesh, r=20, c="black")
points_mesh = np.array(mesh.points())
idx_faces_mesh = np.array(mesh.cells())
points_mesh_normalized = points_mesh-center_mesh

incisor_teeth = [
            ToothType.INCISOR_UL2_LR2.value, 
            ToothType.INCISOR_UL1_LR1.value,
            ToothType.INCISOR_UR1_LL1.value,
            ToothType.INCISOR_UR2_LL2.value
        ]

eig_val, eig_vec = getEigen(points_mesh_normalized, idx_faces_mesh, mesh.celldata['Label'], incisor_teeth)
eig_vec = np.array(eig_vec)*4
draweig = draw_eigen_vec(eig_vec, mesh.centerOfMass())
colors = convert_labels_to_colors(mesh.celldata['Label'])
mesh.celldata['Color'] = colors
mesh.celldata.select('Color')
msp, sp = get_bottom(points_mesh, idx_faces_mesh)
pts_boundary=[]
for s in sp:
    print(s)
    pts_boundary.append(Point(s, c="gray", r=15))
msp_bound = Point(msp, c="orange", r=20)
plt = Plotter(axes=1)
mesh = mesh.alpha(0.3)
plt.show(mesh,center_mesh_pt , pts_boundary, msp_bound)