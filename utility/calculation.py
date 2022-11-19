import numpy as np
import enum

def find_distance_between_two_points(pt1,pt2):
    return np.linalg.norm(pt1 - pt2)

def find_closest_point_between_a_point_and_a_line(pt, pts_line):
    d = (pts_line[0] - pts_line[1]) / np.linalg.norm(pts_line[0] - pts_line[1])
    v = pt - pts_line[1]
    t = np.dot(v,d)
    P = pts_line[1] + t * d
    return P

def find_distance_between_a_point_and_a_line(pt, pts_line):
    return np.linalg.norm(np.cross(pts_line[0] - pts_line[1], pts_line[1] - pt))/np.linalg.norm(pts_line[0] - pts_line[1])

def find_distance_between_a_point_and_a_3pts_plane(pt, plane_pts):
    n = np.cross(plane_pts[0]-plane_pts[1],plane_pts[2]-plane_pts[1])
    n = n/np.linalg.norm(n)
    dist = abs(np.dot(pt - plane_pts[1],n))
    return dist

def find_closest_point_between_a_point_and_a_3pts_plane(pt, plane_pts):
    u = plane_pts[1] - plane_pts[0]
    print("pts u",u)
    v = plane_pts[2] - plane_pts[0]
    print("pts v",v)
    # vector normal to plane
    n = np.cross(u, v)
    print("n cross",n)
    print("n norm",np.linalg.norm(n))
    n = n / np.linalg.norm(n)
    print("n bagi b norm",n)
    p_ = pt - plane_pts[0]
    print("p_",p_)
    dist_to_plane = np.dot(p_, n)
    print("dist_to_plane",dist_to_plane)
    p_normal = np.dot(p_, n) * n
    print("p_normal",p_normal)
    p_tangent = p_ - p_normal
    print("p_tangent",p_tangent)
    

    closest_point = p_tangent + plane_pts[0]
    print("closest_point",closest_point)
    
    # coords = np.linalg.lstsq(np.column_stack((u, v)), p_tangent)[0]
    # print("coords all",np.linalg.lstsq(np.column_stack((u, v)), p_tangent))
    # print("coords",coords)
    
    return closest_point


def find_new_point_in_a_line_with_new_distance(pt1_anchor, pt2, new_distance):
    v=pt2-pt1_anchor
    vv=np.linalg.norm(v)
    u=v/vv
    dd=vv-(vv-new_distance)
    return np.array(pt1_anchor)+(dd*u)

def find_new_point_in_a_line_with_delta_distance(pt1_anchor, pt2, delta_distance):
    v=pt2-pt1_anchor
    vv=np.linalg.norm(v)
    u=v/vv
    dd=vv+(delta_distance)
    return np.array(pt1_anchor)+(dd*u)

class FaceTypeConversion(enum.Enum):
    RIGHT = 0,
    FRONT=1,
    UP=2,
    LEFT=3,
    BACK=4,
    DOWN=5

def convert_to_2d(face_type, eigen_vec, points):
    left_right = eigen_vec[0]
    forward_backward = eigen_vec[1]
    upward_downward = eigen_vec[2]
    pts_transpose = np.transpose(points)
    if(face_type==FaceTypeConversion.RIGHT.value):
        temp = np.matmul(np.array([[0,0,0],forward_backward,upward_downward]), pts_transpose)
    elif(face_type==FaceTypeConversion.FRONT.value):
        temp = np.matmul(np.array([left_right,[0,0,0],upward_downward]), pts_transpose)
    elif(face_type==FaceTypeConversion.UP.value):
        temp = np.matmul(np.array([left_right,forward_backward,[0,0,0]]), pts_transpose)
    elif(face_type==FaceTypeConversion.LEFT.value):
        temp = np.matmul(np.array([[0,0,0],forward_backward,upward_downward]), pts_transpose)
    elif(face_type==FaceTypeConversion.BACK.value):
        temp = np.matmul(np.array([left_right,[0,0,0],upward_downward]), pts_transpose)
    elif(face_type==FaceTypeConversion.DOWN.value):
        temp = np.matmul(np.array([left_right,forward_backward,[0,0,0]]), pts_transpose)
    return np.transpose(temp)

def get_eigen_flat(points):
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
    return eig_val, eig_vec

if __name__ == '__main__':
    a = np.array([1,0])
    b = np.array([5,0])
    dst = 1.2
    p = np.array([4,1])
    print(find_distance_between_two_points(a,b))
    c = find_new_point_in_a_line_with_delta_distance(a,b,dst)
    print(c)
    print(find_distance_between_two_points(a,c))
    d=find_closest_point_between_a_point_and_a_line(a,[b,c])
    print("d",d)
    e = find_distance_between_a_point_and_a_line(c,(a,b))
    print("e",e)