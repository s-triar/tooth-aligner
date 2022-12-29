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
    find_new_point_in_a_line_with_new_distance,
    find_distance_between_a_point_and_a_line,
    find_distance_between_two_points,
    closest_line_seg_line_seg,
    find_closest_point_between_a_point_and_a_line,
    getToothLabelSeberang,
)
import math
import pandas as pd

def load_ld(model, filename, typearch):
    df = pd.read_csv(filename, index_col=0)
    print(df.head())
    
    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        tooth = arch.teeth[row['label']]
        tooth.landmark_pt[row['landmark']]=np.array([row['x'],row['y'],row['z']])
        
    
def get_mesial_distal_as_R(model):
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

def get_CD(sph_interect, ln_side):
    C_circle_pts = sph_interect.geodesic(ln_side[0], ln_side[1])
    c_val = 1000000000000
    candidate = []
    for p in C_circle_pts.points():
        dst = find_distance_between_a_point_and_a_line(p, ln_side)
        if(dst < c_val):
            c_val=dst
            candidate=p
    return candidate


l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj LowerJawScan _d_predicted_refined.vtp')
u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan _d_predicted_refined.vtp')
path_ld_u = 'D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\Gerry Sihaj\\step_0\\Gerry Sihaj_landmark_UPPER__step_0.csv'
path_ld_l = 'D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_landmark\\Gerry Sihaj\\step_0\\Gerry Sihaj_landmark_LOWER__step_0.csv'
model = Arch(ArchType.UPPER.value,u)
load_ld(model,path_ld_u,ArchType.UPPER.value)
model_lw = Arch(ArchType.LOWER.value,l)
load_ld(model_lw,path_ld_l,ArchType.LOWER.value)
R = get_mesial_distal_as_R(model)

centermeshPT=Point(u.centerOfMass(),c='black',r=20)

centermeshtoothcenterpt = []
for tp in ToothType:
    if(tp.value!=ToothType.GINGIVA.value and tp.value != ToothType.DELETED.value):
        a = model.teeth[tp.value].center
        centermeshtoothcenterpt.append(a)

centermeshtoothcenterpt = np.mean(centermeshtoothcenterpt,axis=0)
centermeshtoothcenterPT = Point(centermeshtoothcenterpt, c='grey',r=20)

# mid_incisor_pt
# TODO coba dengan titik terluar bukan center
A = np.mean([model.teeth[ToothType.INCISOR_UL1_LR1.value].center, model.teeth[ToothType.INCISOR_UR1_LL1.value].center], axis=0)
# A = np.mean([model.teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value], model.teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]], axis=0)

used_center = u.centerOfMass()

molarL72x_pt = ((model.teeth[ToothType.MOLAR_UL7_LR7.value].center - used_center) * 4) + used_center
molarR72x_pt = ((model.teeth[ToothType.MOLAR_UR7_LL7.value].center - used_center) * 4) + used_center

GG = find_closest_point_between_a_point_and_a_line(A, [model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center])
HH = find_closest_point_between_a_point_and_a_line(molarL72x_pt,[model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center])
II = find_closest_point_between_a_point_and_a_line(molarR72x_pt,[model.teeth[ToothType.MOLAR_UL7_LR7.value].center, model.teeth[ToothType.MOLAR_UR7_LL7.value].center])


AA = find_new_point_in_a_line_with_new_distance(GG,A,find_distance_between_two_points(GG,A)+100)

AA_A = find_distance_between_two_points(AA,A)
AA_GG = find_distance_between_two_points(AA,GG)
AA_II = find_distance_between_two_points(AA,II)
n_AA_AANN = (AA_A/AA_GG) * AA_II
AANN = find_new_point_in_a_line_with_new_distance(AA,II,n_AA_AANN)
AAMM = find_new_point_in_a_line_with_new_distance(AA,HH,n_AA_AANN)

B = find_new_point_in_a_line_with_new_distance(A,GG,R)

E = find_new_point_in_a_line_with_new_distance(A,B,2*R)

