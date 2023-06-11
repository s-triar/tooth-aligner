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
    getToothLabelSeberang, find_closest_point_between_a_point_and_a_3pts_plane,
)
from utility.calculation import (
    FaceTypeConversion,
    convert_to_2d, find_new_point_in_a_line_with_delta_distance, get_angle_from_2_2d_lines)
import math
from controller.summary_controller import get_bonwill, get_mesial_distal_as_R
from utility.tooth_label import get_tooth_labels
from utility.colors import map_label_color
from sklearn.cluster import KMeans
import pandas as pd
from utility.landmarking_lib import draw_eigen_vec


def load_ld(model, filename, typearch):
    df = pd.read_csv(filename, index_col=0)
    print(df.head())

    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        tooth = arch.teeth[row['label']]
        tooth.landmark_pt[row['landmark']] = np.array([row['x'], row['y'], row['z']])


def calculate_flat_plane_points(model):
    coords = {}

    i = model.arch_type
    if i == ArchType.UPPER.value:
        i = ArchType.UPPER
    else:
        i = ArchType.LOWER

    mesh = model.mesh
    teeth = model.teeth

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
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                #
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
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
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                #
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
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
    return pts, coords


def get_closest_to_mesial_distal(teeth, spl, B):
    cls_mesial = []
    cls_distal = []
    for toothlabel in teeth:
        tooth = teeth[toothlabel]
        if (tooth.label in tooth_labels['anterior'] or tooth.label in tooth_labels['canine']):

            mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
            distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
            closest_spl_mesial, closest_ln_mesial = spl.closestPointToAline([B, mesial], isAwal=(tooth.label > 7))
            closest_spl_distal, closest_ln_distal = spl.closestPointToAline([B, distal], isAwal=(tooth.label > 7))
            ln_distal = Line(B, distal, c="blue6")
            ln_mesial = Line(B, mesial, c="red6")
        else:  # posterior
            mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
            distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
            central_mesial_pt = find_closest_point_between_a_point_and_a_line(mesial, vertical_line)
            central_distal_pt = find_closest_point_between_a_point_and_a_line(distal, vertical_line)
            closest_spl_mesial, closest_ln_mesial = spl.closestPointToAline([central_mesial_pt, mesial],
                                                                            isAwal=(tooth.label > 7))
            closest_spl_distal, closest_ln_distal = spl.closestPointToAline([central_distal_pt, distal],
                                                                            isAwal=(tooth.label > 7))
            ln_distal = Line(central_distal_pt, distal, c="blue4")
            ln_mesial = Line(central_mesial_pt, mesial, c="red4")

        cls_mesial.append(Point(closest_spl_mesial, r=15, c="red6"))
        cls_distal.append(Point(closest_spl_distal, r=15, c="blue6"))
        cls_mesial.append(ln_mesial)
        cls_distal.append(ln_distal)
    return cls_mesial, cls_distal


def get_spl_pts_through_sphere(sphere, spl, A, ):
    # A = spl.getHalwayPoint()

    temp_spl = spl.clone().extrude(1).triangulate()
    # print("temp_spl")
    inter = (sphere.intersectWith(temp_spl)).points()

    # print("inter")
    inter_dst = []
    cls_pts = []
    for p in inter:
        cp = spl.closestPoint(p)
        cls_pts.append(cp)
        dis = find_distance_between_two_points(p, cp)
        inter_dst.append(dis)

    # plt = Plotter()
    # plt.add(spl)
    # plt.add(Points(inter))
    # plt.add(Points(cls_pts, c='red',r=16))
    # plt.add(Points(spl.points(), c='green'))
    # plt.show()
    # print("inter_dst", inter_dst)
    sk = KMeans(n_clusters=2, max_iter=80)
    sk = sk.fit(inter)
    # print("sk")
    label0dist = 9999999
    label1dist = 9999999
    label0pt = None
    label1pt = None
    for il in range(len(sk.labels_)):
        if (sk.labels_[il] == 1):
            if (inter_dst[il] < label1dist):
                label1dist = inter_dst[il]
                label1pt = cls_pts[il]
        else:
            if (inter_dst[il] < label0dist):
                label0dist = inter_dst[il]
                label0pt = cls_pts[il]
    if (find_distance_between_two_points(A, label0pt) < find_distance_between_two_points(A, label1pt)):
        return [label0pt, label1pt]
    else:
        return [label1pt, label0pt]
    # return mesial distal


global OJK
OJK = None
global OKK
OKK = None


