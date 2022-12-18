from vedo import *
import numpy as np
import math

def points_neighbor_from_selected_face(
    mesh_all_points, mesh_all_faces_vert_list,
    index_face, merge_neighbor_with_selected=False):
    """
    return points of selected mesh, 
           points of neighbor of selected mesh,
           index of points of selected mesh, 
           index of points of neighbor of selected mesh
    """
    chosen_face = mesh_all_faces_vert_list[index_face]
    points_of_chosen_face = mesh_all_points[chosen_face]
    index_of_points_of_chosen_face = np.argwhere(np.isin(mesh_all_points, points_of_chosen_face).all(axis=1))[:,0]
    index_neighbor_faces = np.argwhere(np.isin(mesh_all_faces_vert_list,chosen_face).any(axis=1))[:,0]
    index_points_of_neighbor_faces = np.unique(mesh_all_faces_vert_list[index_neighbor_faces])
    if merge_neighbor_with_selected == False:
        index_points_of_neighbor_faces=index_points_of_neighbor_faces[np.where(np.isin(index_points_of_neighbor_faces, chosen_face, invert=True))[0]]
    return points_of_chosen_face, mesh_all_points[index_points_of_neighbor_faces], index_of_points_of_chosen_face, index_points_of_neighbor_faces

def _Debug_points_neighbor_from_selected_face(points_of_chosen_face, points_of_neighbor_faces):
    additional_mesh=[]
    for pc in points_of_chosen_face:
        temp = Point(pc,r=12,c="grey")
        additional_mesh.append(temp)
    for pc in points_of_neighbor_faces:
        temp = Point(pc,r=12,c="black")
        additional_mesh.append(temp)
    return additional_mesh

def faces_neighbor_from_selected_points(
    mesh_all_points, mesh_all_faces_vert_list,
    index_point):
    """
    return selected point, 
           neighbor faces of selected point (indexes), 
           index of couples of points beside index of selected point
    """
    chosen_point = mesh_all_points[index_point]
    faces_contain_selected_point = np.argwhere(np.isin(mesh_all_faces_vert_list,index_point).any(axis=1))
    index_of_neighbor_faces_of_selected_point = mesh_all_faces_vert_list[faces_contain_selected_point]
    index_of_neighbor_faces_of_selected_point = np.reshape(index_of_neighbor_faces_of_selected_point, (len(index_of_neighbor_faces_of_selected_point),3))
    couple_points_beside_selected = np.argwhere(index_of_neighbor_faces_of_selected_point!=index_point)
    couple_points_beside_selected = np.reshape(couple_points_beside_selected[:,1], (math.floor(len(couple_points_beside_selected[:])/2),2))
    return chosen_point, index_of_neighbor_faces_of_selected_point, couple_points_beside_selected
    
def points_neighbor_from_selected_points(
    mesh_all_points, mesh_all_faces_vert_list,
    index_point, merge_neighbor_with_selected=False): 
    """
    return selected point, 
           neighbor points of selected point, 
           index of neighbor points of selected point
    """
    chosen_point = mesh_all_points[index_point]
    faces_contain_selected_point = np.argwhere(np.isin(mesh_all_faces_vert_list,index_point).any(axis=1))
    index_of_neighbor_faces_of_selected_point = mesh_all_faces_vert_list[faces_contain_selected_point]
    index_of_neighbor_faces_of_selected_point = np.unique(index_of_neighbor_faces_of_selected_point)
    if merge_neighbor_with_selected == False:
        index_of_index_point = np.where(index_of_neighbor_faces_of_selected_point== index_point)[0][0]
        index_of_neighbor_faces_of_selected_point = np.delete(index_of_neighbor_faces_of_selected_point, index_of_index_point,axis=0)
    return chosen_point, mesh_all_points[index_of_neighbor_faces_of_selected_point], index_of_neighbor_faces_of_selected_point

