from vedo import *
import numpy as np
import math
from utility import neighboring_lib as nl
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def extract_labels(mesh):
    temp_obj_info = {}
    N = mesh.NCells()
    labels = np.unique(mesh.celldata['Label'])
    points = vtk2numpy(mesh.polydata().GetPoints().GetData())  # vertices (coordinate)
    ids = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:, 1:]  # faces (list of index of vertices)
    # cells = points[ids].reshape(N, 9).astype(dtype='float32')
    centers = []
    label_names = []
    temp_obj_info['labels'] = {}
    for label in labels:
        cells_label_index = np.where(mesh.celldata['Label'] == label)
        cells_label = ids[cells_label_index]
        points_index = np.unique(cells_label)
        points_label = points[points_index]
        points_tooth = points[cells_label]
        vtk_label = Mesh([points_label, cells_label])  # tooth, gingiva
        center_label = vtk_label.centerOfMass()
        # if label != 0.:
        centers.append(center_label)
        label_names.append(label)
        temp_obj_info['labels'][label] = {}
        temp_obj_info['labels'][label]['vtk'] = vtk_label
        temp_obj_info['labels'][label]['center'] = center_label
        temp_obj_info['labels'][label]['vertices'] = points_label
        temp_obj_info['labels'][label]['cells'] = cells_label
        temp_obj_info['labels'][label]['vertices_cell'] = points_tooth
    temp_obj_info['centers'] = centers
    temp_obj_info['label_names'] = label_names
    return temp_obj_info


def draw_eigen_vec(eigen_vec, center):
    left_right = eigen_vec[0]
    forward_backward = eigen_vec[1]
    upward_downward = eigen_vec[2]
    line_lr = Line(center - left_right, center + left_right, c="red")
    line_fb = Line(center - forward_backward, center + forward_backward, c="green")
    line_ud = Line(center - upward_downward, center + upward_downward, c="blue")
    point_lr = Point((center - left_right), c="red", r=15)
    point_fb = Point((center - forward_backward), c="green", r=15)
    point_ud = Point((center - upward_downward), c="blue", r=15)
    point_lr2 = Point((center + left_right), c="pink", r=15)
    point_fb2 = Point((center + forward_backward), c="yellow", r=15)
    point_ud2 = Point((center + upward_downward), c="violet", r=15)
    return [line_lr, line_fb, line_ud, point_fb, point_fb2, point_lr, point_lr2, point_ud, point_ud2]


def getEigenAttachment(points):
    # print("center_incisors",center_incisors)
    # print("center_molar",center_molar)
    points_np = np.array(points, dtype=np.float32)
    points_np_t = points_np.transpose()
    m = np.matmul(points_np_t, points_np)
    eig_linal = np.linalg.eig(m)
    # print(eig_linal)
    eig_val = eig_linal[0]
    eig_vec = eig_linal[1]
    arrindx = eig_val.argsort()
    # print(arrindx)
    eig_val = eig_val[arrindx[::-1]]
    eig_vec = eig_vec[arrindx[::-1]]
    return eig_val, eig_vec


def getEigenPlain(points):
    points_np = np.array(points, dtype=np.float32)
    points_np_t = points_np.transpose()
    m = np.matmul(points_np_t, points_np)
    eig_linal = np.linalg.eig(m)
    # print(eig_linal)
    eig_val = eig_linal[0]
    eig_vec = eig_linal[1]
    arrindx = eig_val.argsort()
    # print(arrindx)
    eig_val = eig_val[arrindx[::-1]]
    eig_vec = eig_vec[arrindx[::-1]]
    return eig_val, eig_vec