def get_destination_points(arch, spl, A, eig_right):  # double sphere
    teeth = arch.teeth
    dests = {}
    labels_strt = [7, 6, 5, 4, 3, 2, 1]
    labels_end = [8, 9, 10, 11, 12, 13, 14]
    a_strt = A[:]
    a_end = A[:]
    eig_right_inv = (eig_right[:]) * -1
    for label in labels_strt:
        if teeth[label]:
            # print("str", label)
            tooth = teeth[label]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value],
                                                  tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_strt, r=rf / 2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dis_mid = dst[1]
            if (label == 7):
                eig_l_m = np.dot(eig_right_inv, dst[0])
                eig_l_d = np.dot(eig_right_inv, dst[1])
                if (eig_l_m < eig_l_d):
                    dis_mid = dst[0]
                else:
                    dis_mid = dst[1]
            a_strt = dis_mid[:]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value],
                                                  tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_strt, r=rf / 2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dst.append(dis_mid)
            a_strt = dst[1][:]
            dests[label] = dst
            # print("str2", label)

            # if(arch.arch_type == ArchType.UPPER.value):
            #     sph = Sphere(a_strt,r=1.5)
            #     yy = get_spl_pts_through_sphere(sph, spl, A)
            #     a_strt=yy[1][:]
    for label in labels_end:
        if teeth[label]:
            # print("end", label)
            tooth = teeth[label]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value],
                                                  tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_end, r=rf / 2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dis_mid = dst[1]
            if (label == 8):
                eig_r_m = np.dot(eig_right, dst[0])
                eig_r_d = np.dot(eig_right, dst[1])
                if (eig_r_m < eig_r_d):
                    dis_mid = dst[0]
                else:
                    dis_mid = dst[1]
            a_end = dis_mid[:]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value],
                                                  tooth.landmark_pt[LandmarkType.DISTAL.value])
            # print("rf")
            sph = Sphere(a_end, r=rf / 2)
            # print("sph")
            # if label == 14:
            #     temp_spl = spl.clone().extrude(1).triangulate()
            #     plt = Plotter()
            #     plt.add(temp_spl, sph)
            #     plt.show()
            dst = get_spl_pts_through_sphere(sph, spl, A)
            # if label == 14:
            #     global OJK, OKK
            #     OJK = dis_mid[:]
            #     OKK = dst[:]
            #     print('OJK', OJK)
            #     print('DST', dst)
            # print("dst")

            dst.append(dis_mid)
            # print("dst append")

            a_end = dst[1][:]
            # if label == 13:
            #     print(dst)
            # if label == 14:
            #     # global OJK, OKK
            #     OJK = dis_mid[:]
            #     OKK = dst[:]
            #     print('OJK', OJK)
            #     print('DST', dst)
            # print("a_end")
            dests[label] = dst
            # print("end2", label)
            # if(arch.arch_type == ArchType.UPPER.value):
            #     sph = Sphere(a_strt,r=1.5)
            #     yy = get_spl_pts_through_sphere(sph, spl, A)
            #     a_strt=yy[1][:]
    return dests


def calculate_flat_plane_points_belt(model, dst_pts):
    teeth = model.teeth
    arch_type = model.arch_type
    if arch_type == ArchType.UPPER.value:
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
    if arch_type == ArchType.LOWER.value:
        pts = np.array([
            np.mean([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                #
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                # teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
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
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                #
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_DISTAL.value],
                # teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_IN_MESIAL.value],
                # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                # teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_IN.value],
            ], axis=0),
        ])
    res = {}
    res_gum = {}
    for pt in dst_pts:
        temp = []
        temp_gum = []
        new_coord = find_closest_point_between_a_point_and_a_3pts_plane(dst_pts[pt][0], pts)
        temp.append(new_coord)
        new_coord = find_new_point_in_a_line_with_new_distance(new_coord, dst_pts[pt][0],
                                                               find_distance_between_two_points(new_coord,
                                                                                                dst_pts[pt][0]) * 2)
        temp_gum.append(new_coord)
        new_coord = find_closest_point_between_a_point_and_a_3pts_plane(dst_pts[pt][1], pts)
        temp.append(new_coord)
        new_coord = find_new_point_in_a_line_with_new_distance(new_coord, dst_pts[pt][1],
                                                               find_distance_between_two_points(new_coord,
                                                                                                dst_pts[pt][1]) * 2)
        temp_gum.append(new_coord)
        new_coord = find_closest_point_between_a_point_and_a_3pts_plane(dst_pts[pt][2], pts)
        temp.append(new_coord)
        new_coord = find_new_point_in_a_line_with_new_distance(new_coord, dst_pts[pt][2],
                                                               find_distance_between_two_points(new_coord,
                                                                                                dst_pts[pt][2]) * 2)
        temp_gum.append(new_coord)
        res[pt] = temp
        res_gum[pt] = temp_gum
    return res, res_gum