def _Debug_points_neighbor_from_selected_points(chosen_point, points_of_neighbor_selected_point):
    additional_mesh=[]
    temp = Point(chosen_point,r=12,c="grey")
    additional_mesh.append(temp)
    for pc in points_of_neighbor_selected_point:
        temp = Point(pc,r=12,c="black")
        additional_mesh.append(temp)
    return additional_mesh

def faces_neighbor_from_selected_face(
    mesh_all_faces_vert_list,
    index_face, merge_neighbor_with_selected=False): 
    """
    return selected face, 
           neighbor faces of selected face, 
           index neighbor faces of selected face,
           
    """
    chosen_face = mesh_all_faces_vert_list[index_face]
    print("chosen_face",chosen_face)
    index_of_neighbor_faces = np.argwhere(np.isin(mesh_all_faces_vert_list,chosen_face).any(axis=1))[:,0]
    print("index_of_neighbor_faces", index_of_neighbor_faces)
    if merge_neighbor_with_selected == False:
        index_of_neighbor_faces = index_of_neighbor_faces[np.where(np.isin(index_of_neighbor_faces, index_face, invert=True))[0]]
    print("index_of_neighbor_faces", index_of_neighbor_faces)
        
    return chosen_face, mesh_all_faces_vert_list[index_of_neighbor_faces], index_of_neighbor_faces

def _DEBUG_faces_neighbor_from_selected_face(mesh_all_points, chosen_face, neighbor_faces):
    additional_mesh=[]
    temp = Mesh([mesh_all_points,[chosen_face]],c="grey")
    additional_mesh.append(temp)
    for nb in neighbor_faces:
        temp = Mesh([mesh_all_points,[nb]],c="black")
        additional_mesh.append(temp)
    return additional_mesh


def faces_side_from_selected_face(
    mesh_all_faces_vert_list,
    index_face, merge_neighbor_with_selected=False): 
    """
    return selected face, 
           neighbor faces of selected face, 
           index neighbor faces of selected face,
           
    """
    chosen_face = mesh_all_faces_vert_list[index_face]
    index_of_neighbor_face = np.where(np.isin(mesh_all_faces_vert_list,chosen_face))
    print("index_of_neighbor_face", index_of_neighbor_face)
    unique, counts = np.unique(index_of_neighbor_face[0], return_counts=True)
    print("u/c",unique, counts)
    c=[]
    if(merge_neighbor_with_selected==True):
        c = np.where((counts==2) | (counts==3))
    else:
        c = np.where(counts==2)
    index_of_neighbor_face=unique[c[0]]
    print("index_of_neighbor_face",index_of_neighbor_face)
        
    return chosen_face, mesh_all_faces_vert_list[index_of_neighbor_face], index_of_neighbor_face

def _DEBUG_faces_side_from_selected_face(mesh_all_points, chosen_face, neighbor_faces):
    additional_mesh=[]
    temp = Mesh([mesh_all_points,[chosen_face]],c="grey")
    additional_mesh.append(temp)
    for nb in neighbor_faces:
        temp = Mesh([mesh_all_points,[nb]],c="black")
        additional_mesh.append(temp)
    return additional_mesh