def getEigen(points, idx_faces, cell_data, label_anterior):
    # print("center_incisors",center_incisors)
    # print("center_molar",center_molar)
    points_np = np.array(points, dtype=np.float32)
    points_np_t = points_np.transpose()
    m = np.matmul(points_np_t, points_np)
    eig_linal = np.linalg.eig(m)
    # print(eig_linal)
    eig_val = eig_linal[0]
    eig_vec = eig_linal[1]
    arrindx = eig_val.argsort()
    # print(arrindx)
    eig_val = eig_val[arrindx[::-1]]
    eig_vec = eig_vec[arrindx[::-1]]
    # print(eig_val)
    # print(eig_vec)
    # if rahang==True:
    # ============================================

    # Fixing position Eigen vector

    # depan belakang

    # ori_fb = np.dot(p_bottom_indicator,eig_vec[1]) # DEPRECATED
    # inv_fb = np.dot(p_bottom_indicator,eig_vec[1]*-1) # DEPRECATED
    # DONE TODO CHECK THE DISTANCE WITH INCISOR 1ST LEFT AND RIGHT TEETH WITH LABEL 7 AND 8 INSTEAD
    center_anteriors = []
    center_anterior = 0
    for label in label_anterior:
        cells_tooth_index = np.where(cell_data == label)
        if (len(cells_tooth_index[0]) > 0):
            label = math.floor(label)
            cells_tooth = idx_faces[cells_tooth_index]
            points_tooth_index = np.unique(cells_tooth)
            points_tooth = points[points_tooth_index]
            center_tooth = np.mean(points_tooth, axis=0)
            center_anteriors.append(center_tooth)
    center_anterior = np.mean(center_anteriors, axis=0)

    ori_fb = np.dot(center_anterior, eig_vec[1])
    inv_fb = np.dot(center_anterior, eig_vec[1] * -1)
    if (ori_fb > inv_fb):
        eig_vec[1] *= -1

        # atas bawah
    p_bottom_indicator, s_p = nl.get_bottom(points, np.array(idx_faces))
    temp_eig_up_down = eig_vec[2] * -1
    if (
            np.dot(eig_vec[2], p_bottom_indicator) < np.dot(temp_eig_up_down, p_bottom_indicator)
    ):
        eig_vec[2] *= -1
    # kanan kiri
    # THIS IS NOT ROBUST.
    # DONE? TODO CHECK THE DISTANCE WITH MOLAR TOOTH WITH LABEL 1 OR 2 INSTEAD
    # det_eig = np.linalg.det([eig_vec[0], eig_vec[1], eig_vec[2]])
    # if(det_eig==1):
    #     eig_vec[0] *=-1
    center_lefts = []
    center_left = 0
    for label in [1, 2, 3, 4]:
        cells_tooth_index = np.where(cell_data == label)
        if (len(cells_tooth_index[0]) > 0):
            label = math.floor(label)
            cells_tooth = idx_faces[cells_tooth_index]
            points_tooth_index = np.unique(cells_tooth)
            points_tooth = points[points_tooth_index]
            center_tooth = np.mean(points_tooth, axis=0)
            center_lefts.append(center_tooth)
    center_left = np.mean(center_lefts, axis=0)
    ori_rl = np.dot(center_left, eig_vec[0])
    inv_rl = np.dot(center_left, eig_vec[0] * -1)
    if (ori_rl < inv_rl):
        eig_vec[0] *= -1
        # left_right = eig_vec[0]
    # forward_backward = eig_vec[1]
    # upward_downward = eig_vec[2]
    return eig_val, eig_vec


def map_point_index(unique_indexes):
    temp = {}
    for i in range(len(unique_indexes)):
        temp[unique_indexes[i]] = i
    return temp


def mapping_point_index(map, indexes):
    temp = []
    for i in range(len(indexes)):
        temp_j = []
        for j in range(len(indexes[i])):
            temp_j.append(map[indexes[i][j]])
        temp.append(temp_j)
    return temp


def get_index_point_from_mesh_vertices(point, points):
    return np.argwhere(np.isin(points, point).all(axis=1))[0][0]


