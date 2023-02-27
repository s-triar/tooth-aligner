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
    print(df.head())
    
    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        print(row)
        tooth = arch.teeth[int(row['label'])]
        tooth.landmark_pt[int(row['landmark'])]=np.array([row['x'],row['y'],row['z']])

# l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UPPERJawScan _d_predicted_refined.vtp')
u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan _d_predicted_refined.vtp')
path_ld_u = 'D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\Gerry Sihaj\\step_0\\Gerry Sihaj_landmark_UPPER__step_0.csv'
# path_ld_l = 'D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\Gerry Sihaj\\step_0\\Gerry Sihaj_landmark_LOWER__step_0.csv'

model = Arch(ArchType.UPPER.value,u)
eigenvec = [model.right_left_vec, model.forward_backward_vec, model.upward_downward_vec]
model2 = ArchCopy(model.arch_type, model.mesh.clone(), eigenvec, copy.deepcopy(model.teeth), copy.deepcopy(model.gingiva))
load_ld(model,path_ld_u,ArchType.UPPER.value)
lds=[]
for l in model.teeth:
    tooth = model.teeth[l]
    c='grey'
    if(l>7):
        c='black'
    for ld in tooth.landmark_pt:
        pt = tooth.landmark_pt[ld]
        if (not pt is None) and len(pt)>2:
            pp = Point(pt,c=c)
            lds.append(pp)
# model_lw = Arch(ArchType.LOWER.value,l)
# load_ld(model_lw,path_ld_l,ArchType.LOWER.value)
summary_line, line_center, B, A = get_bonwill(u, model)
spl = SplineKu(summary_line)
tooth_labels = get_tooth_labels()
dst_points_u = get_destination_points(model,spl, A, model.right_left_vec)
flats = get_flats(model)
mesial_dst =[]
distal_dst=[]
mid_dst=[]
print()
for k in dst_points_u:
    print(k, dst_points_u[k])
    mesial_dst.append(dst_points_u[k][0])
    distal_dst.append(dst_points_u[k][1])
    mid_dst.append(dst_points_u[k][2])


destinations_line = []
error_mesial_lines=[]
error_distal_lines=[]

i=0
for lbl in dst_points_u:
    temp=dst_points_u[lbl]
    print(temp)
    c="red"
    if(i%3==1):
        c="blue"
    elif(i%3==2):
        c="green"
    tooth = model.teeth[lbl]
    m = tooth.landmark_pt[LandmarkType.MESIAL.value]
    d = tooth.landmark_pt[LandmarkType.DISTAL.value]
    l = Line(temp[0],temp[1],lw=11,c=c)
    destinations_line.append(l)
    m_line = Line(temp[0],m,lw=13,c=c+'3')
    d_line = Line(temp[1],d,lw=13,c=c+'3')
    error_mesial_lines.append(m_line)
    error_distal_lines.append(d_line)
    # pm.append(Point(temp[0],r=20))
    # pd.append(Point(temp[1],r=20))
    i+=1


bonwill_points_obj = Points(summary_line)
mesial_dst_obj=Points(mesial_dst, c='red',r=20)
distal_dst_obj=Points(distal_dst, c='blue',r=20)
mid_dst_obj=Points(mid_dst, c='grey',r=20)