def find_neighborhood_point(mesh, pt, deep=3):
    if deep < 0:
        raise Exception("deep must be min 1")
    g = np.linalg.norm(mesh.points() - pt, axis=1)
    ind = np.argmin(g)
    cells = np.array(mesh.cells())
    t = np.where(cells == ind)
    hasil = np.unique(cells[t[0]])
    if deep < 1:
        return hasil
    already_check = [ind]
    for i in range(deep - 1):
        search = np.delete(hasil, np.where(np.isin(hasil, already_check)))
        temp = np.where(np.isin(cells, search))
        htemp = np.unique(cells[temp[0]])
        hasil = np.concatenate((hasil, htemp), axis=0)
        hasil = np.unique(hasil)
        already_check.extend(search)
    bound = mesh.boundaries(returnPointIds=True)
    hasil = np.delete(hasil, np.where(np.isin(hasil, bound)))
    return mesh.points()[hasil]


# l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo LowerJawScan _d_predicted_refined.vtp')
# u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan _d_predicted_refined.vtp')
# u4 = load('D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_new_bonwill_standalone\\Gerry Sihaj\\step_4\\Gerry Sihaj_UPPER__step_4.vtp')
u = load('D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.vtp')
u4 = load('D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.vtp')
path_ld_u = 'D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.csv'
path_ld_l = 'D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.csv'

# u = load('D:\\tesis\\fix\\4. SN\\SN._UPPER.vtp')
# u4 = load('D:\\tesis\\fix\\4. SN\\SN._LOWER.vtp')
# path_ld_u = 'D:\\tesis\\fix\\4. SN\\SN._UPPER.csv'
# path_ld_l = 'D:\\tesis\\fix\\4. SN\\SN._LOWER.csv'


u = load('D:\\tesis\\fix\\12. KEC\\KEC_UPPER.vtp')
u4 = load('D:\\tesis\\fix\\12. KEC\\KEC_LOWER.vtp')
path_ld_u = 'D:\\tesis\\fix\\12. KEC\\KEC_UPPER.csv'
path_ld_l = 'D:\\tesis\\fix\\12. KEC\\KEC_LOWER.csv'

model = Arch(ArchType.UPPER.value, u)
model4 = Arch(ArchType.LOWER.value, u4)
load_ld(model, path_ld_u, ArchType.UPPER.value)
load_ld(model4, path_ld_l, ArchType.LOWER.value)

titiks, vertical_line, B, A = get_bonwill(u, model)
print(len(titiks))
titiks4, vertical_line4, B4, A4 = get_bonwill(u4, model4)
tooth_labels = get_tooth_labels()
R = get_mesial_distal_as_R(model)
spl = SplineKu(titiks)
spl4 = SplineKu(titiks4)

cls_mesial, cls_distal = get_closest_to_mesial_distal(model.teeth, spl, B)
cls_mesial4, cls_distal4 = get_closest_to_mesial_distal(model4.teeth, spl, B4)

ptd = cls_distal[14]
# rf = find_distance_between_two_points(cls_mesial[14].points()[0], ptd.points()[0])
# print(rf)
# sph = Sphere(ptd.points()[0],r=rf)

# ptthr = get_spl_pts_through_sphere(sph, spl)

# cmid = Point(ptthr[0],c="yellow",r=20)
# fmid = Point(ptthr[1],c="green",r=20)

# sph.alpha(0.3)

destinations_pts = get_destination_points(model, spl, A, model.right_left_vec)

destinations_pts_belt, destinations_pts_belt_gum = calculate_flat_plane_points_belt(model, destinations_pts)

destinations_line = []
i = 0
pm = []
pd = []
for lbl in destinations_pts:
    temp = destinations_pts[lbl]
    c = map_label_color(lbl)
    # print(temp)
    # c="red"
    # if(i%3==1):
    #     c="blue"
    # elif(i%3==2):
    #     c="green"
    l = Line(temp[0], temp[1], lw=13, c=c)
    destinations_line.append(l)
    # pm.append(Point(temp[0],r=20))
    # pd.append(Point(temp[1],r=20))
    i += 1
