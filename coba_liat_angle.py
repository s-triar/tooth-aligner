from utility.arch_copy import ArchCopy
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
    Sphere,
    Circle,fitCircle,
    Arc,
    KSpline,
    CSpline,
    
)
from utility.calculation import (
    FaceTypeConversion,
    convert_to_2d,
    find_closest_point_between_a_point_and_a_3pts_plane,
    find_new_point_in_a_line_with_new_distance,
    find_distance_between_a_point_and_a_line,
    find_distance_between_two_points,
    closest_line_seg_line_seg,
    find_closest_point_between_a_point_and_a_line,
    getToothLabelSeberang,
)
import math
import pandas as pd
import copy
from controller.summary_controller import (
    get_bonwill,
    get_destination_points,
)
from utility.tooth_label import get_tooth_labels
from optimization.optimization_helper5 import calculate_buccallabial_to_bonwill_line, calculate_cusp_to_flat_level_line, calculate_mesiodistal_balance_to_bonwill_line_from_side_view, calculate_mesiodistal_balance_to_bonwill_line_from_top_view, get_closest_possible_movements, get_closest_possible_rotations, get_closest_possible_rotations_and_movements


def get_flats(model):
    mesh = model.mesh
    teeth = model.teeth
    pts = np.array([
        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
        np.mean([
            teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
            teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
        ], axis=0),
        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
    ])
    pts_cusps=np.array([
        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
        teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
        teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
        teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
        teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
        
        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
        teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
        teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
        teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
        teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
    ])
    new_coords = []
    for pt in pts_cusps:
        # new_coord = abs(np.dot(pt - pts[1],n))
        new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
        new_coords.append(new_coord)
    return new_coords

def load_ld(model, filename, typearch):
    df = pd.read_csv(filename, index_col=0)
    
    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        tooth = arch.teeth[int(row['label'])]
        tooth.landmark_pt[int(row['landmark'])]=np.array([row['x'],row['y'],row['z']])

ori = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan _d_predicted_refined.vtp')
path_ld_ori = 'D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\Gerry Sihaj\\step_0\\Gerry Sihaj_landmark_UPPER__step_0.csv'

n_step = load('D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\saved_custom_crossover\\Gerry Sihaj\\step_15\\Gerry Sihaj_UPPER__step_15.vtp')
path_ld_step = 'D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\saved_custom_crossover\\Gerry Sihaj\\step_15\\Gerry Sihaj_landmark_UPPER__step_15.csv'


model = Arch(ArchType.UPPER.value,ori, test=True)

load_ld(model,path_ld_ori,ArchType.UPPER.value)

model_step = Arch(ArchType.UPPER.value,n_step, test=True)
load_ld(model_step,path_ld_step,ArchType.UPPER.value)
eigenvec = [model.right_left_vec, model.forward_backward_vec, model.upward_downward_vec]

summary_line, line_center, B, A = get_bonwill(ori, model)

spl = SplineKu(summary_line)
tooth_labels = get_tooth_labels()
destinations_pts = get_destination_points(model,spl, A, model.right_left_vec)
flats = get_flats(model)



lbl_target=10
pts_ori=[]
pts_step=[]
teeth_ori = model.teeth
teeth_step = model_step.teeth
for lbl in destinations_pts:
    if lbl == lbl_target:
        temp=destinations_pts[lbl]
        tooth_ori = teeth_ori[lbl]
        tooth_step= teeth_step[lbl]
        pts_ori.append(Point(temp[0],c='red4',r=20))
        pts_ori.append(Point(temp[1],c='blue4',r=20))
        pts_ori.append(Point(tooth_ori.landmark_pt[LandmarkType.MESIAL.value], c='red',r=15))
        pts_ori.append(Point(tooth_ori.landmark_pt[LandmarkType.DISTAL.value], c='blue',r=15))
        pts_step.append(Point(temp[1],c='blue4',r=20))
        pts_step.append(Point(temp[0],c='red4',r=20))
        pts_step.append(Point(tooth_step.landmark_pt[LandmarkType.MESIAL.value], c='red',r=15))
        pts_step.append(Point(tooth_step.landmark_pt[LandmarkType.DISTAL.value], c='blue',r=15))
        
        calculate_mesiodistal_balance_to_bonwill_line_from_top_view(tooth_ori,B, line_center, spl, eigenvec, True, True, A, destinations_pts, for_cr=False)
        calculate_mesiodistal_balance_to_bonwill_line_from_top_view(tooth_step,B, line_center, spl, eigenvec, True, True, A, destinations_pts, for_cr=False)

        calculate_mesiodistal_balance_to_bonwill_line_from_side_view(tooth_ori, spl, eigenvec, True, True, A, destinations_pts, for_cr=False)
        calculate_mesiodistal_balance_to_bonwill_line_from_side_view(tooth_step, spl, eigenvec, True, True, A, destinations_pts, for_cr=False)

line1 = [
    [10.67364701, -9.11792534],
    [10.41279467, -8.90876097]
]

line2 = [
    [10.67364701, -9.11792534],
    [6.71067934, -8.13429176]
]

ln1 = Line(line1[0],line1[1],lw=4,c='green')
ln2 = Line(line2[0],line2[1],lw=4,c='violet')

linee1 = [
    [10.67364701, -9.11792534],
    [10.68048122, -8.54920956]
]

linee2 = [
   [10.67364701, -9.11792534],
    [6.71067934, -8.13429176 ]
    
]

lne1 = Line(linee1[0],linee1[1],lw=4,c='red')
lne2 = Line(linee2[0],linee2[1],lw=4,c='violet')

plt = Plotter(N=3)
plt.show(model.mesh.alpha(0.5), pts_ori,spl, at=0)
plt.show(model_step.mesh.alpha(0.5), pts_step,spl, at=1)
plt.show(ln1,ln2,lne1,lne2, at=2)
plt.interactive()