chr = [
 -2.18750000e-02, -2.18750000e-02,  9.05738127e-02,  4.93106663e-01,
 -7.75768579e-02,  3.08952952e-01,  2.61298941e-01,  4.72723783e-01,
  6.27183453e-02, -5.22531098e-02, -2.52695646e-01, -2.04642257e-01,
 -4.81662949e-01,  5.00000000e-01, -5.00000000e-01, -4.25000000e-01,
  5.00000000e-01, -4.25000000e-01, -4.74559236e-01,  2.71778616e-02,
 -4.03842332e-01, -2.88519534e-01, -3.54946022e-01,  1.99871819e-01,
 -2.50906570e-01, -1.89604328e-01,  6.23298728e-02,  0.00000000e+00,
  0.00000000e+00,  0.00000000e+00,  5.00000000e-01,  5.00000000e-01,
 -5.00000000e-01, -3.11492797e-03,  4.07743206e-03, -1.78356211e-03,
 -3.72763485e-01, -1.23998630e-01,  2.98870803e-01, -2.32047009e-02,
 -1.11468006e-01,  4.72555718e-02, -1.20515375e-02, -3.50827424e-01,
  2.69225239e-02, -5.00000000e-01,  2.28069053e-01,  2.67875210e-01,
 -1.97643478e-01,  2.62974378e-01,  8.09600080e-02, -5.00000000e-01,
  5.56464938e-02,  3.18199214e-01,  1.39812844e-01,  4.93460853e-01,
  5.24373127e-02, -4.80468750e-01,  4.98110082e-02,  6.86123589e-02,
 -4.89641570e-01, -7.15755697e-03,  1.90853273e-01, -4.91149762e-01,
 -3.47203329e-01,  4.22567111e-01,  3.20848277e-03,  3.41045977e-01,
 -1.27834607e-01, -5.00000000e-01,  4.33690014e-01,  4.94741127e-01,
  2.97511121e-01, -4.70880712e-01,  1.26794842e-01, -5.00000000e-01,
  5.00000000e-01,  3.53006320e-01, -1.70729142e-01, -2.43924377e-01,
  2.06884814e-01, -4.93750000e-01,  1.87354968e-01,  4.22048155e-01,
 -5.00000000e-01, -4.47880530e-02,  3.40243697e-01, -5.00000000e-01]
from optimization.de_optimization5 import de_rotation_and_moving
model = de_rotation_and_moving(model, chr)

teeth = model.teeth
tot_error_top_view=0
tot_error_side_view=0
tot_error_top_view_move=0
tot_error_side_view_move=0
error_summary=0
error_summary_i=0
punish_collision = 0
flat_line=SplineKu(flats)
for tooth_type in teeth:
    if tooth_type != ToothType.GINGIVA.value and tooth_type != ToothType.DELETED.value:
        
        error_top_view = calculate_mesiodistal_balance_to_bonwill_line_from_top_view(teeth[tooth_type], B,line_center,summary_line,eigenvec, False, True,  A, dst_points_u) 
        error_side_view = calculate_mesiodistal_balance_to_bonwill_line_from_side_view(teeth[tooth_type], summary_line, eigenvec, False, True,  A, dst_points_u)
        
        error_top_view_move = calculate_buccallabial_to_bonwill_line(teeth[tooth_type], summary_line,eigenvec, False,  A, dst_points_u)
        error_side_view_move = calculate_cusp_to_flat_level_line(teeth[tooth_type], flat_line,eigenvec, False)
        
        tot_error_top_view+=error_top_view**2
        tot_error_side_view+=error_side_view**2
        
        tot_error_top_view_move+=error_top_view_move**2
        tot_error_side_view_move+=error_side_view_move**2
        
        # error_total = error_top_view+error_side_view+error_top_view_move+error_side_view_move
        
        # error_summary+=(error_total**2)
        error_summary_i+=1

tot_error_top_view=math.sqrt(tot_error_top_view/error_summary_i)
tot_error_side_view=math.sqrt(tot_error_side_view/error_summary_i)

tot_error_top_view_move=math.sqrt(tot_error_top_view_move/error_summary_i)
tot_error_side_view_move=math.sqrt(tot_error_side_view_move/error_summary_i)
# error_summary = math.sqrt(error_summary/error_summary_i)
error_summary = tot_error_top_view+tot_error_side_view+tot_error_top_view_move+tot_error_side_view_move
totalerror = error_summary+punish_collision
print("total error:", totalerror)



plt = Plotter(N=3)
plt.show(model.mesh.alpha(0.5),bonwill_points_obj, mesial_dst_obj, distal_dst_obj, destinations_line, at=0)
plt.show(model.mesh.alpha(0.5),bonwill_points_obj, mesial_dst_obj, distal_dst_obj, destinations_line, error_distal_lines, error_mesial_lines, at=1)
plt.show(model2.mesh.alpha(0.5),bonwill_points_obj, mesial_dst_obj, distal_dst_obj, destinations_line, error_distal_lines, error_mesial_lines, at=2)
plt.interactive()



