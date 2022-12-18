from constant.enums import ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices
from vedo import Plotter, load, Mesh, Points
import os
import numpy as np
from utility.colors import convert_labels_to_colors


path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\ada non-manyfold\\MNF LowerJawScan_d_predicted_refined.vtp')
mesh = load(path)

center_mesh = mesh.centerOfMass()
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
plt = Plotter(axes=1)
plt.show(mesh, draweig)