def get_buccal_or_labial_andlingual_or_palatal_anterior(label, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # pts=[]
    # rr = np.where(temp_r>center_r-0.75)
    # ll = np.where(temp_r<center_r+0.75)
    # uu = np.where(temp_u>center_u-0.75)
    # dd = np.where(temp_u<center_u+0.75)
    # rrll = np.intersect1d(np.intersect1d(rr[0],ll[0]),np.intersect1d(uu[0],dd[0]))
    if (label in [6, 9]):
        cntr = np.where((temp_r > center_r - 0.75) & (temp_r < center_r + 0.75) & (temp_u > center_u - 0.75) & (
                    temp_u < center_u + 0.75))
    else:
        cntr = np.where((temp_r > center_r - 0.75) & (temp_r < center_r + 0.75) & (temp_u > center_u - 2.75) & (
                    temp_u < center_u + 0.75))

    cntr = cntr[0]
    # for i in cntr:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]

    ins_outs = []  # lingual or palatal and buccal or labial
    for v in vertices_new:
        # biru = np.dot(v,upward_downward)
        hijau = np.dot(v, forward_backward)
        merah = np.dot(v, left_right)
        pink = np.dot(v, left_right * -1)
        ins_outs.append(np.mean([hijau, pink, merah]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal = vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal  # , pts


def get_buccal_or_labial_andlingual_or_palatal_anterior_second(is_awal, is_upper, label, eigen_vec_mesh, center_tooth,
                                                               vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # pts=[]
    # rr = np.where(temp_r>center_r-0.75)
    # ll = np.where(temp_r<center_r+0.75)
    # uu = np.where(temp_u>center_u-0.75)
    # dd = np.where(temp_u<center_u+0.75)
    # rrll = np.intersect1d(np.intersect1d(rr[0],ll[0]),np.intersect1d(uu[0],dd[0]))
    if (label in [6, 9]):
        cntr = np.where((temp_r > center_r - 0.75) & (temp_r < center_r + 0.75) & (temp_u > center_u - 0.75) & (
                    temp_u < center_u + 0.75))
    else:
        cntr = np.where((temp_r > center_r - 0.75) & (temp_r < center_r + 0.75) & (temp_u > center_u - 2.75) & (
                    temp_u < center_u + 0.75))

    cntr = cntr[0]
    # for i in cntr:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]

    ins = []  # lingual or palatal and buccal or labial
    outs = []  # lingual or palatal and buccal or labial
    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        # biru = np.dot(v,upward_downward)
        hijau = np.dot(v, forward_backward)
        hijau_muda = np.dot(v, forward_backward * -1)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        if (is_upper):
            ins.append(np.mean([hijau_muda * 0.1, pink * 0.25, merah * 0.65]))
        else:
            ins.append(np.mean([hijau_muda * 0.15, pink * 0.425, merah * 0.425]))
        outs.append(np.mean([hijau * 0.15, pink * 0.85]))
    ins_index_sorted = np.argsort(ins)
    outs_index_sorted = np.argsort(outs)
    buccal_or_labial = vertices_new[outs_index_sorted[0]]
    lingual_or_palatal = vertices_new[ins_index_sorted[0]]
    return buccal_or_labial, lingual_or_palatal  # , pts


def get_buccal_or_labial_andlingual_or_palatal_canine(is_awal, is_upper, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    # pts=[]
    if is_awal == True:
        inv = -1
        cntr = np.where(
            (temp_r > center_r - 4) & (temp_r < center_r + 4) &
            (temp_u > center_u - 1.5) & (temp_u < center_u + 1.5) &
            (temp_f > center_f - 2.1) & (temp_f < center_f + 2)
        )
    else:
        inv = 1
        cntr = np.where(
            (temp_r > center_r - 4) & (temp_r < center_r + 4) &
            (temp_u > center_u - 1.5) & (temp_u < center_u + 1.5) &
            (temp_f > center_f - 2) & (temp_f < center_f + 2.1)
        )
    # print("cntr",cntr)
    cntr = cntr[0]
    # for i in cntr:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]

    ins_outs = []  # lingual or palatal and buccal or labial
    ins_outs_upper = []  # lingual or palatal and buccal or labial
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        hijau = np.dot(v, forward_backward)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        if (is_upper):
            ins_outs_upper.append(np.mean([biru * 0.1, pink * 0.3, merah * 0.5, hijau * 0.1]))
        else:
            ins_outs.append(np.mean([biru * 0.1, pink * 0.25, merah * 0.35, hijau * 0.3]))
    if is_upper:
        ins_outs_index_sorted = np.argsort(ins_outs_upper)
        buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
        lingual_or_palatal = vertices_new[ins_outs_index_sorted[-1]]
        return buccal_or_labial, lingual_or_palatal  # , pts
    else:
        ins_outs_index_sorted = np.argsort(ins_outs)
        buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
        lingual_or_palatal = vertices_new[ins_outs_index_sorted[-1]]
        return buccal_or_labial, lingual_or_palatal  # , pts


def get_buccal_or_labial_andlingual_or_palatal_premolar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth,
                                                        vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    # pts=[]
    if is_awal == True:
        inv = -1
        cntr = np.where(
            (temp_r > center_r - 5) & (temp_r < center_r + 4) &
            (temp_u > center_u - 1.5) & (temp_u < center_u + 2) &
            (temp_f > center_f - 2.5) & (temp_f < center_f + 1.8)
        )
    else:
        inv = 1
        cntr = np.where(
            (temp_r > center_r - 4) & (temp_r < center_r + 5) &
            (temp_u > center_u - 2) & (temp_u < center_u + 1.5) &
            (temp_f > center_f - 1.8) & (temp_f < center_f + 2.5)
        )
    # print("cntr",cntr)
    cntr = cntr[0]
    # for i in cntr:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]

    ins_outs = []  # lingual or palatal and buccal or labial
    for v in vertices_new:
        # biru = np.dot(v,upward_downward)
        hijau = np.dot(v, forward_backward)
        merah = np.dot(v, (left_right * inv))
        # pink = np.dot(v, (left_right * inv)  * -1)
        ins_outs.append(np.mean([merah * 0.6, hijau * 0.4]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal = vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal  # , pts


def get_buccal_or_labial_andlingual_or_palatal_molar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth,
                                                     vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    # pts=[]
    if is_awal == True:
        inv = -1
        cntr = np.where(
            (temp_r > center_r - 5) & (temp_r < center_r + 4) &
            (temp_u > center_u - 1.5) & (temp_u < center_u + 2) &
            (temp_f > center_f - 2.5) & (temp_f < center_f + 1.8)
        )
    else:
        inv = 1
        cntr = np.where(
            (temp_r > center_r - 4) & (temp_r < center_r + 5) &
            (temp_u > center_u - 2) & (temp_u < center_u + 1.5) &
            (temp_f > center_f - 1.8) & (temp_f < center_f + 2.5)
        )
    # print("cntr",cntr)
    cntr = cntr[0]
    # for i in cntr:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]

    ins_outs = []  # lingual or palatal and buccal or labial
    for v in vertices_new:
        # biru = np.dot(v,upward_downward)
        # hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right * inv))
        # pink = np.dot(v, (left_right * inv)  * -1)
        ins_outs.append(np.mean([merah]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal = vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal  # , pts


def get_mesial_distal_anterior(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    # forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    # most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)

    # most = np.argsort(temp_h)
    # most_h = vertices_tooth[most[0]]
    # pts=[]
    # pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h)  # temp[most[0]]+2.5
    # for i in ww[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))

    vertices_new = vertices_tooth[ww[0]]
    mesials = []
    distals = []

    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        # hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        mesials.append(np.mean([merah * 0.7, biru * 0.3]))
        distals.append(np.mean([pink * 0.7, biru * 0.3]))

    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal  # , pts


def get_mesial_distal_anterior_second(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    # most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)

    # most = np.argsort(temp_h)
    # most_h = vertices_tooth[most[0]]
    # pts=[]
    # pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h)  # temp[most[0]]+2.5
    # for i in ww[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))

    vertices_new = vertices_tooth[ww[0]]
    mesials = []
    distals = []

    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        hijau = np.dot(v, forward_backward)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        mesials.append(np.mean([merah * 0.45, hijau * 0.2, biru * 0.35]))
        distals.append(np.mean([pink * 0.75, biru * 0.25]))

    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal  # , pts


def get_mesial_distal_canine(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    # most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    # most = np.argsort(temp_h)
    # most_h = vertices_tooth[most[0]]
    # pts=[]
    # pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h)  # temp[most[0]]+2.5
    # for i in ww[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials = []
    distals = []
    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        hijau = np.dot(v, forward_backward)
        hijau_muda = np.dot(v, forward_backward * -1)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        mesials.append(np.mean([merah * 0.4, biru * 0.1, hijau * 0.5]))
        distals.append(np.mean([pink * 0.5, biru * 0.25, hijau_muda * 0.25]))

    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal  # , pts


def get_mesial_distal_premolar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    # most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    most = np.argsort(temp_h)
    # most_h = vertices_tooth[most[0]]
    # pts=[]
    # pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h)  # temp[most[0]]+2.5
    # for i in ww[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials = []
    distals = []
    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        hijau = np.dot(v, forward_backward)
        hijau_muda = np.dot(v, forward_backward * -1)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        mesials.append(np.mean([pink * 0.2, biru * 0.15, hijau * 0.45, merah * 0.2]))
        if (is_upper == False and (label == 3 or label == 12)):
            distals.append(np.mean([pink * 0.5, hijau_muda * 0.5]))
        else:
            distals.append(np.mean([pink * 0.4, biru * 0.1, hijau_muda * 0.5]))

    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal  # , pts


def get_mesial_distal_molar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    # most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    # most = np.argsort(temp_h)
    # most_h = vertices_tooth[most[0]]
    # pts=[]
    # pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h)  # temp[most[0]]+2.5
    # for i in ww[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials = []
    distals = []
    inv = 1
    if (is_awal == False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        # biru_muda = np.dot(v,upward_downward * -1)
        hijau = np.dot(v, forward_backward)
        hijau_muda = np.dot(v, forward_backward * -1)
        merah = np.dot(v, (left_right * inv))
        pink = np.dot(v, (left_right * inv) * -1)
        mesials.append(np.mean([pink * 0.2, biru * 0.15, hijau * 0.45, merah * 0.2]))
        if (is_upper == False and (label == 2 or label == 13)):
            distals.append(np.mean([pink * 0.7, hijau_muda * 0.3]))
        else:
            # distals.append(np.mean([pink*0.4,biru*0.1,hijau_muda*0.5]))
            distals.append(np.mean([pink * 0.65, hijau_muda * 0.35]))
            # distals.append(np.mean([pink]))

    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal  # , pts


def get_cusp_anterior(eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    # center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    # temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    crcl = np.where(
        (temp_r > center_r - 1) & (temp_r < center_r + 1) &
        (temp_f > center_f - 3) & (temp_f < center_f + 3)
    )
    # pts=[]
    # for i in crcl[0]:
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[crcl[0]]
    cusps = []
    for v in vertices_new:
        biru = np.dot(v, upward_downward)
        hijau = np.dot(v, forward_backward)
        cusps.append(np.mean([biru * 0.8, hijau * 0.2]))
    cusps_index_sorted = np.argsort(cusps)
    cusp = vertices_new[cusps_index_sorted[0]]
    return cusp  # , pts


def get_cusp_posterior_third_fourth_upper(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 4
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r)
    )
    vertices_in = np.where(
        (temp_u < center_u) & (temp_r > center_r)
    )
    if is_awal == True:
        vertices_out, vertices_in = vertices_in, vertices_out
    vertices_out_new = vertices_tooth[vertices_out[0]]
    vertices_in_new = vertices_tooth[vertices_in[0]]
    temp_f_in = np.matmul(forward_backward, np.transpose(vertices_in_new))
    temp_f_out = np.matmul(forward_backward, np.transpose(vertices_out_new))

    vertices_out_mesial = np.where(
        (temp_f_out < center_f - 1.0)  # -1.75
    )
    vertices_out_distal = np.where(
        (temp_f_out >= center_f - 1.5)  # -0.5
    )
    vertices_in_mesial = np.where(
        (temp_f_in < center_f + 1.5)
    )
    vertices_in_distal = np.where(
        (temp_f_in >= center_f + 1)
    )
    # pts=[]
    # for i in vertices_in_mesial[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink"))
    # for i in vertices_in_distal[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink3"))
    # for i in vertices_out_mesial[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink5"))
    # for i in vertices_out_distal[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink7"))

    vertices_in_mesial_new = vertices_in_new[vertices_in_mesial[0]]
    vertices_in_distal_new = vertices_in_new[vertices_in_distal[0]]
    vertices_out_mesial_new = vertices_out_new[vertices_out_mesial[0]]
    vertices_out_distal_new = vertices_out_new[vertices_out_distal[0]]

    vertices_in_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_in_mesial_new))
    cusps_in_mesial_index_sorted = np.argsort(vertices_in_mesial_new_up)
    cusp_in_mesial = vertices_in_mesial_new[cusps_in_mesial_index_sorted[0]]

    vertices_in_distal_new_up = np.dot(upward_downward, np.transpose(vertices_in_distal_new))
    cusps_in_distal_index_sorted = np.argsort(vertices_in_distal_new_up)
    cusp_in_distal = vertices_in_distal_new[cusps_in_distal_index_sorted[0]]

    vertices_out_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_out_mesial_new))
    cusps_out_mesial_index_sorted = np.argsort(vertices_out_mesial_new_up)
    cusp_out_mesial = vertices_out_mesial_new[cusps_out_mesial_index_sorted[0]]

    vertices_out_distal_new_up = np.dot(upward_downward, np.transpose(vertices_out_distal_new))
    cusps_out_distal_index_sorted = np.argsort(vertices_out_distal_new_up)
    cusp_out_distal = vertices_out_distal_new[cusps_out_distal_index_sorted[0]]

    return [cusp_in_mesial, cusp_in_distal, cusp_out_mesial, cusp_out_distal]  # , pts


def get_cusp_posterior_first_second_upper(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 2
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0]
    # forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    # center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r)
    )
    vertices_in = np.where(
        (temp_u < center_u) & (temp_r > center_r)
    )
    if is_awal == True:
        vertices_out, vertices_in = vertices_in, vertices_out
    # pts=[]
    # for i in vertices_out[0]:
    #     pts.append(Point(vertices_tooth[i],c="pink"))
    # for i in vertices_in[0]:
    #     pts.append(Point(vertices_tooth[i],c="pink5"))

    vertices_out_new = vertices_tooth[vertices_out[0]]
    vertices_in_new = vertices_tooth[vertices_in[0]]
    vertices_in_new_up = np.dot(upward_downward, np.transpose(vertices_in_new))
    vertices_out_new_up = np.dot(upward_downward, np.transpose(vertices_out_new))
    cusps_in_index_sorted = np.argsort(vertices_in_new_up)
    cusp_in = vertices_in_new[cusps_in_index_sorted[0]]

    cusps_out_index_sorted = np.argsort(vertices_out_new_up)
    cusp_out = vertices_out_new[cusps_out_index_sorted[0]]
    return [cusp_in, cusp_out]  # , pts


def get_cusp_posterior_first_premolar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 2
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0] * inv
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r + 0.25)
    )
    vertices_in = np.where(
        (temp_u < center_u) & (temp_r > center_r - 1) &  # center_r+2 #EDITTED
        #  (temp_f > center_f - 0.5)
        (temp_f > center_f - 1)  # center_f+0.7 #EDITTED
    )
    # pts=[]
    # for i in vertices_out[0]:
    #     pts.append(Point(vertices_tooth[i],c="pink"))
    # for i in vertices_in[0]:
    #     pts.append(Point(vertices_tooth[i],c="pink5"))

    vertices_out_new = vertices_tooth[vertices_out[0]]
    # print('vertices_in',vertices_in)
    vertices_in_new = vertices_tooth[vertices_in[0]]
    # print('vertices_in_new',vertices_in_new)
    vertices_in_new_up = np.dot(upward_downward, np.transpose(vertices_in_new))
    # print('vertices_in_new_up',vertices_in_new_up)
    vertices_out_new_up = np.dot(upward_downward, np.transpose(vertices_out_new))
    cusps_in_index_sorted = np.argsort(vertices_in_new_up)
    # print('cusps_in_index_sorted',cusps_in_index_sorted)

    cusp_in = vertices_in_new[cusps_in_index_sorted[0]]

    cusps_out_index_sorted = np.argsort(vertices_out_new_up)
    cusp_out = vertices_out_new[cusps_out_index_sorted[0]]
    return [cusp_in, cusp_out]  # , pts


def get_cusp_posterior_second_premolar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 3
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0] * inv
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r)
    )
    vertices_in = np.where(
        (temp_u < center_u) & (temp_r > center_r)
    )
    # if is_awal ==True:
    #     vertices_out, vertices_in = vertices_in, vertices_out
    vertices_out_new = vertices_tooth[vertices_out[0]]
    vertices_in_new = vertices_tooth[vertices_in[0]]
    temp_f_in = np.matmul(forward_backward, np.transpose(vertices_in_new))
    # temp_f_out = np.matmul(forward_backward, np.transpose(vertices_out_new))

    # vertices_out_mesial=np.where(
    #     (temp_f_out < center_f-1.75)
    # )
    # vertices_out_distal=np.where(
    #     (temp_f_out >= center_f-0.5)
    # )
    vertices_in_mesial = np.where(
        (temp_f_in < center_f + 1)  # center_f+1.5 #EDITTED
    )
    vertices_in_distal = np.where(
        (temp_f_in >= center_f + 1)  # center_f+2 #EDITTED
    )
    # pts=[]
    # for i in vertices_in_mesial[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink"))
    # for i in vertices_in_distal[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink3"))
    # # for i in vertices_out_mesial[0]:
    # #     pts.append(Point(vertices_out_new[i],c="pink5"))
    # for i in vertices_out[0]:
    #     pts.append(Point(vertices_tooth[i],c="brown"))

    vertices_in_mesial_new = vertices_in_new[vertices_in_mesial[0]]
    vertices_in_distal_new = vertices_in_new[vertices_in_distal[0]]
    # vertices_out_mesial_new = vertices_out_new[vertices_out_mesial[0]]
    # vertices_out_distal_new = vertices_out_new[vertices_out_distal[0]]

    vertices_in_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_in_mesial_new))
    cusps_in_mesial_index_sorted = np.argsort(vertices_in_mesial_new_up)
    cusp_in_mesial = vertices_in_mesial_new[cusps_in_mesial_index_sorted[0]]

    vertices_in_distal_new_up = np.dot(upward_downward, np.transpose(vertices_in_distal_new))
    cusps_in_distal_index_sorted = np.argsort(vertices_in_distal_new_up)
    cusp_in_distal = vertices_in_distal_new[cusps_in_distal_index_sorted[0]]

    # vertices_out_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_out_mesial_new))
    # cusps_out_mesial_index_sorted = np.argsort(vertices_out_mesial_new_up)
    # cusp_out_mesial = vertices_out_mesial_new[cusps_out_mesial_index_sorted[0]]

    vertices_out_new_up = np.dot(upward_downward, np.transpose(vertices_out_new))
    cusps_out_index_sorted = np.argsort(vertices_out_new_up)
    cusp_out = vertices_out_new[cusps_out_index_sorted[0]]

    return [cusp_in_mesial, cusp_in_distal, cusp_out]  # , pts


