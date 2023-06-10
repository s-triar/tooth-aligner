from utility.splineku import SplineKu
from utility.arch import Arch
from constant.enums import ArchType, ToothType, LandmarkType
import numpy as np
from vedo import (
    load, 
    Mesh, 
    Plotter,
    Line,
    Point,
    Points,
    Sphere
)
from utility.calculation import (
    find_new_point_in_a_line_with_new_distance,
    find_distance_between_two_points,
    find_distance_between_a_point_and_a_line,
    closest_line_seg_line_seg,
    find_closest_point_between_a_point_and_a_line,
    getToothLabelSeberang,
)
import pandas as pd

def load_ld(model, filename, typearch):
    df = pd.read_csv(filename, index_col=0)
    print(df.head())

    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        tooth = arch.teeth[row['label']]
        tooth.landmark_pt[row['landmark']] = np.array([row['x'], row['y'], row['z']])

# l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo LowerJawScan _d_predicted_refined.vtp')
# u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo UpperJawScan _d_predicted_refined.vtp')
u = load('D:\\tesis\\fix\\12. KEC\\KEC_UPPER.vtp')
path_ld_u = 'D:\\tesis\\fix\\12. KEC\\KEC_UPPER.csv'
model = Arch(ArchType.UPPER.value,u)
load_ld(model, path_ld_u, ArchType.UPPER.value)

centermeshPT=Point(u.centerOfMass(),c='black',r=20)

centermeshtoothcenterpt = []
for tp in ToothType:
    if(tp.value!=ToothType.GINGIVA.value and tp.value != ToothType.DELETED.value):
        a = model.teeth[tp.value].center
        centermeshtoothcenterpt.append(a)

centermeshtoothcenterpt = np.mean(centermeshtoothcenterpt,axis=0)
centermeshtoothcenterPT = Point(centermeshtoothcenterpt, c='grey',r=20)



# centermeshtoothBOUNDcenterpt =[]
# for tp in ToothType:
#     if(tp.value!=ToothType.GINGIVA.value and tp.value != ToothType.DELETED.value):
#         a = model.teeth[tp.value].center
#         centermeshtoothcenterpt.append(a)

mid_incisor_pt = np.mean([model.teeth[ToothType.INCISOR_UL1_LR1.value].center, model.teeth[ToothType.INCISOR_UR1_LL1.value].center], axis=0)
print(mid_incisor_pt)

icvpt = Point(mid_incisor_pt,c='orange',r=20)

mid_molar_pt = np.mean([model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center], axis=0)
mid_molar_PT = Point(mid_molar_pt,c='blue',r=20)
mpt = Points([model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center], c='yellow',r=20)
molar_ln = Line(mpt.points()[0], mpt.points()[1], c='yellow')
molar_perpendicular_pt = find_closest_point_between_a_point_and_a_line(mid_incisor_pt, mpt.points())
molar_perpendicular_PT = Point(molar_perpendicular_pt,c='yellow',r=20)

mid_incv_to_molar_LN = Line(mid_incisor_pt,molar_perpendicular_pt,c='orange')

used_center = u.centerOfMass()

meshpts_normalize = u.points() - used_center

molarL72x_pt = ((model.teeth[ToothType.MOLAR_UL7_LR7.value].center - used_center) * 2) + used_center
molarR72x_pt = ((model.teeth[ToothType.MOLAR_UR7_LL7.value].center - used_center) * 2) + used_center

molarL72x_pt = find_closest_point_between_a_point_and_a_line(molarL72x_pt,[model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center])
molarR72x_pt = find_closest_point_between_a_point_and_a_line(molarR72x_pt,[model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center])

molarL72x_PT = Point(molarL72x_pt, c='yellow',r=18)
molarR72x_PT = Point(molarR72x_pt, c='yellow',r=18)



def get_mesial_distal_as_R(arch):
    teeth = [
        ToothType.CANINE_UL3_LR3.value,
        ToothType.INCISOR_UL2_LR2.value,
        ToothType.INCISOR_UL1_LR1.value
    ]
    mesio_distal = 0 
    for t in teeth:
        t_inverse = getToothLabelSeberang(t)
        temp = find_distance_between_two_points(model.teeth[t].landmark_pt[LandmarkType.MESIAL.value], model.teeth[t].landmark_pt[LandmarkType.DISTAL.value])
        temp2 = find_distance_between_two_points(model.teeth[t_inverse].landmark_pt[LandmarkType.MESIAL.value], model.teeth[t_inverse].landmark_pt[LandmarkType.DISTAL.value])
        mesio_distal += np.mean([temp,temp2])
    return mesio_distal

R = get_mesial_distal_as_R(model)
print(R)

circle_pertama = Sphere(mid_incisor_pt, r=R)

plt = Plotter(axes=1)
plt.show(
    model.mesh,
    centermeshPT,
    centermeshtoothcenterPT,
    mpt,
    molar_ln,
    mid_molar_PT,
    icvpt,
    molar_perpendicular_PT,
    mid_incv_to_molar_LN,
    molarL72x_PT,
    molarR72x_PT,
    
    circle_pertama
    )