def calc_angle(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    angle = math.degrees(angle)
    return angle

def get_boundary_mesh(mesh, faces):
    N = mesh.NCells()
    points = vtk2numpy(mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
    # idx_faces = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
    faces_unique = np.unique(faces)
    # s_p = []
    i_s_p = []
    for i in faces_unique:
        index_selected_point = i
        chosen_point, index_of_neighbor_faces_of_selected_point, couple_points_beside_selected = faces_neighbor_from_selected_points(points,faces, index_selected_point)
        total_angle = 0
        for i in range(len(index_of_neighbor_faces_of_selected_point)):
            p_a = index_of_neighbor_faces_of_selected_point[i][couple_points_beside_selected[i][0]]
            p_b = index_of_neighbor_faces_of_selected_point[i][couple_points_beside_selected[i][1]]
            p_a = points[p_a]-points[index_selected_point]
            p_b = points[p_b]-points[index_selected_point]
            angle = calc_angle(p_a,p_b)
            total_angle+=angle
        if(total_angle<360):
            # s_p.append(points[index_selected_point])
            i_s_p.append(index_selected_point)
    return i_s_p

def get_bottom(points, idx_faces):
    # N = mesh.NCells()
    # points = vtk2numpy(mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
    # idx_faces = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
    s_p = []

    kk = math.floor(len(points)/2)
    mm = math.floor(len(points)/4)
    for p in range(kk-mm, kk):
    # for p in range(len(points)):
        index_selected_point = p
        chosen_point, index_of_neighbor_faces_of_selected_point, couple_points_beside_selected = faces_neighbor_from_selected_points(points,idx_faces, index_selected_point)
        total_angle = 0
        for i in range(len(index_of_neighbor_faces_of_selected_point)):
            p_a = index_of_neighbor_faces_of_selected_point[i][couple_points_beside_selected[i][0]]
            p_b = index_of_neighbor_faces_of_selected_point[i][couple_points_beside_selected[i][1]]
            p_a = points[p_a]-points[index_selected_point]
            p_b = points[p_b]-points[index_selected_point]
            angle = calc_angle(p_a,p_b)
            total_angle+=angle
        if(total_angle<=180):
            s_p.append(points[index_selected_point])
        
    m_s_p = np.mean(s_p, axis=0)        
    return m_s_p

def extract_labels(mesh):
        temp_obj_info = {}
        N = mesh.NCells()
        labels = np.unique(mesh.celldata['Label'])
        points = vtk2numpy(mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
        ids = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
        # cells = points[ids].reshape(N, 9).astype(dtype='float32')
        centers = []
        label_names = []
        temp_obj_info['labels']={}
        for label in labels:
            cells_label_index = np.where(mesh.celldata['Label'] == label)
            cells_label = ids[cells_label_index]
            points_index = np.unique(cells_label)
            points_label = points[points_index]
            points_tooth = points[cells_label]
            vtk_label = Mesh([points_label, cells_label]) # tooth, gingiva
            center_label = vtk_label.centerOfMass()
            # if label != 0.:
            centers.append(center_label)
            label_names.append(label)
            temp_obj_info['labels'][label]={}
            temp_obj_info['labels'][label]['vtk']=vtk_label
            temp_obj_info['labels'][label]['center']=center_label
            temp_obj_info['labels'][label]['vertices']=points_label
            temp_obj_info['labels'][label]['cells']=cells_label
            temp_obj_info['labels'][label]['vertices_cell']=points_tooth
        temp_obj_info['centers']=centers
        temp_obj_info['label_names']=label_names
        return temp_obj_info


def draw_eigen_vec(eigen_vec, center):
    left_right = eigen_vec[0]
    forward_backward = eigen_vec[1]
    upward_downward = eigen_vec[2]
    line_lr = Line(center-left_right, center+left_right, c="red")
    line_fb = Line(center-forward_backward, center+forward_backward, c="green")
    line_ud = Line(center-upward_downward, center+upward_downward, c="blue")
    point_lr = Point((center-left_right), c="red", r=15)
    point_fb = Point((center-forward_backward), c="green", r=15)
    point_ud = Point((center-upward_downward), c="blue", r=15)
    point_lr2 = Point((center+left_right), c="pink", r=15)
    point_fb2 = Point((center+forward_backward), c="yellow", r=15)
    point_ud2 = Point((center+upward_downward), c="violet", r=15)
    return [line_lr, line_fb, line_ud, point_fb, point_fb2, point_lr, point_lr2, point_ud, point_ud2]


def getEigen(points,idx_faces):
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
    eig_vec =  eig_vec[arrindx[::-1]]
    # print(eig_val)
    # print(eig_vec)
    # if rahang==True:
    # ============================================
    
    # Fixing position Eigen vector
    p_bottom_indicator = get_bottom(points,np.array(idx_faces))
    # depan belakang
    ori_fb = np.dot(p_bottom_indicator,eig_vec[1])
    inv_fb = np.dot(p_bottom_indicator,eig_vec[1]*-1)
    # TODO CHECK THE DISTANCE WITH INCISOR 1ST LEFT AND RIGHT TEETH WITH LABEL 7 AND 8 INSTEAD
    if(ori_fb>inv_fb):
        eig_vec[1] *=-1   
    # atas bawah
    temp_eig_up_down = eig_vec[2] * -1
    if(
        np.dot(eig_vec[2], p_bottom_indicator) < np.dot(temp_eig_up_down, p_bottom_indicator)
    ):
        eig_vec[2] *=-1
    # kanan kiri
    # THIS IS NOT ROBUST. 
    # TODO CHECK THE DISTANCE WITH MOLAR TOOTH WITH LABEL 1 OR 2 INSTEAD
    det_eig = np.linalg.det([eig_vec[0], eig_vec[1], eig_vec[2]])
    if(det_eig==1):
        eig_vec[0] *=-1

    # left_right = eig_vec[0]
    # forward_backward = eig_vec[1]
    # upward_downward = eig_vec[2]
    return eig_val, eig_vec

def get_index_point_from_mesh_vertices(point, points):
    return np.argwhere(np.isin(points, point).all(axis=1))[0][0]

def get_buccal_or_labial_andlingual_or_palatal_anterior(eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    pts=[]
    # rr = np.where(temp_r>center_r-0.75)
    # ll = np.where(temp_r<center_r+0.75)
    # uu = np.where(temp_u>center_u-0.75)
    # dd = np.where(temp_u<center_u+0.75)
    # rrll = np.intersect1d(np.intersect1d(rr[0],ll[0]),np.intersect1d(uu[0],dd[0]))
    cntr = np.where((temp_r>center_r-0.75) & (temp_r<center_r+0.75) & (temp_u>center_u-0.75) &(temp_u<center_u+0.75))
    print("cntr",cntr)
    cntr=cntr[0]
    for i in cntr: 
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]
    
    ins_outs = [] #lingual or palatal and buccal or labial
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        merah = np.dot(v, left_right )
        pink = np.dot(v, left_right  * -1)
        ins_outs.append(np.mean([hijau,pink,merah]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal =vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal, pts

def get_buccal_or_labial_andlingual_or_palatal_canine(is_awal,eigen_vec_mesh, center_tooth, vertices_tooth):
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
    pts=[]
    if is_awal==True:
        inv=-1
        cntr = np.where(
            (temp_r>center_r-2) & (temp_r<center_r+2.3) & 
            (temp_u>center_u-1.5) &(temp_u<center_u+1.5) &
            (temp_f>center_f-2.1) &(temp_f<center_f+2) 
        )
    else:
        inv=1
        cntr = np.where(
            (temp_r>center_r-2.3) & (temp_r<center_r+2) & 
            (temp_u>center_u-1.5) &(temp_u<center_u+1.5) &
            (temp_f>center_f-2) &(temp_f<center_f+2.1) 
        )
    print("cntr",cntr)
    cntr=cntr[0]
    for i in cntr: 
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]
    
    ins_outs = [] #lingual or palatal and buccal or labial
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right * inv) )
        pink = np.dot(v, (left_right * inv)  * -1)
        ins_outs.append(np.mean([biru*0.1,pink*0.3,merah*0.4, hijau*0.2]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal =vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal, pts

def get_buccal_or_labial_andlingual_or_palatal_premolar(is_awal,is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
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
    pts=[]
    if is_awal==True:
        inv=-1
        cntr = np.where(
            (temp_r>center_r-5) & (temp_r<center_r+4) & 
            (temp_u>center_u-1.5) &(temp_u<center_u+2) &
            (temp_f>center_f-2.5) &(temp_f<center_f+1.8) 
        )
    else:
        inv=1
        cntr = np.where(
            (temp_r>center_r-4) & (temp_r<center_r+5) & 
            (temp_u>center_u-2) &(temp_u<center_u+1.5) &
            (temp_f>center_f-1.8) &(temp_f<center_f+2.5) 
        )
    print("cntr",cntr)
    cntr=cntr[0]
    for i in cntr: 
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]
    
    ins_outs = [] #lingual or palatal and buccal or labial
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right * inv) )
        pink = np.dot(v, (left_right * inv)  * -1)
        ins_outs.append(np.mean([merah*0.6, hijau*0.4]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal =vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal, pts

def get_buccal_or_labial_andlingual_or_palatal_molar(is_awal,is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
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
    pts=[]
    if is_awal==True:
        inv=-1
        cntr = np.where(
            (temp_r>center_r-5) & (temp_r<center_r+4) & 
            (temp_u>center_u-1.5) &(temp_u<center_u+2) &
            (temp_f>center_f-2.5) &(temp_f<center_f+1.8) 
        )
    else:
        inv=1
        cntr = np.where(
            (temp_r>center_r-4) & (temp_r<center_r+5) & 
            (temp_u>center_u-2) &(temp_u<center_u+1.5) &
            (temp_f>center_f-1.8) &(temp_f<center_f+2.5) 
        )
    print("cntr",cntr)
    cntr=cntr[0]
    for i in cntr: 
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[cntr]
    
    ins_outs = [] #lingual or palatal and buccal or labial
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right * inv) )
        pink = np.dot(v, (left_right * inv)  * -1)
        ins_outs.append(np.mean([merah]))
    ins_outs_index_sorted = np.argsort(ins_outs)
    buccal_or_labial = vertices_new[ins_outs_index_sorted[0]]
    lingual_or_palatal =vertices_new[ins_outs_index_sorted[-1]]
    return buccal_or_labial, lingual_or_palatal, pts


def get_mesial_distal_anterior(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    # forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    
    most = np.argsort(temp_h)
    most_h = vertices_tooth[most[0]]
    pts=[]
    pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h) #temp[most[0]]+2.5
    for i in ww[0]:
        pts.append(Point(vertices_tooth[i],c="violet"))
        
    vertices_new = vertices_tooth[ww[0]]
    mesials=[]
    distals=[]
    
    inv = 1
    if(is_awal==False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        # hijau = np.dot(v,forward_backward)
        merah = np.dot(v, (left_right*inv) )
        pink = np.dot(v, (left_right *inv) * -1)
        mesials.append(np.mean([merah*0.7,biru*0.3]))
        distals.append(np.mean([pink*0.7,biru*0.3]))
        
        
    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal, pts

def get_mesial_distal_canine(is_awal, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    most = np.argsort(temp_h)
    most_h = vertices_tooth[most[0]]
    pts=[]
    pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h) #temp[most[0]]+2.5
    for i in ww[0]:
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials=[]
    distals=[]
    inv = 1
    if(is_awal==False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        hijau_muda = np.dot(v,forward_backward * -1)
        merah = np.dot(v, (left_right*inv) )
        pink = np.dot(v, (left_right *inv) * -1)
        mesials.append(np.mean([merah*0.4,biru*0.1,hijau*0.5]))
        distals.append(np.mean([pink*0.5,biru*0.25,hijau_muda*0.25]))
        
        
    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal, pts


def get_mesial_distal_premolar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    most = np.argsort(temp_h)
    most_h = vertices_tooth[most[0]]
    pts=[]
    pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h) #temp[most[0]]+2.5
    for i in ww[0]:
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials=[]
    distals=[]
    inv = 1
    if(is_awal==False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        hijau_muda = np.dot(v,forward_backward * -1)
        merah = np.dot(v, (left_right*inv) )
        pink = np.dot(v, (left_right *inv) * -1)
        mesials.append(np.mean([pink*0.2,biru*0.15,hijau*0.45, merah*0.2]))
        if(is_upper==False and (label == 3 or label == 12)):
            distals.append(np.mean([pink*0.5,hijau_muda*0.5]))
        else:
            distals.append(np.mean([pink*0.4,biru*0.1,hijau_muda*0.5]))
        
        
    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal, pts

def get_mesial_distal_molar(is_awal, is_upper, label, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    center_h = np.dot(center_tooth, upward_downward)
    most_h =0
    vertices_tooth_trans = np.transpose(vertices_tooth)
    temp_h = np.matmul(upward_downward, vertices_tooth_trans)
    most = np.argsort(temp_h)
    most_h = vertices_tooth[most[0]]
    pts=[]
    pts.append(Point(most_h, c="white"))
    ww = np.where(temp_h < center_h) #temp[most[0]]+2.5
    for i in ww[0]:
        pts.append(Point(vertices_tooth[i],c="violet"))
    vertices_new = vertices_tooth[ww[0]]
    mesials=[]
    distals=[]
    inv = 1
    if(is_awal==False):
        inv = -1
    for v in vertices_new:
        biru = np.dot(v,upward_downward)
        hijau = np.dot(v,forward_backward)
        hijau_muda = np.dot(v,forward_backward * -1)
        merah = np.dot(v, (left_right*inv) )
        pink = np.dot(v, (left_right *inv) * -1)
        mesials.append(np.mean([pink*0.2,biru*0.15,hijau*0.45, merah*0.2]))
        if(is_upper==False and (label == 2 or label == 13)):
            distals.append(np.mean([pink*0.5,hijau_muda*0.5]))
        else:
            distals.append(np.mean([pink*0.4,biru*0.1,hijau_muda*0.5]))
        
        
    mesials_index_sorted = np.argsort(mesials)
    mesial = vertices_new[mesials_index_sorted[0]]
    distals_index_sorted = np.argsort(distals)
    distal = vertices_new[distals_index_sorted[0]]
    return mesial, distal, pts
    
    
if __name__ == "__main__":
    filepath = 'D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segment/BA LowerJawScan_d_predicted_refined.vtp'
    mesh = load(filepath)
    ratio = 1000/mesh.NCells()
    print(mesh.NCells())
    N = mesh.NCells()
    points = vtk2numpy(mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
    ids = vtk2numpy(mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
    
    
    # pt_chosen_mesh, pt_neigh, idx_pt_chosen_mesh, idx_pt_neigh = points_neighbor_from_selected_face(points, ids,2001)
    # additional_mesh = _Debug_points_neighbor_from_selected_face(pt_chosen_mesh, pt_neigh)
    
    pt_chosen_mesh, pt_neigh, idx_pt_neigh = points_neighbor_from_selected_points(points, ids,2001)
    additional_mesh = _Debug_points_neighbor_from_selected_points(pt_chosen_mesh, pt_neigh)
    
    # pt_chosen_mesh, pt_neigh, idx_pt_neigh = faces_neighbor_from_selected_face(ids,2001)
    # additional_mesh = _DEBUG_faces_neighbor_from_selected_face(points, pt_chosen_mesh, pt_neigh)
    
    # pt_chosen_mesh, pt_neigh, idx_pt_neigh = faces_side_from_selected_face(ids,2001)
    # additional_mesh = _DEBUG_faces_side_from_selected_face(points, pt_chosen_mesh, pt_neigh)
    
    show(mesh,
        additional_mesh,
        #  spline,
        axes=1)
# [[ 15.089668   -11.621852     4.6010957 ]
#  [ 15.019489    -8.277051    -1.2631611 ]
#  [ 32.302654   -12.522393   -10.0969095 ]
#  [ 13.386324   -15.421863     8.875461  ]
#  [ 18.656666    -7.315266    -3.7007804 ]
#  [ 19.26639     -7.5142136   -3.7282462 ]
#  [ 23.085783    -7.664467    -5.3215694 ]
#  [ 23.059458    -8.329133    -5.7040806 ]
#  [ 16.53377     -9.251474     4.728519  ]
#  [ 15.081059    -8.414474     3.368339  ]
#  [ 15.825705   -10.133887     5.728507  ]
#  [ 14.758792    -5.9779077    1.5147805 ]
#  [ 20.399256    -7.313439    -3.2227652 ]
#  [ 25.055988    -9.994181    -5.7068825 ]
#  [ 15.981918    -5.955047     0.32978007]
#  [ 18.536192    -7.6274977   -1.6300938 ]]