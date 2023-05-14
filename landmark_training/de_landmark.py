import numpy as np
from vedo import load
import utility.landmarking_lib as ll
from constant.enums import ToothType, LandmarkType, ArchType, LandmarkDefinition
from landmark_training.landmark_helper import get_candidate_points, get_point_landmark_normalized
from landmark_training.param_landmark_area import candidate_definition
import time
import pandas as pd
import math

from utility.calculation import find_distance_between_two_points
import csv

def load_ld(filename, tooth_type, landmark_type):
    df = pd.read_csv(filename, index_col=0)
    row =  df[(df['label']==tooth_type) & (df['landmark'] == landmark_type)]
    print(row)
    coor = np.ndarray.flatten(np.array([row['x'], row['y'], row['z']]))
    print(coor)
    return coor

    # index_in_models = Arch._get_index_arch_type(typearch)
    arch = model
    for index, row in df.iterrows():
        print(row)
        tooth = arch.teeth[int(row['label'])]
        tooth.landmark_pt[int(row['landmark'])] = np.array([row['x'], row['y'], row['z']])

def extract_vtp(mesh, label):
    center_mesh = mesh.centerOfMass()
    points_mesh = np.array(mesh.points())
    idx_faces_mesh = np.array(mesh.cells())
    points_mesh_normalized = points_mesh - center_mesh
    incisor_teeth = [
        ToothType.INCISOR_UL2_LR2.value,
        ToothType.INCISOR_UL1_LR1.value,
        ToothType.INCISOR_UR1_LL1.value,
        ToothType.INCISOR_UR2_LL2.value
    ]
    eigen_val_mesh, eigen_vec_mesh = ll.getEigen(points_mesh_normalized, idx_faces_mesh, mesh.celldata['Label'],
                                                 incisor_teeth)
    cells_tooth_index = np.where(mesh.celldata['Label'] == label)
    label = math.floor(label)
    cells_tooth = idx_faces_mesh[cells_tooth_index]
    points_tooth_index = np.unique(cells_tooth)
    points_tooth = points_mesh[points_tooth_index]
    points_tooth_normalized = points_mesh_normalized[points_tooth_index]
    center_tooth = np.mean(points_tooth, axis=0)
    center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)

    return eigen_vec_mesh, points_tooth, points_tooth_normalized, center_tooth_normalized


def mutation_best(xb, x, F): #DE/best/1
    return xb + F * (x[0] - x[1])


def crossover(mutated, target, dims, cr):
    # generate a uniform random value for every dimension
    p = np.random.rand(dims)
    # generate trial vector by binomial crossover
    trial = np.array([mutated[i] if p[i] < cr else target[i] for i in range(dims)])
    return trial


def check_bounds(mutated):
    return mutated/np.sum(mutated)


def get_landmark_point(parameter, arch_type, tooth_type, landmark_type, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth, vertices_tooth):
    # candidate_def = candidate_definition[arch_type][tooth_type][landmark_type]
    # vertices_tooth_new = get_candidate_points(candidate_def, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth)
    normalized_point = get_point_landmark_normalized(eigen_vec_mesh, norm_vertices_tooth, parameter)
    landmark_index = np.argwhere(np.isin(norm_vertices_tooth, normalized_point).all(axis=1))[0][0]
    return vertices_tooth[landmark_index]


def minimize_function(individu, mesh_data, arch_type, tooth_type, landmark_type):
    # root mean square error
    total_se = 0
    for data in mesh_data:
        current_point = get_landmark_point(individu, arch_type, tooth_type, landmark_type,
                                           data['eigen'],
                                           data['norm_center_tooth'],
                                           data['norm_vertices_tooth'],
                                           data['vertices_tooth'])
        error = find_distance_between_two_points(data['ground_truth'], current_point)
        se = math.pow(error, 2)
        total_se += se
    mse = total_se/len(mesh_data)
    rmse = math.sqrt(mse)
    return rmse

def de_optimization(data_meshes, pop_size, n_chromosome, iter, F, cr, arch_type, tooth_type, landmark_type):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = np.random.rand(pop_size, n_chromosome)
    for i in range(len(pop)):
        pop[i] = check_bounds(pop[i])

    obj_all = [ minimize_function(indv, data_meshes, arch_type, tooth_type, landmark_type) for indv in pop]
    # print(obj_all)

    # find the best performing vector of initial population
    best_vector = pop[np.argmin(obj_all)]
    best_obj = np.min(obj_all)
    prev_obj = best_obj
    # run iterations of the algorithm
    for i in range(iter):
        # print("iter", i)
        # iterate over all candidate solutions
        for j in range(pop_size):
            # choose three candidates, a, b and c, that are not the current one
            candidates = [candidate for candidate in range(pop_size) if candidate != j]
            a, b = pop[np.random.choice(candidates, 2, replace=False)]
            # perform mutation
            mutated = mutation_best(best_vector, [a, b], F)
            # check that lower and upper bounds are retained after mutation
            mutated = check_bounds(mutated)
            # perform crossover
            trial = crossover(mutated, pop[j], n_chromosome, cr)
            # check that lower and upper bounds are retained after trial
            trial = check_bounds(trial)

            # compute objective function value for target vector
            obj_target = minimize_function(pop[j], data_meshes, arch_type, tooth_type, landmark_type)
            # compute objective function value for trial vector
            obj_trial = minimize_function(trial, data_meshes, arch_type, tooth_type, landmark_type)
            # perform selection
            if obj_trial <= obj_target:
                # replace the target vector with the trial vector
                pop[j] = trial
                # store the new objective function value
                obj_all[j] = obj_trial
        # find the best performing vector at each iteration
        best_obj = np.min(obj_all)
        # store the lowest objective function value
        if best_obj < prev_obj:
            best_vector = pop[np.argmin(obj_all)]
            prev_obj = best_obj
            # report progress at each iteration
            print('Iteration: %d = %.5f' % (i, best_obj))
            # print('Iteration: %d f([%s]) = %.5f' % (i, np.around(best_vector, decimals=5), best_obj))
    return [best_vector, best_obj]

    # dilakukan de dan return models yang paling optimum
    # return de models yang paling optimum