sphA = Sphere(A,r=R)
sphB = Sphere(B,r=R)
CD_circle = sphA.intersectWith(sphB)
C=get_CD(CD_circle,[AAMM,HH])
D=get_CD(CD_circle,[AANN,II])

F,f = closest_line_seg_line_seg([AAMM,AANN],[E,D])

G = find_new_point_in_a_line_with_new_distance(A,GG,find_distance_between_two_points(E,F))

AA_G =find_distance_between_two_points(AA,G)
n_AA_AAPP = (AA_G/AA_GG) * AA_II
AAOO = find_new_point_in_a_line_with_new_distance(AA,II,n_AA_AAPP)
AAPP = find_new_point_in_a_line_with_new_distance(AA,HH,n_AA_AAPP)
n_A_G = find_distance_between_two_points(A,G)


H = find_new_point_in_a_line_with_new_distance(G,AAOO,n_A_G)
I = find_new_point_in_a_line_with_new_distance(G,AAPP,n_A_G)

n_I_C = find_distance_between_two_points(I,D)
J = find_new_point_in_a_line_with_new_distance(I,H,n_I_C)
n_H_D = find_distance_between_two_points(H,C)
K = find_new_point_in_a_line_with_new_distance(H,I,n_H_D)

spl = SplineKu([J,D,A,C,K],degree=2,easing='Sine',smooth=0)

ctr,rad,norm = fitCircle([K,C])
ccr_CAD = KSpline([K,C,A,D,J],)
ccr_DJ = KSpline([A,D,J],continuity=0.1,tension=-1)
ccr_CK = KSpline([K,C,A],continuity=0.1,tension=-1)



ccr_CKs = []
batas_CK = find_distance_between_two_points(C,K)
for p in ccr_CK.points():
    if(batas_CK>find_distance_between_two_points(p,K)):
        ccr_CKs.append(p)

ccr_CADs = []
batas_AC = find_distance_between_two_points(A,C)
batas_AD = find_distance_between_two_points(A,D)
for p in ccr_CAD.points():
    temp = find_distance_between_two_points(p,A)
    if(temp < batas_AC and temp < batas_AD):
        ccr_CADs.append(p)

ccr_DJs = []
batas_DJ = find_distance_between_two_points(D,J)
for p in ccr_DJ.points():
    if(batas_DJ>find_distance_between_two_points(p,J)):
        ccr_DJs.append(p)

titiks = np.concatenate((ccr_CKs, ccr_CADs, ccr_DJs))

spr = Sphere(B,r=find_distance_between_two_points(B,A),res=24).c('blue3').alpha(0.1)
spr2 = Sphere(I,r=find_distance_between_two_points(I,J),res=24).c('grey').alpha(0.1)
spr3 = Sphere(H,r=find_distance_between_two_points(H,K),res=24).c('grey').alpha(0.1)

spl = SplineKu(titiks)
# tttt = spr.geodesic(K,C)


toCenterArch=[
    ToothType.CANINE_UR3_LL3.value,
    ToothType.INCISOR_UR2_LL2.value,
    ToothType.INCISOR_UR1_LL1.value,
    ToothType.INCISOR_UL1_LR1.value,
    ToothType.INCISOR_UL2_LR2.value,
    ToothType.CANINE_UL3_LR3.value
]
toCrossover = [
    ToothType.MOLAR_UR7_LL7.value,
    ToothType.MOLAR_UR6_LL6.value,
    ToothType.PREMOLAR_UR5_LL5.value,
    ToothType.PREMOLAR_UR4_LL4.value,
    ToothType.PREMOLAR_UL4_LR4.value,
    ToothType.PREMOLAR_UL5_LR5.value,
    ToothType.MOLAR_UL6_LR6.value,
    ToothType.MOLAR_UL7_LR7.value
]
llg = []
teeth = model.teeth
error_summary_i=0
error_summary=0
eigenvec = [model.right_left_vec, model.forward_backward_vec, model.upward_downward_vec]

