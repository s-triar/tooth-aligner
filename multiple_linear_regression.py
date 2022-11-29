from constant.enums import ArchType, ToothType
from utility.app_tool import load_all_landmarks
import numpy as np
from sklearn import linear_model
import random

from vedo import load, Mesh, Plotter, Point
from utility import landmarking_lib as ll

label = 10
df = load_all_landmarks(ArchType.UPPER.value, label, 2)
print(df.head())

x=[]
y=[]
for i in range(len(df)):
    print(df.iloc[i])
    row = df.iloc[i]
    x_coor = [row['x'], row['y'], row['z']]
    x_eigen = [
                [
                    row['right_left_vec_x'],
                    row['right_left_vec_y'],
                    row['right_left_vec_z'],
                ],
                [
                    row['forward_backward_vec_x'],
                    row['forward_backward_vec_y'],
                    row['forward_backward_vec_z'],
                ],
                [
                    row['upward_downward_vec_x'],
                    row['upward_downward_vec_y'],
                    row['upward_downward_vec_z'],
                ],
            ]
    print(x_eigen)
    lr = np.array(x_eigen[0])
    fb = np.array(x_eigen[1])
    ud = np.array(x_eigen[2])
    
    lr_inv = np.array(x_eigen[0]) * -1
    fb_inv = np.array(x_eigen[1]) * -1
    ud_inv = np.array(x_eigen[2]) * -1
    
    
    dot_lr = np.dot(x_coor, lr)
    dot_fb = np.dot(x_coor, fb)
    dot_ud = np.dot(x_coor, ud)
    
    dot_lr_inv = np.dot(x_coor, lr_inv)
    dot_fb_inv = np.dot(x_coor, fb_inv)
    dot_ud_inv = np.dot(x_coor, ud_inv)
    x.append([dot_lr, dot_fb, dot_ud])
    
print(x)
x_mean = np.mean(x, axis=0)
x_std = np.std(x, axis=0)


print(x_mean)

for xi in x:
    y_col = [  (xi[0]-x_mean[0])/x_std[0], (xi[1]-x_mean[1])/x_std[1],( xi[2]-x_mean[2])/x_std[2] ]
    y.append(np.mean(y_col))
print(y)

for ty in range(len(y)):
    y[ty] = 1-y[ty]

    
regr = linear_model.LinearRegression()
regr.fit(x, y)


print(regr.coef_)
COEF = regr.coef_
pred = regr.predict(x)
print(pred)


incisor_teeth = [
            ToothType.INCISOR_UL2_LR2.value, 
            ToothType.INCISOR_UL1_LR1.value,
            ToothType.INCISOR_UR1_LL1.value,
            ToothType.INCISOR_UR2_LL2.value
        ]
mesh = load('D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\KEC\\step_0\\KEC_UPPER__step_0.vtp')

center_mesh = mesh.centerOfMass()
points_mesh = np.array(mesh.points())
idx_faces_mesh = np.array(mesh.cells())
points_mesh_normalized = points_mesh-center_mesh
# print(points_mesh[:10], points_mesh_normalized[:10])
# print(idx_faces_mesh)
eigen_val_mesh, eigen_vec_mesh = ll.getEigen(points_mesh_normalized, idx_faces_mesh, mesh.celldata['Label'], incisor_teeth)
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

point_tooth_index_map = ll.map_point_index(points_tooth_index)
cells_tooth_mapped = ll.mapping_point_index(point_tooth_index_map, cells_tooth)
tooth_mesh = Mesh([points_tooth, cells_tooth_mapped]).subdivide(1, method=0)
points_tooth_normalized = tooth_mesh.points()-center_mesh
center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)

y_pred = []
for x_coor in points_tooth_normalized:
    # dot_lr = np.dot(x_coor, eigen_vec_mesh[0])
    # dot_fb = np.dot(x_coor, -1*eigen_vec_mesh[1])
    # dot_ud = np.dot(x_coor, eigen_vec_mesh[2])
    
    lr = np.array(eigen_vec_mesh[0])
    fb = np.array(eigen_vec_mesh[1])
    ud = np.array(eigen_vec_mesh[2])
    
    lr_inv = np.array(eigen_vec_mesh[0]) * -1
    fb_inv = np.array(eigen_vec_mesh[1]) * -1
    ud_inv = np.array(eigen_vec_mesh[2]) * -1
    
    
    dot_lr = np.dot(x_coor, lr)
    dot_fb = np.dot(x_coor, fb)
    dot_ud = np.dot(x_coor, ud)
    
    dot_lr_inv = np.dot(x_coor, lr_inv)
    dot_fb_inv = np.dot(x_coor, fb_inv)
    dot_ud_inv = np.dot(x_coor, ud_inv)
    
    y_pred.append(regr.predict([[dot_lr, dot_fb, dot_ud]])[-1])
print(y_pred)

index_y_pred_sorted = np.argsort(y_pred)
print(index_y_pred_sorted)
pts = tooth_mesh.points()[index_y_pred_sorted[-1]]
point = Point(pts)
plt= Plotter()
draw_ei = ll.draw_eigen_vec(eigen_vec_mesh, mesh.centerOfMass())

plt.show(mesh,tooth_mesh, point,draw_ei)