i = 0
for lbl in destinations_pts_belt:
    temp = destinations_pts_belt[lbl]
    c = map_label_color(lbl)
    # print(temp)
    # c="red"
    # if(i%3==1):
    #     c="blue"
    # elif(i%3==2):
    #     c="green"
    l = Line(temp[0], temp[1], lw=10, c=c)
    destinations_line.append(l)
    # pm.append(Point(temp[0],r=20))
    # pd.append(Point(temp[1],r=20))
    i += 1
for lbl in destinations_pts_belt_gum:
    temp = destinations_pts_belt_gum[lbl]
    c = map_label_color(lbl)
    # print(temp)
    # c="red"
    # if(i%3==1):
    #     c="blue"
    # elif(i%3==2):
    #     c="green"
    l = Line(temp[0], temp[1], lw=10, c=c)
    destinations_line.append(l)
    # pm.append(Point(temp[0],r=20))
    # pd.append(Point(temp[1],r=20))
    i += 1

mesh = model.mesh
teeth = model.teeth

pts, coords = calculate_flat_plane_points(model)
new_coords_out = coords[model.arch_type][0]
new_coords_in = coords[model.arch_type][1]

mm = Mesh([pts, [[0, 1, 2]]], c='red5').alpha(0.7)


def is_point_in_triangle_3d(point, triangle):
    """
    Check if a point is inside a triangle in 3D space.

    Args:
        point: A tuple or list containing the coordinates of the point in (x, y, z) format.
        triangle: A list of three tuples or lists, each representing the coordinates of a vertex of the triangle.

    Returns:
        True if the point lies inside the triangle, False otherwise.
    """
    p = np.array(point)
    a = np.array(triangle[0])
    b = np.array(triangle[1])
    c = np.array(triangle[2])

    # Calculate the vectors from vertex A to the other two vertices
    v0 = c - a
    v1 = b - a
    v2 = p - a

    # Calculate dot products
    dot00 = np.dot(v0, v0)
    dot01 = np.dot(v0, v1)
    dot02 = np.dot(v0, v2)
    dot11 = np.dot(v1, v1)
    dot12 = np.dot(v1, v2)

    # Calculate barycentric coordinates
    inv_denom = 1.0 / (dot00 * dot11 - dot01 * dot01)
    u = (dot11 * dot02 - dot01 * dot12) * inv_denom
    v = (dot00 * dot12 - dot01 * dot02) * inv_denom

    # Check if the barycentric coordinates satisfy the condition for the point to lie inside the triangle
    if (u >= 0) and (v >= 0) and (u + v <= 1):
        return True
    else:
        return False


trgt_pts_out = Points(new_coords_out, c='orange', r=12)
trgt_pts_in = Points(new_coords_in, c='yellow', r=12)
spl_out = SplineKu(trgt_pts_out)
spl_in = SplineKu(trgt_pts_in)

tri = [
    [0, 0, 0],
    [-3, 6, 8],
    [3, -1, -1]
]

trip = [0.2, 10, 8]
gh = find_closest_point_between_a_point_and_a_3pts_plane(trip, np.array(tri))
meshtri = Mesh([tri, [[0, 1, 2]]])
opopop = is_point_in_triangle_3d(gh, meshtri.points())
print("in tri", opopop)

hj = find_closest_point_between_a_point_and_a_line(trip, np.array([tri[1], tri[2]]))

ttty = []
for lbl in model.teeth:
    if lbl != ToothType.DELETED.value and lbl != ToothType.GINGIVA.value:
        pts = find_neighborhood_point(model.teeth[lbl].get_mesh(), model.teeth[lbl].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value])
        ttty.extend(pts)



# ff= Point(ptd.points()[0],c="black",r=20)
# ln.rotate(45, axis=ln.points()[0], point=ln.points()[0])
# ln.c("yellow").lw(10)
# lp = Line(-ln.points()[0]+ln.points()[0],ln.points()[0]+ln.points()[0], c="orange",lw=10)
eigdraw = draw_eigen_vec(model.orientatin_vec, model.mesh.centerOfMass())
plt = Plotter(N=4, axes=1)
plt.show(model.mesh, Points(ttty), at=0)
plt.show(model4.mesh, spl, cls_mesial4, cls_distal4, at=1)
plt.show(model.mesh, spl, destinations_line, eigdraw, at=2)
plt.show(model.mesh, eigdraw, mm, trgt_pts_out, trgt_pts_in, spl_out, spl_in, at=3)
# plt.show(Point(trip, c='red', r=16), meshtri, Points(tri), Point(gh, c='green', r=15), Line(trip, hj), at=4)
plt.interactive()