def get_cusp_posterior_first_molar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 5
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0] * inv
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r)
    )
    vertices_in = np.where(
        (temp_u < center_u + 2) & (temp_r > center_r + 1)
    )
    # if is_awal ==True:
    #     vertices_out, vertices_in = vertices_in, vertices_out
    vertices_out_new = vertices_tooth[vertices_out[0]]
    vertices_in_new = vertices_tooth[vertices_in[0]]
    temp_f_in = np.matmul(forward_backward, np.transpose(vertices_in_new))
    temp_f_out = np.matmul(forward_backward, np.transpose(vertices_out_new))

    vertices_out_mesial = np.where(
        (temp_f_out < center_f - 1.75)
    )
    vertices_out_middle = np.where(
        (temp_f_out > center_f - 1.75) &
        (temp_f_out < center_f + 1.75)
    )
    vertices_out_distal = np.where(
        (temp_f_out >= center_f + 2.5)
    )
    vertices_in_mesial = np.where(
        (temp_f_in < center_f + 1.5)
    )
    vertices_in_distal = np.where(
        (temp_f_in >= center_f + 2)
    )
    # pts=[]
    # for i in vertices_in_mesial[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink"))
    # for i in vertices_in_distal[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink3"))
    # for i in vertices_out_mesial[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink5"))
    # for i in vertices_out_middle[0]:
    #     pts.append(Point(vertices_out_new[i],c="green6"))
    # for i in vertices_out_distal[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink7"))

    vertices_in_mesial_new = vertices_in_new[vertices_in_mesial[0]]
    vertices_in_distal_new = vertices_in_new[vertices_in_distal[0]]
    vertices_out_mesial_new = vertices_out_new[vertices_out_mesial[0]]
    vertices_out_distal_new = vertices_out_new[vertices_out_distal[0]]
    vertices_out_middle_new = vertices_out_new[vertices_out_middle[0]]

    vertices_in_mesial_new_up = np.add(np.dot(upward_downward, np.transpose(vertices_in_mesial_new)) * 0.5,
                                       np.dot(left_right * -1, np.transpose(vertices_in_mesial_new)) * 0.5)
    cusps_in_mesial_index_sorted = np.argsort(vertices_in_mesial_new_up)
    cusp_in_mesial = vertices_in_mesial_new[cusps_in_mesial_index_sorted[0]]

    vertices_in_distal_new_up = np.add(np.dot(upward_downward, np.transpose(vertices_in_distal_new)) * 0.5,
                                       np.dot(left_right * -1, np.transpose(vertices_in_distal_new)) * 0.5)
    cusps_in_distal_index_sorted = np.argsort(vertices_in_distal_new_up)
    cusp_in_distal = vertices_in_distal_new[cusps_in_distal_index_sorted[0]]

    vertices_out_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_out_mesial_new))
    cusps_out_mesial_index_sorted = np.argsort(vertices_out_mesial_new_up)
    cusp_out_mesial = vertices_out_mesial_new[cusps_out_mesial_index_sorted[0]]

    vertices_out_distal_new_up = np.dot(upward_downward, np.transpose(vertices_out_distal_new))
    cusps_out_distal_index_sorted = np.argsort(vertices_out_distal_new_up)
    cusp_out_distal = vertices_out_distal_new[cusps_out_distal_index_sorted[0]]

    vertices_out_middle_new_up = np.dot(upward_downward, np.transpose(vertices_out_middle_new))
    cusps_out_middle_index_sorted = np.argsort(vertices_out_middle_new_up)
    cusp_out_middle = vertices_out_middle_new[cusps_out_middle_index_sorted[0]]

    return [cusp_in_mesial, cusp_in_distal, cusp_out_mesial, cusp_out_middle, cusp_out_distal]  # , pts


