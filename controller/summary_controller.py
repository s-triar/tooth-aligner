import numpy as np
from sklearn.cluster import KMeans
from vedo import Point, Sphere, CSpline, KSpline
from constant.enums import ArchType, LandmarkType, ToothType
from utility.arch import Arch
from utility.calculation import (
    find_closest_point_between_a_point_and_a_3pts_plane, 
    find_closest_point_between_a_point_and_a_line, 
    find_new_point_in_a_line_with_delta_distance, 
    find_new_point_in_a_line_with_new_distance,
    find_distance_between_a_point_and_a_line,
    find_distance_between_two_points,
    closest_line_seg_line_seg,
    getToothLabelSeberang,
    )
from utility.splineku import SplineKu
# from controller.step_controller import add_transform_arch


def init_summary(self):
    self.summary_flat_pts = None
    self.studi_model_summary_pts=None
    self.line_center_pts=None
    self.Bs_pts=None
    self.As_pts=None
    self.destination_tooth=None

def calculate_studi_model(self):
    if(Arch._is_complete()):
        # for m in self.models:
        #     m.extract_tooth()
        self.bolton_studi_model.calc_anterior_overall(self.models)
        print("calculating bolton study model is done")
        # print("get_anterior_overall",self.bolton_studi_model.get_anterior_overall())
        # print("overjet",self.bolton_studi_model.get_overjet())
        self.korkhaus_studi_model.calculate_khorkaus(self.models)
        print("calculating korkhaus study model is done")
        self.pont_studi_model.calculate_pont(self.models)
        print("calculating pont study model is done")
        self.carey_studi_model.calculate_carey(self.models)
        print("calculating carey study model is done")
        self.summary_flat_pts = calculate_flat_plane_points(self)
        print("calculating flat is done")
        # self.studi_model_summary_pts=calculate_studi_model_summary_pts(self)
        self.studi_model_summary_pts, self.line_center_pts, self.Bs_pts, self.As_pts = calculate_bonwill(self)
        print("calculating bonwill is done")
        self.destination_tooth = calculate_destination_points(self)
        print("calculating bonwill destination is done")
        # print("self.studi_model_summary_pts")
        # print(self.studi_model_summary_pts)
        # print()

def get_As_pts(self):
    return self.As_pts 

def get_Bs_pts(self):
    return self.Bs_pts    

def get_line_centers_pts(self):
    return self.line_center_pts        
        
def get_studi_model_summary_pts(self):
    return self.studi_model_summary_pts

def get_destination_tooth(self):
    return self.destination_tooth


def get_summary_flat_pts(self):
    return self.summary_flat_pts

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
        # mesio_distal += np.mean([temp,temp2])
        mesio_distal += np.mean([temp,temp2]) + (0 if t == teeth[-1] else 1.5)
        
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

def get_bonwill(u, model):
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
    # A = np.mean([model.teeth[ToothType.INCISOR_UL1_LR1.value].center, model.teeth[ToothType.INCISOR_UR1_LL1.value].center], axis=0)
    A = np.mean([model.teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value], model.teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]], axis=0)

    used_center = u.centerOfMass()

    molarrl7pt_ctr = model.teeth[ToothType.MOLAR_UL7_LR7.value].center
    molarrr7pt_ctr = model.teeth[ToothType.MOLAR_UR7_LL7.value].center

    molarL72x_pt = ((model.teeth[ToothType.MOLAR_UL7_LR7.value].center - used_center) * 4) + used_center
    molarR72x_pt = ((model.teeth[ToothType.MOLAR_UR7_LL7.value].center - used_center) * 4) + used_center

    molarrl7pt = molarL72x_pt[:]
    molarrr7pt = molarR72x_pt[:]


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

    # spl = SplineKu([J,D,A,C,K],degree=2,easing='Sine',smooth=0)

    # ctr,rad,norm = fitCircle([K,C])
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

    # spr0 =Sphere(A,r=find_distance_between_two_points(B,A),res=24).c('green3').alpha(0.1) 
    # spr = Sphere(B,r=find_distance_between_two_points(B,A),res=24).c('blue3').alpha(0.1)
    # spr2 = Sphere(I,r=find_distance_between_two_points(I,J),res=24).c('grey').alpha(0.1)
    # spr3 = Sphere(H,r=find_distance_between_two_points(H,K),res=24).c('grey').alpha(0.1)

    # spl = SplineKu(titiks)
    
    return titiks, [AA,GG], B, A


