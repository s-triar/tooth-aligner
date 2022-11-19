from utility.calculation import convert_to_2d, FaceTypeConversion
from utility.landmarking_lib import getEigen, draw_eigen_vec
from vedo import Plotter, load, Mesh
import os


path = os.path.join('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan Cleaned 10000_d_predicted_refined a.vtp')
arch = load(path)
eigen_val, eigen_vec = getEigen(arch.points(), arch.cells())
print(eigen_val)
print(eigen_vec)
eigen_drawing = draw_eigen_vec(eigen_vec, arch.centerOfMass())

temp = convert_to_2d(FaceTypeConversion.LEFT.value, eigen_vec,arch.points())
print(temp)
new_mesh = Mesh([temp, arch.cells()])
plt = Plotter(axes=1)
plt.show(arch,eigen_drawing,new_mesh)