def get_cusp_posterior_second_molar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    # n_cusp = 4
    inv = 1
    if is_awal == True:
        inv = -1
    left_right = eigen_vec_mesh[0] * inv
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    # temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    vertices_out = np.where(
        (temp_u < center_u) & (temp_r < center_r)
    )
    vertices_in = np.where(
        (temp_u < center_u + 2) & (temp_r > center_r + 1)
    )
    # if is_awal ==True:
    #     vertices_out, vertices_in = vertices_in, vertices_out
    vertices_out_new = vertices_tooth[vertices_out[0]]
    vertices_in_new = vertices_tooth[vertices_in[0]]
    temp_f_in = np.matmul(forward_backward, np.transpose(vertices_in_new))
    temp_f_out = np.matmul(forward_backward, np.transpose(vertices_out_new))

    vertices_out_mesial = np.where(
        (temp_f_out < center_f - 1)  # -1.75
    )
    vertices_out_distal = np.where(
        (temp_f_out >= center_f - 0.5)
    )
    vertices_in_mesial = np.where(
        (temp_f_in < center_f + 1)  # +1
    )
    vertices_in_distal = np.where(
        (temp_f_in >= center_f + 2)
    )
    # pts=[]
    # for i in vertices_in_mesial[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink"))
    # for i in vertices_in_distal[0]:
    #     pts.append(Point(vertices_in_new[i],c="pink3"))
    # for i in vertices_out_mesial[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink5"))
    # for i in vertices_out_distal[0]:
    #     pts.append(Point(vertices_out_new[i],c="pink7"))
    # print("vertices_in_mesial")
    # print(vertices_in_mesial)
    vertices_in_mesial_new = vertices_in_new[vertices_in_mesial[0]]
    vertices_in_distal_new = vertices_in_new[vertices_in_distal[0]]
    vertices_out_mesial_new = vertices_out_new[vertices_out_mesial[0]]
    vertices_out_distal_new = vertices_out_new[vertices_out_distal[0]]
    # print("vertices_in_mesial_new")
    # print(vertices_in_mesial_new)
    # vertices_in_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_in_mesial_new))
    vertices_in_mesial_new_up = np.add(np.dot(upward_downward, np.transpose(vertices_in_mesial_new)) * 0.5,
                                       np.dot(left_right * -1, np.transpose(vertices_in_mesial_new)) * 0.5)

    cusps_in_mesial_index_sorted = np.argsort(vertices_in_mesial_new_up)
    cusp_in_mesial = vertices_in_mesial_new[cusps_in_mesial_index_sorted[0]]

    # vertices_in_distal_new_up = np.dot(upward_downward, np.transpose(vertices_in_distal_new))
    vertices_in_distal_new_up = np.add(np.dot(upward_downward, np.transpose(vertices_in_distal_new)) * 0.5,
                                       np.dot(left_right * -1, np.transpose(vertices_in_distal_new)) * 0.5)
    cusps_in_distal_index_sorted = np.argsort(vertices_in_distal_new_up)
    cusp_in_distal = vertices_in_distal_new[cusps_in_distal_index_sorted[0]]

    vertices_out_mesial_new_up = np.dot(upward_downward, np.transpose(vertices_out_mesial_new))
    cusps_out_mesial_index_sorted = np.argsort(vertices_out_mesial_new_up)
    cusp_out_mesial = vertices_out_mesial_new[cusps_out_mesial_index_sorted[0]]

    vertices_out_distal_new_up = np.dot(upward_downward, np.transpose(vertices_out_distal_new))
    cusps_out_distal_index_sorted = np.argsort(vertices_out_distal_new_up)
    cusp_out_distal = vertices_out_distal_new[cusps_out_distal_index_sorted[0]]

    return [cusp_in_mesial, cusp_in_distal, cusp_out_mesial, cusp_out_distal]  # , pts