def calculate_bonwill(self):
    archwire = {}
    center_line= {}
    Bs={}
    As={}
    if Arch._is_complete():
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            titiks, line_center, B, A = get_bonwill(mesh, self.models[idx])
            archwire[i.value] = titiks
            center_line[i.value] = line_center
            Bs[i.value] = B
            As[i.value] = A
    return archwire, center_line, Bs, As

def calculate_flat_plane_points(self):
    if Arch._is_complete():
        coords = {}
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            # mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            if i.value == ArchType.UPPER.value:
                pts = np.array([
                    np.mean([
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    ], axis=0),
                    np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                    ], axis=0),
                    np.mean([
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    ], axis=0),
                ])
            coords[i.value] = pts
        return coords
    else:
        return {}

def calculate_flat_plane_points_DEPRECATED2(self):
    if Arch._is_complete():
        coords = {}
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            if i.value == ArchType.UPPER.value:
                pts = np.array([
                    np.mean([
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        #
                        # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN.value],
                        # teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        # teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    ], axis=0),
                    np.mean([
                        # teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
                        # teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                        # teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
                        # teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
                    ], axis=0),
                    np.mean([
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        #
                        # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN.value],
                        # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    ], axis=0),
                ])
            if i.value == ArchType.LOWER.value:
                pts = np.array([
                    np.mean([
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],

                        teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    ], axis=0),
                    np.mean([
                        teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
                        teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
                    ], axis=0),
                    np.mean([
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],

                        teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                        teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                        teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                        teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    ], axis=0),
                ])
            if i.value == ArchType.UPPER.value:
                pts_cusps_OUT = np.array([
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
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
                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                ])
            if i.value == ArchType.LOWER.value:
                pts_cusps_OUT = np.array([
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
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
                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                ])
            if i.value == ArchType.UPPER.value:
                pts_cusps_IN = np.array([
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],

                    teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_IN.value],

                    # teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],

                    teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN.value],

                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],

                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                ])
            if i.value == ArchType.LOWER.value:
                pts_cusps_IN = np.array([
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],

                    teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                    teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_IN.value],

                    # teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                    # teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],

                    teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
                    teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],

                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],

                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                    teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                ])

            new_coords_OUT = []
            for pt in pts_cusps_OUT:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords_OUT.append(new_coord)
            new_coords_IN = []
            for pt in pts_cusps_IN:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords_IN.append(new_coord)
            coords[i.value] = [new_coords_OUT, new_coords_IN]
        return coords
    else:
        return {}

def calculate_flat_plane_points_DEPRECATED(self):
    if Arch._is_complete():
        coords = {}
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
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
            coords[i.value] = new_coords
        return coords
    else:
        return {}
    
def calculate_studi_model_summary_pts(self):
    res = {}
    if(Arch._is_complete()):
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            msh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            preds=[]
            legacies=[]
            teeth_type=[
                ToothType.MOLAR_UL7_LR7.value,
                ToothType.MOLAR_UR7_LL7.value
            ]
            teeth_type_pont=[

                ToothType.MOLAR_UL6_LR6.value,
                ToothType.PREMOLAR_UL4_LR4.value,

                ToothType.PREMOLAR_UR4_LL4.value,
                ToothType.MOLAR_UR6_LL6.value,
            ]
            teeth_type_anterior=[
                ToothType.CANINE_UL3_LR3.value,
                ToothType.INCISOR_UL2_LR2.value,
                ToothType.INCISOR_UL1_LR1.value,
                
                ToothType.INCISOR_UR1_LL1.value,
                ToothType.INCISOR_UR2_LL2.value,
                ToothType.CANINE_UR3_LL3.value,
            ]
            for tooth_type in teeth:
                if (tooth_type in teeth_type or tooth_type in teeth_type_anterior or tooth_type in teeth_type_pont):
                    legacies.append(teeth[tooth_type].center)
                
                if(tooth_type in teeth_type):
                    preds.append(teeth[tooth_type].center)
                elif(tooth_type in teeth_type_anterior ):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    
                    anterior_korkhaus_should_move=self.korkhaus_studi_model.status_line_to_width[i.value]
                    
                    new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(anterior_korkhaus_should_move)))
                    # P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                    # center = new_center
                    # center_arch = P
                    # new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                    preds.append(new_center)
                
                elif(tooth_type in teeth_type_pont):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    P=find_closest_point_between_a_point_and_a_line(teeth[tooth_type].center,[batas_awal,batas_akhir])
                    center = teeth[tooth_type].center
                    center_arch = P
                    val_cor = None
                    val_cor_status=None
                    if(tooth_type in [ToothType.MOLAR_UL6_LR6.value, ToothType.MOLAR_UR6_LL6.value]):
                        val_cor = -1*(self.pont_studi_model.delta_mp[i.value]/2.0)
                        val_cor_status = self.pont_studi_model.status_mp[i.value]
                    elif(tooth_type in [ToothType.PREMOLAR_UL4_LR4.value, ToothType.PREMOLAR_UR4_LL4.value]):
                        val_cor = -1*(self.pont_studi_model.delta_pv[i.value]/2.0)
                        val_cor_status=self.pont_studi_model.status_pv[i.value]
                    new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, val_cor)
                    preds.append(new_center)
            line_molar = [legacies[0],legacies[-1]]
            preds[0] = find_closest_point_between_a_point_and_a_line(preds[1],line_molar)
            preds[-1] = find_closest_point_between_a_point_and_a_line(preds[-2],line_molar)
            res[i.value]=[legacies,preds]
    return res        
                    
