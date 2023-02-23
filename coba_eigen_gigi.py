from vedo import load, Mesh, Plotter
from utility.colors import convert_labels_to_colors
import utility.neighboring_lib as nl
import utility.landmarking_lib as ll
import numpy as np
import math

arch = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\KEC LowerJawScan_d_predicted_refined.vtp')

teeth_label = arch.celldata['Label']
colors = convert_labels_to_colors(arch.celldata['Label'])
arch.celldata['Color'] = colors
arch.celldata.select('Color')


center_mesh = arch.centerOfMass()
points_mesh = np.array(arch.points())
idx_faces_mesh = np.array(arch.cells())
points_mesh_normalized = points_mesh-center_mesh
# print(points_mesh[:10], points_mesh_normalized[:10])
# print(idx_faces_mesh)
eigen_val_mesh, eigen_vec_mesh = ll.getEigen(points_mesh_normalized, idx_faces_mesh)
right_left_vec = eigen_vec_mesh[0]
forward_backward_vec = eigen_vec_mesh[1]
upward_downward_vec = eigen_vec_mesh[2]


def map_point_index(unique_indexes):
    temp = {}
    for i in range(len(unique_indexes)):
        temp[unique_indexes[i]]=i
    return temp
    
def mapping_point_index(map, indexes):
    temp = []
    for i in range(len(indexes)):
        temp_j = []
        for j in range (len(indexes[i])):
            temp_j.append(map[indexes[i][j]])
        temp.append(temp_j)
    return temp
    
# get tooth point

label = 7

cells_tooth_index = np.where(teeth_label == label)
label = math.floor(label)
cells_tooth = idx_faces_mesh[cells_tooth_index]
points_tooth_index = np.unique(cells_tooth)
print(points_tooth_index)
point_tooth_index_map = map_point_index(points_tooth_index)
cells_tooth_mapped = mapping_point_index(point_tooth_index_map, cells_tooth)
points_tooth = points_mesh[points_tooth_index]
points_tooth_normalized = points_mesh_normalized[points_tooth_index]
center_tooth = np.mean(points_tooth,axis=0)

points_tooth = points_tooth - center_tooth

# center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)
# points_tooth_normalized= points_tooth_normalized-center_tooth_normalized
# center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)
# ============

# points_tooth = np.transpose(points_tooth)
# points_tooth = np.matmul(eigen_vec_mesh,points_tooth)
# points_tooth = np.transpose(points_tooth)

# ============


tooth_mesh = Mesh([points_tooth, cells_tooth_mapped])

tooth_mesh = tooth_mesh.subdivide(1, method=0)
print(len(tooth_mesh.cells()))

eigen_val_tooth, eigen_vec_tooth = ll.getEigenPlain(points_tooth)

eig_draw = ll.draw_eigen_vec(eigen_vec_tooth, center_tooth)

plt = Plotter(axes=1)
plt.show(
    arch, 
    tooth_mesh,
    eig_draw
    )


