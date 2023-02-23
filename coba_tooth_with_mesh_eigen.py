from constant.enums import ArchType, ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices, get_mesial_distal_anterior, get_pit
from vedo import Plotter, load, Mesh, Point
import os
import numpy as np
from utility.arch import Arch


path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\KEC LowerJawScan_d_predicted_refined.vtp')
mesh = load(path)
model = Arch(ArchType.LOWER.value,mesh)
mesh_eig = [ model.right_left_vec,
        model.forward_backward_vec,
        model.upward_downward_vec]

mesh_eig_inv = mesh_eig*-1

label = 7

teeth = model.teeth
tooth = teeth[label].get_mesh()
tooth_center = Point(tooth.centerOfMass(),r=20)
tooth_eig_draw = draw_eigen_vec(mesh_eig,tooth.centerOfMass())

tooth_norm = tooth.clone().points(tooth.points()-tooth.centerOfMass())
tooth_center_norm =Point(tooth_norm.centerOfMass(),r=20)
tooth_norm_eig_draw = draw_eigen_vec(mesh_eig,tooth_norm.centerOfMass())

plt = Plotter(N=2, axes=1)
plt.show(tooth.alpha(0.6),tooth_center,tooth_eig_draw, at=0)
# plt.show(tooth_norm.alpha(0.6),tooth_center_norm,tooth_norm_eig_draw, at=1)
plt.interactive()