def calculate_studi_model_summary_pts_lama(self): #DEPRECETED
    res = {}
    if(Arch._is_complete()):
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            msh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            preds=[]
            legacies=[]
            teeth_type=[
                ToothType.MOLAR_UL7_LR7.value,
                ToothType.MOLAR_UR7_LL7.value
            ]
            teeth_type_pont=[

                ToothType.MOLAR_UL6_LR6.value,
                ToothType.PREMOLAR_UL4_LR4.value,

                ToothType.PREMOLAR_UR4_LL4.value,
                ToothType.MOLAR_UR6_LL6.value,
            ]
            teeth_type_anterior=[
                ToothType.CANINE_UL3_LR3.value,
                ToothType.INCISOR_UL2_LR2.value,
                ToothType.INCISOR_UL1_LR1.value,
                
                ToothType.INCISOR_UR1_LL1.value,
                ToothType.INCISOR_UR2_LL2.value,
                ToothType.CANINE_UR3_LL3.value,
            ]
            for tooth_type in teeth:
                if (tooth_type in teeth_type or tooth_type in teeth_type_anterior or tooth_type in teeth_type_pont):
                    legacies.append(teeth[tooth_type].center)
                
                if(tooth_type in teeth_type):
                    preds.append(teeth[tooth_type].center)

                elif(tooth_type in teeth_type_anterior ):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    proklinasi_atas=0
                    if(i.value == ArchType.UPPER.value):
                        proklinasi_atas=self.korkhaus_studi_model.status_khorkaus
                    if(self.bolton_studi_model.correction_arch_anterior == i.value):
                        new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(self.bolton_studi_model.correction_anterior+proklinasi_atas)))
                        P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                        center = new_center
                        center_arch = P
                        new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                        preds.append(new_center)
                    else:
                        new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(proklinasi_atas)))
                        P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                        center = new_center
                        center_arch = P
                        new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                        preds.append(new_center)
                        
                elif(tooth_type in teeth_type_pont):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    P=find_closest_point_between_a_point_and_a_line(teeth[tooth_type].center,[batas_awal,batas_akhir])
                    center = teeth[tooth_type].center
                    center_arch = P
                    val_cor = None
                    val_cor_status=None
                    if(tooth_type in [ToothType.MOLAR_UL6_LR6.value, ToothType.MOLAR_UR6_LL6.value]):
                        val_cor = self.pont_studi_model.delta_mp[i.value]/2.0
                        val_cor_status = self.pont_studi_model.status_mp[i.value]
                    elif(tooth_type in [ToothType.PREMOLAR_UL4_LR4.value, ToothType.PREMOLAR_UR4_LL4.value]):
                        val_cor = self.pont_studi_model.delta_pv[i.value]/2.0
                        val_cor_status=self.pont_studi_model.status_pv[i.value]
                    new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, val_cor)
                    preds.append(new_center)
            res[i.value]=[legacies,preds]
    return res
                        