def get_cusp_posterior(is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    if (is_upper == True):
        if (label in [3, 4, 11, 12]):
            # premolar
            is_awal = True if label in [3, 4] else False
            return get_cusp_posterior_first_second_upper(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)
        elif (label in [1, 2, 13, 14]):
            # molar
            is_awal = True if label in [1, 2] else False
            return get_cusp_posterior_third_fourth_upper(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)

    elif (is_upper == False):
        #  first premolar
        if (label in [4, 11]):
            is_awal = True if label == 4 else False
            return get_cusp_posterior_first_premolar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)
        #  second premolar
        elif (label in [3, 12]):
            is_awal = True if label == 3 else False
            return get_cusp_posterior_second_premolar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)
        #  first molar
        elif (label in [2, 13]):
            is_awal = True if label == 2 else False
            return get_cusp_posterior_first_molar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)
        #  second molar
        elif (label in [1, 14]):
            is_awal = True if label == 1 else False
            return get_cusp_posterior_second_molar_lower(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth)


def get_cusp_posterior_backup(is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    n_cusp = 2

    if (is_upper == True and label in [1, 2, 13, 14]):
        n_cusp = 4
    elif (is_upper == False):
        if (label in [1, 14]):
            n_cusp = 4
        elif (label in [2, 13]):
            n_cusp = 5
        elif (label in [3, 12]):
            n_cusp = 3
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    crcl = np.where(
        temp_u < center_u + 0.5
        # (temp_r>center_r-1) & (temp_r<center_r+1) &
        # (temp_f>center_f-3) & (temp_f<center_f+3)
    )
    pts = []
    for i in crcl[0]:
        pts.append(Point(vertices_tooth[i], c="violet"))
    vertices_new = vertices_tooth[crcl[0]]
    km = KMeans(n_clusters=n_cusp, init='random', algorithm='full')
    km.fit(vertices_new)

    centroid = km.cluster_centers_

    for c in centroid:
        pts.append(Point(c, c="orange7"))

    rs = [[] for i in range(n_cusp)]
    for j in range(len(vertices_new)):
        pred = km.predict([vertices_new[j]])
        # print(pred)
        rs[pred[0]].append(vertices_new[j])

    result_cusps = []
    for cluster in rs:
        cluster_trans = np.transpose(cluster)
        temp_u = np.matmul(upward_downward, cluster_trans)
        cusps_index_sorted = np.argsort(temp_u)
        cusp = cluster[cusps_index_sorted[0]]
        result_cusps.append(cusp)
    # cusps=[]
    # for v in vertices_new:
    #     biru = np.dot(v,upward_downward)
    #     hijau = np.dot(v,forward_backward)
    #     cusps.append(np.mean([biru*0.8,hijau*0.2]))
    # cusps_index_sorted = np.argsort(cusps)
    # cusp = vertices_new[cusps_index_sorted[0]]
    return result_cusps, pts


def get_pit(eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    # center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    # temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    crcl = np.where(
        (temp_r > center_r - 1) & (temp_r < center_r + 1) &
        (temp_f > center_f - 1) & (temp_f < center_f + 1)
    )
    # pts=[]
    # for i in crcl[0]:
    #     pts.append(i)
    #     pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[crcl[0]]
    temp_uu = np.matmul(upward_downward * -1, np.transpose(vertices_new))
    grooves_index_sorted = np.argsort(temp_uu)
    groove = vertices_new[grooves_index_sorted[0]]
    return groove  # ,pts


if __name__ == "__main__":
    filepath = 'D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segment/BA LowerJawScan_d_predicted_refined.vtp'
    mesh = load(filepath)
    ratio = 1000 / mesh.NCells()
    print(mesh.NCells())
    N = mesh.NCells()
    points = vtk2numpy(mesh.polydata().GetPoints().GetData())  # vertices (coordinate)
    ids = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:, 1:]  # faces (list of index of vertices)

    # pt_chosen_mesh, pt_neigh, idx_pt_chosen_mesh, idx_pt_neigh = points_neighbor_from_selected_face(points, ids,2001)
    # additional_mesh = _Debug_points_neighbor_from_selected_face(pt_chosen_mesh, pt_neigh)

    pt_chosen_mesh, pt_neigh, idx_pt_neigh = nl.points_neighbor_from_selected_points(points, ids, 2001)
    additional_mesh = nl._Debug_points_neighbor_from_selected_points(pt_chosen_mesh, pt_neigh)

    # pt_chosen_mesh, pt_neigh, idx_pt_neigh = faces_neighbor_from_selected_face(ids,2001)
    # additional_mesh = _DEBUG_faces_neighbor_from_selected_face(points, pt_chosen_mesh, pt_neigh)

    # pt_chosen_mesh, pt_neigh, idx_pt_neigh = faces_side_from_selected_face(ids,2001)
    # additional_mesh = _DEBUG_faces_side_from_selected_face(points, pt_chosen_mesh, pt_neigh)
    eigen_val, eigen_vec = getEigen(points, ids)
    draw_ei = draw_eigen_vec(eigen_vec, mesh.centerOfMass())
    show(mesh,
         additional_mesh,
         draw_ei,
         #  spline,
         axes=1)