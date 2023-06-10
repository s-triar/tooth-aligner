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

def find_neighborhood_point(tooth, pt, deep=3):
    if deep<0:
        raise Exception("deep must be min 1")
    g = np.linalg.norm(tooth.points()-pt, axis=1)
    ind = np.argmin(g)
    cells = np.array(tooth.cells())
    t = np.where(cells==ind)
    hasil = np.unique(cells[t[0]])
    if deep <1:
        return hasil
    already_check = [ind]
    for i in range(deep-1):
        search = np.delete(hasil, np.where(np.isin(hasil, already_check)))
        temp = np.where(np.isin(cells, search))
        htemp = np.unique(cells[temp[0]])
        hasil = np.concatenate((hasil, htemp), axis=0)
        hasil = np.unique(hasil)
        already_check.extend(search)
    bound = tooth.boundaries(returnPointIds=True)
    hasil = np.delete(hasil, np.where(np.isin(hasil, bound)))
    return tooth.points()[hasil]

u = load('D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.vtp')
u4 = load('D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.vtp')
path_ld_u = 'D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.csv'
path_ld_l = 'D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.csv'

model = Arch(ArchType.UPPER.value,u)
model4 = Arch(ArchType.LOWER.value,u4)
load_ld(model,path_ld_u,ArchType.UPPER.value)
load_ld(model4,path_ld_l,ArchType.LOWER.value)

h=[]
for i in range(1,15):
    m = model.teeth[i].get_mesh()
    pt = model.teeth[i].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]

    pts =find_neighborhood_point(m, pt)
    h.extend(pts)
plt = Plotter()
plt.show(model.mesh, Points(h, c='r'))