def get_flat_plane_DEPRECATED(self): # deprecated
    if Arch._is_complete():
        coords = []
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            
            # pts = np.array([
            #     mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            #     np.mean([
            #         mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
            #         mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]]
            #     ], axis=0),
            #     mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]]
            # ])
            pts = np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                np.mean([
                    teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                    teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                ], axis=0),
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
            for pp in pts:
                self.model_plot.add(Point(pp, c="violet"))
            print("pts plane",pts)
            # n = np.cross(pts[0]-pts[1],pts[2]-pts[1])
            # n = n/np.linalg.norm(n)
            # pts_cusps=np.array([
            #     mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
                
            #     mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            # ])
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
            
            print("pts_cusps",pts_cusps)
            new_coords = []
            for pt in pts_cusps:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords.append(new_coord)
            coords.append(new_coords)
        return coords
    else:
        return []
            
def calculate_destination_points(self):
    model_destination = {}
    As = get_As_pts(self)
    studi_model_summary_pts = get_studi_model_summary_pts(self)
    if(Arch._is_complete()):
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            arch = self.models[idx]
            dest = get_destination_points(arch, SplineKu(studi_model_summary_pts[i.value]), As[i.value], arch.right_left_vec)
            model_destination[i.value]=dest
    return model_destination               

def get_spl_pts_through_sphere(sphere, spl, A):
    # A = spl.getHalwayPoint()
    temp_spl = spl.clone().extrude(1).triangulate()
    inter = (sphere.intersectWith(temp_spl)).points()
    inter_dst=[]
    cls_pts = []
    for p in inter:
        cp = spl.closestPoint(p)
        cls_pts.append(cp)
        dis = find_distance_between_two_points(p,cp)
        inter_dst.append(dis)
    sk = KMeans(n_clusters=2,max_iter=20)
    sk = sk.fit(inter)
    label0dist=9999999
    label1dist=9999999
    label0pt=None
    label1pt=None
    for il in range(len(sk.labels_)):
        if(sk.labels_[il]==1):
            if(inter_dst[il]<label1dist):
                label1dist = inter_dst[il]
                label1pt=cls_pts[il]
        else:
            if(inter_dst[il]<label0dist):
                label0dist = inter_dst[il]
                label0pt=cls_pts[il]
    if(find_distance_between_two_points(A,label0pt) < find_distance_between_two_points(A,label1pt)):
        return [label0pt,label1pt]
    else:
        return [label1pt,label0pt]
    # return mesial distal

def get_destination_points(arch, spl, A, eig_right): #double sphere
    teeth = arch.teeth
    dests = {}
    labels_strt = [7,6,5,4,3,2,1]
    labels_end =  [8,9,10,11,12,13,14]
    a_strt = A[:]
    a_end = A[:]
    eig_right_inv = (eig_right[:])*-1
    for label in labels_strt:
        print("dst label", label)
        if teeth[label]:
            tooth = teeth[label]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value], tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_strt,r=rf/2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dis_mid = dst[1]
            if(label == 7):
                eig_l_m = np.dot(eig_right_inv, dst[0])
                eig_l_d = np.dot(eig_right_inv, dst[1])
                if(eig_l_m<eig_l_d):
                    dis_mid =dst[0]
                else:
                    dis_mid =dst[1]
            a_strt=dis_mid[:]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value], tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_strt,r=rf/2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dst.append(dis_mid)
            a_strt=dst[1][:]
            dests[label]= dst
            # if(arch.arch_type == ArchType.UPPER.value):
            #     sph = Sphere(a_strt,r=1.5)
            #     yy = get_spl_pts_through_sphere(sph, spl, A)
            #     a_strt=yy[1][:]
    for label in labels_end:
        print("dst label", label)
        if teeth[label]:
            tooth = teeth[label]
            # print(tooth.vertices, 'tooth v', label)
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value], tooth.landmark_pt[LandmarkType.DISTAL.value])
            print(rf, 'rf', label)
            sph = Sphere(a_end,r=rf/2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dis_mid = dst[1]
            if(label == 8):
                eig_r_m = np.dot(eig_right, dst[0])
                eig_r_d = np.dot(eig_right, dst[1])
                if(eig_r_m<eig_r_d):
                    dis_mid =dst[0]
                else:
                    dis_mid =dst[1]
            a_end=dis_mid[:]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value], tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_end,r=rf/2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dst.append(dis_mid)
            a_end=dst[1][:]
            dests[label]= dst
            # if(arch.arch_type == ArchType.UPPER.value):
            #     sph = Sphere(a_strt,r=1.5)
            #     yy = get_spl_pts_through_sphere(sph, spl, A)
            #     a_strt=yy[1][:]
    return dests