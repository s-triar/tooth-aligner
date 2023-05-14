import numpy as np
from landmark_training.param_landmark_area import candidate_definition
from landmark_training.param_landmark_position import landmark_definition
def get_array_compared(key, arr):
    if(key == 'u'):
        return arr[0]
    elif (key == 'd'):
        return arr[1]
    elif (key == 'r'):
        return arr[2]
    elif (key == 'l'):
        return arr[3]
    elif (key == 'f'):
        return arr[4]
    elif (key == 'b'):
        return arr[5]

def get_center_compared(key, centers):
    if (key == 'u'):
        return centers[0]
    elif (key == 'd'):
        return centers[1]
    elif (key == 'r'):
        return centers[2]
    elif (key == 'l'):
        return centers[3]
    elif (key == 'f'):
        return centers[4]
    elif (key == 'b'):
        return centers[5]

def get_candidate_points(candidate_def, eigen_vec_mesh, center_tooth, vertices_tooth):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    inv_left_right = eigen_vec_mesh[0]*-1
    inv_forward_backward = eigen_vec_mesh[1]*-1
    inv_upward_downward = eigen_vec_mesh[2]*-1

    vertices_tooth_trans = np.transpose(vertices_tooth)

    center_u = np.dot(center_tooth, upward_downward)
    center_r = np.dot(center_tooth, left_right)
    center_f = np.dot(center_tooth, forward_backward)
    center_d = np.dot(center_tooth, inv_upward_downward)
    center_l = np.dot(center_tooth, inv_left_right)
    center_b = np.dot(center_tooth, inv_forward_backward)

    temp_u = np.matmul(upward_downward, vertices_tooth_trans)
    temp_r = np.matmul(left_right, vertices_tooth_trans)
    temp_f = np.matmul(forward_backward, vertices_tooth_trans)
    temp_d = np.matmul(inv_upward_downward, vertices_tooth_trans)
    temp_l = np.matmul(inv_left_right, vertices_tooth_trans)
    temp_b = np.matmul(inv_forward_backward, vertices_tooth_trans)
    arr_comp = [temp_u, temp_d, temp_r, temp_l, temp_f, temp_b]
    centers_comp = [center_u, center_d, center_r, center_l, center_f, center_b]
    query = np.logical_and.reduce(
        [
            np.logical_and(np.where(isinstance(v[0], bool), v[0], get_array_compared(k, arr_comp) > get_center_compared(k, centers_comp)+v[0]),
                           np.where(isinstance(v[1], bool), v[1], get_array_compared(k, arr_comp) < get_center_compared(k, centers_comp)+v[1]))
            # ( v[0] if isinstance(v[0], bool) else (get_array_compared(k, arr_comp) > get_center_compared(k, centers_comp)+v[0])) &
            # (v[1] if isinstance(v[1], bool) else (get_array_compared(k, arr_comp) < get_center_compared(k, centers_comp)+v[1]))
            for k, v in candidate_def.items()
        ]
    )

    vertices_new = vertices_tooth[query]
    return vertices_new


def get_point_landmark_normalized(eigen_vec_mesh, vertices_tooth_new, parameter):
    left_right = eigen_vec_mesh[0]
    forward_backward = eigen_vec_mesh[1]
    upward_downward = eigen_vec_mesh[2]
    inv_left_right = eigen_vec_mesh[0] * -1
    inv_forward_backward = eigen_vec_mesh[1] * -1
    inv_upward_downward = eigen_vec_mesh[2] * -1

    vertices_tooth_trans = np.transpose(vertices_tooth_new)

    temp_r = np.matmul(left_right * parameter[0], vertices_tooth_trans)
    temp_l = np.matmul(inv_left_right * parameter[1], vertices_tooth_trans)
    temp_f = np.matmul(forward_backward * parameter[2], vertices_tooth_trans)
    temp_b = np.matmul(inv_forward_backward * parameter[3], vertices_tooth_trans)
    temp_u = np.matmul(upward_downward*parameter[4], vertices_tooth_trans)
    temp_d = np.matmul(inv_upward_downward*parameter[5], vertices_tooth_trans)

    stacked_array = np.column_stack((temp_u, temp_d, temp_r, temp_l, temp_f, temp_b))

    mean_per_row = np.mean(stacked_array, axis=1)
    min_mean_index = np.argsort(mean_per_row)[0]
    normalize_point = vertices_tooth_new[min_mean_index]

    return normalize_point


def get_landmark_point(arch_type, tooth_type, landmark_type, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth, vertices_tooth):
    candidate_def = candidate_definition[arch_type][tooth_type][landmark_type]
    vertices_tooth_new = get_candidate_points(candidate_def, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth)
    parameter = landmark_definition[arch_type][tooth_type][landmark_type]
    normalized_point = get_point_landmark_normalized(eigen_vec_mesh, vertices_tooth_new, parameter)
    landmark_index = np.argwhere(np.isin(norm_vertices_tooth, normalized_point).all(axis=1))[0][0]
    return vertices_tooth[landmark_index]