def get_landmark_name(ld_val):
    for ld in LandmarkType:
        if ld.value == ld_val:
            return ld.name

def start_de_landmark():
    paths_upper=[
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_UPPER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._UPPER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_UPPER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_UPPER.vtp",
    ]
    paths_ld_upper = [
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_UPPER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._UPPER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_UPPER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_UPPER.csv",
    ]
    paths_lower = [
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_LOWER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._LOWER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_LOWER.vtp",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_LOWER.vtp",
    ]
    paths_ld_lower = [
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_LOWER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._LOWER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_LOWER.csv",
        "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_LOWER.csv",
    ]

    paths_upper = [
        "D:\\tesis\\fix\\1 MNF\\MNF_UPPER.vtp",
        "D:\\tesis\\fix\\4. SN\\SN._UPPER.vtp",
        "D:\\tesis\\fix\\7. GSF\\GSF_UPPER.vtp",
        "D:\\tesis\\fix\\8. UR\\UR_UPPER.vtp",
    ]
    paths_ld_upper = [
        "D:\\tesis\\fix\\1 MNF\\MNF_UPPER.csv",
        "D:\\tesis\\fix\\4. SN\\SN._UPPER.csv",
        "D:\\tesis\\fix\\7. GSF\\GSF_UPPER.csv",
        "D:\\tesis\\fix\\8. UR\\UR_UPPER.csv",
    ]
    paths_lower = [
        "D:\\tesis\\fix\\1 MNF\\MNF_LOWER.vtp",
        "D:\\tesis\\fix\\4. SN\\SN._LOWER.vtp",
        "D:\\tesis\\fix\\7. GSF\\GSF_LOWER.vtp",
        "D:\\tesis\\fix\\8. UR\\UR_LOWER.vtp",
    ]
    paths_ld_lower = [
        "D:\\tesis\\fix\\1 MNF\\MNF_LOWER.csv",
        "D:\\tesis\\fix\\4. SN\\SN._LOWER.csv",
        "D:\\tesis\\fix\\7. GSF\\GSF_LOWER.csv",
        "D:\\tesis\\fix\\8. UR\\UR_LOWER.csv",
    ]

    paths_upper.extend(paths_lower)
    paths_vtp = paths_upper[:]
    paths_ld_upper.extend(paths_ld_lower)
    paths_csv = paths_ld_upper[:]

    pop_size = 10
    n_chromosome = 6 # kanan kiri depan belakang atas bawah
    # left_right = eig_vec[0]
    # forward_backward = eig_vec[1]
    # upward_downward = eig_vec[2]

    # define number of iterations
    iter = 100
    # define scale factor for mutation
    F = 0.5
    # define crossover rate for recombination
    cr = 0.7

    ld_def = LandmarkDefinition().archs
    for archtype in ArchType:
        for toothtype in ToothType:
            # print(toothtype.value)
            if toothtype.value == toothtype.GINGIVA.value or toothtype.value == toothtype.DELETED.value:
                continue
            for ld in ld_def[archtype.value][toothtype.value]:
                # print("ld",ld)
                meshes_data = []
                for vtp_path, ld_path in (zip(paths_vtp, paths_csv)):
                    word = 'UPPER'
                    if archtype.value == ArchType.LOWER.value:
                        word = 'LOWER'
                    if word not in vtp_path:
                        continue
                    # print(vtp_path)
                    ground_truth = load_ld(ld_path, toothtype.value, ld)
                    eigen_vec_mesh, vertices_tooth, norm_vertices_tooth, norm_center_tooth = extract_vtp(load(vtp_path), toothtype.value)
                    meshes_data.append({
                        'eigen': eigen_vec_mesh,
                        'vertices_tooth': vertices_tooth,
                        'norm_vertices_tooth': norm_vertices_tooth,
                        'norm_center_tooth':norm_center_tooth,
                        'ground_truth': ground_truth
                    })
                seconds_start = time.time()
                solution = de_optimization(meshes_data, pop_size, n_chromosome, iter, F, cr, archtype.value, toothtype.value, ld)
                print("solution: ", archtype.name, toothtype.name, get_landmark_name(ld), solution[1], solution[0])
                seconds_finish = time.time()
                finish_time = (seconds_finish-seconds_start)
                print("waktu de opt", finish_time, "detik")
                f = open('ld_saved_de.csv', 'a+', encoding='utf-8', newline='')
                writer = csv.writer(f)
                coor = '|'.join([str(c) for c in solution[0]])
                writer.writerow([archtype.name, archtype.value, toothtype.name, toothtype.value, get_landmark_name(ld), ld, solution[1], coor, finish_time])
                f.close()

if __name__ == '__main__':
    start_de_landmark()