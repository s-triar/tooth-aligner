from constant.enums import ToothType
from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec, map_point_index, mapping_point_index, get_index_point_from_mesh_vertices
from vedo import Plotter, load, Mesh, Points, Point
import os
import numpy as np
from utility.colors import convert_labels_to_colors, map_landmark_color
from utility.app_tool import get_landmark

path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\ada non-manyfold\\UR UpperJawScan_d_predicted_refined.vtp')
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
eig_vec = np.array(eig_vec)
draweig = draw_eigen_vec(eig_vec, mesh.centerOfMass())
colors = convert_labels_to_colors(mesh.celldata['Label'])
mesh.celldata['Color'] = colors
mesh.celldata.select('Color')

artyp = 1 if "Upper" in path else 0

df_lm = get_landmark(artyp, "UR")
print(df_lm)
LDPOINTS = []
for index, row in df_lm.iterrows():
    x = row['x']
    y = row['y']
    z = row['z']
    lbl_ld = row['landmark']
    color = map_landmark_color(lbl_ld)
    pt = Point([x,y,z],r=20,c=color)
    if(lbl_ld!=3 and lbl_ld!=4):
        LDPOINTS.append(pt)

plt = Plotter(axes=1)
plt.show(mesh, draweig, LDPOINTS)