for tooth_type in model.teeth:
    if tooth_type != ToothType.GINGIVA.value and tooth_type != ToothType.DELETED.value:
        if(tooth_type in toCenterArch):
            hitpspln, hitpln = spl.closestPointToAline([model.mesh.centerOfMass(), teeth[tooth_type].center], isAwal=(tooth_type>7))
            # hitpspln2 = spl.closestPoint(teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value])
            
        elif(tooth_type in toCrossover):
            labelSeberang = getToothLabelSeberang(tooth_type)
            hitpspln, hitpln = spl.closestPointToAline([teeth[tooth_type].center, teeth[labelSeberang].center], isAwal=(tooth_type>7))
            # hitpspln2 = spl.closestPoint(teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value])
        pt_in_line = hitpspln
        # print(tooth_type, pt_in_line, teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value])
        llg.append(Line(pt_in_line,teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value],lw=6,c='blue'))
        # llg.append(Line(hitpspln2,teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value],lw=6,c='green'))
        llg.append(Line(pt_in_line,teeth[tooth_type].center,lw=6,c='red'))
        a = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [pt_in_line])[0]
        # b = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]])[0]
        b = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [teeth[tooth_type].center])[0]
        dst = find_distance_between_two_points(a,b)
        error_summary+=(dst**2)
        # error_summary+= dst 
        
        error_summary_i+=1
        
teeth = model_lw.teeth

for tooth_type in model_lw.teeth:
    print(tooth_type,error_summary)
    if tooth_type != ToothType.GINGIVA.value and tooth_type != ToothType.DELETED.value:
        if(tooth_type in toCenterArch):
            labelSeberang = getToothLabelSeberang(tooth_type)
            pt_in_line = model.teeth[labelSeberang].landmark_pt[LandmarkType.LINGUAL_OR_PALATAL.value]
            llg.append(Line(pt_in_line,teeth[tooth_type].landmark_pt[LandmarkType.CUSP.value],lw=6,c='pink'))
            a = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [pt_in_line])[0]
            b = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [teeth[tooth_type].landmark_pt[LandmarkType.CUSP.value]])[0]
            dst = find_distance_between_two_points(a,b)
            error_summary+=(dst**2)
            # error_summary+= dst 
            
            error_summary_i+=1
            
        elif(tooth_type in toCrossover):
            labelSeberang = getToothLabelSeberang(tooth_type)
            pt_in_line = model.teeth[labelSeberang].landmark_pt[LandmarkType.PIT.value]
            
            bawah = teeth[tooth_type].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value]
            if(bawah is None):
                bawah = teeth[tooth_type].landmark_pt[LandmarkType.CUSP_OUT.value]
            if(bawah is None):
                bawah = np.mean([teeth[tooth_type].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],teeth[tooth_type].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value]],axis=0)
            llg.append(Line(pt_in_line,bawah,lw=6,c='pink'))
            a = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [pt_in_line])[0]
            b = convert_to_2d(FaceTypeConversion.UP.value, eigenvec, [bawah])[0]
            dst = find_distance_between_two_points(a,b)
            error_summary+=(dst**2)
            error_summary_i+=1
        
        
print( math.sqrt(error_summary/error_summary_i), '<===========')
        # llg.append(Line(pt_in_line,teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]))
        # llg.append(Line(pt_in_line,teeth[tooth_type].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]))

plt = Plotter(axes=1)
plt.show(
    u.alpha(0.4),
    l.alpha(0.4),
    Point(A,r=25),
    Point(AA),
    Point(B),
    Point(E),
    Points([AAMM,AANN]),
    Line(AAMM, AANN),
    # CD_circle,
    Points([C,D],r=20,c='red'),
    Point(F,c='blue'),
    Line(E,F),
    Point(G,c='grey'),
    Point(GG,c='black'),
    Points([AAOO,AAPP]),
    Line(AAOO,AAPP),
    Points([H,I],r=12),
    Points([J,K],r=15,c='blue'),
    # ccr_CAD.lw(5).c('green'),
    # ccr_DJ.lw(5).c('red'),
    # ccr_CK.lw(5).c('blue'),
    spr,
    spr2,
    spr3,
    spl.lw(10).c('yellow'),
    llg
    # Points(tttt.points(),r=15),
)

