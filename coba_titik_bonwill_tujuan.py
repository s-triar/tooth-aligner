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
from utility.calculation import (
    FaceTypeConversion, 
    convert_to_2d,  find_new_point_in_a_line_with_delta_distance, get_angle_from_2_2d_lines)
import math
from controller.summary_controller import get_bonwill, get_mesial_distal_as_R
from utility.tooth_label import get_tooth_labels
from sklearn.cluster import KMeans

def get_closest_to_mesial_distal(teeth,spl, B):
    cls_mesial = []
    cls_distal = []
    for toothlabel in teeth:
        tooth = teeth[toothlabel]
        if(tooth.label in tooth_labels['anterior'] or tooth.label in tooth_labels['canine']):
            
            mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
            distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
            closest_spl_mesial, closest_ln_mesial = spl.closestPointToAline([B, mesial],isAwal=(tooth.label>7))
            closest_spl_distal, closest_ln_distal = spl.closestPointToAline([B, distal],isAwal=(tooth.label>7))
            ln_distal = Line(B, distal, c="blue6")
            ln_mesial = Line(B, mesial, c="red6")
        else: #posterior
            mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
            distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
            central_mesial_pt = find_closest_point_between_a_point_and_a_line(mesial, vertical_line)
            central_distal_pt = find_closest_point_between_a_point_and_a_line(distal, vertical_line)
            closest_spl_mesial, closest_ln_mesial = spl.closestPointToAline([central_mesial_pt, mesial],isAwal=(tooth.label>7))
            closest_spl_distal, closest_ln_distal = spl.closestPointToAline([central_distal_pt, distal],isAwal=(tooth.label>7))
            ln_distal = Line(central_distal_pt, distal, c="blue4")
            ln_mesial = Line(central_mesial_pt, mesial, c="red4")
        
        cls_mesial.append(Point(closest_spl_mesial, r=15, c="red6"))
        cls_distal.append(Point(closest_spl_distal, r=15, c="blue6"))
        cls_mesial.append(ln_mesial)
        cls_distal.append(ln_distal)
    return cls_mesial, cls_distal

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
            sph = Sphere(a_strt,r=1.5)
            yy = get_spl_pts_through_sphere(sph, spl, A)
            a_strt=yy[1][:]
    for label in labels_end:
        if teeth[label]:
            tooth = teeth[label]
            rf = find_distance_between_two_points(tooth.landmark_pt[LandmarkType.MESIAL.value], tooth.landmark_pt[LandmarkType.DISTAL.value])
            sph = Sphere(a_end,r=rf/2)
            dst = get_spl_pts_through_sphere(sph, spl, A)
            dis_mid = dst[1]
            if(label == 7):
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
            sph = Sphere(a_strt,r=1.5)
            yy = get_spl_pts_through_sphere(sph, spl, A)
            a_strt=yy[1][:]
    return dests

            
# l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo LowerJawScan _d_predicted_refined.vtp')
u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\Gerry Sihaj UpperJawScan _d_predicted_refined.vtp')
u4 = load('D:\\NyeMan\\KULIAH S2\\Thesis\\tooth-aligner\\saved_new_bonwill_standalone\\Gerry Sihaj\\step_4\\Gerry Sihaj_UPPER__step_4.vtp')
model = Arch(ArchType.UPPER.value,u)
model4 = Arch(ArchType.LOWER.value,u4)

titiks, vertical_line, B, A = get_bonwill(u, model)
print(len(titiks))
titiks4, vertical_line4, B4, A4 = get_bonwill(u4, model4)
tooth_labels = get_tooth_labels()
R = get_mesial_distal_as_R(model)
spl = SplineKu(titiks)
spl4 = SplineKu(titiks4)

cls_mesial, cls_distal =get_closest_to_mesial_distal(model.teeth,spl,B)
cls_mesial4, cls_distal4 =get_closest_to_mesial_distal(model4.teeth,spl,B4)

ptd = cls_distal[14]
rf = find_distance_between_two_points(cls_mesial[14].points()[0], ptd.points()[0])
print(rf)
sph = Sphere(ptd.points()[0],r=rf)

# ptthr = get_spl_pts_through_sphere(sph, spl)

# cmid = Point(ptthr[0],c="yellow",r=20)
# fmid = Point(ptthr[1],c="green",r=20)

sph.alpha(0.3)

destinations_pts = get_destination_points(model, spl, A, model.right_left_vec)
destinations_line = []
i=0
pm=[]
pd=[]
for lbl in destinations_pts:
    temp=destinations_pts[lbl]
    print(temp)
    c="red"
    if(i%3==1):
        c="blue"
    elif(i%3==2):
        c="green"
    l = Line(temp[0],temp[1],lw=13,c=c)
    destinations_line.append(l)
    # pm.append(Point(temp[0],r=20))
    # pd.append(Point(temp[1],r=20))
    i+=1

# ff= Point(ptd.points()[0],c="black",r=20)
# ln.rotate(45, axis=ln.points()[0], point=ln.points()[0])
# ln.c("yellow").lw(10)   
# lp = Line(-ln.points()[0]+ln.points()[0],ln.points()[0]+ln.points()[0], c="orange",lw=10)
plt = Plotter(N=3)
plt.show(model.mesh, spl, cls_mesial, cls_distal, at=0)
plt.show(model4.mesh, spl, cls_mesial4, cls_distal4, at=1)
plt.show( model.mesh,spl,destinations_line,pd, at=2)
plt.interactive()