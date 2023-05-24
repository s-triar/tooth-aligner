import copy
import numpy as np
from vedo import Mesh

from constant.enums import ToothType, ArchType, LandmarkType
from optimization.optimization_helper5 import calculate_buccallabial_to_bonwill_line, calculate_cusp_to_flat_level_line, calculate_mesiodistal_balance_to_bonwill_line_from_side_view, calculate_mesiodistal_balance_to_bonwill_line_from_top_view, get_closest_possible_movements, get_closest_possible_rotations, get_closest_possible_rotations_and_movements
from utility.arch import Arch
from utility.arch_copy import ArchCopy
from utility.bolton_studi_model import Bolton
from utility.calculation import FaceTypeConversion, convert_to_2d, find_distance_between_two_points, getToothLabelSeberang, find_closest_point_between_a_point_and_a_line
from utility.pont_studi_model import Pont
from utility.korkhaus_studi_model import Korkhaus
from utility.carey_studi_model import Carey
import numpy as np
import math

from utility.splineku import SplineKu
import time
    
    
    
    
    # per gigi : val_roll, val_yaw, val_pitch, val_move_x, val_move_y, val_move_z
    
def de_rotation_and_moving(model, chrs):
    for i in ToothType:
        if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
            chr=chrs[(i.value-1)*6:((i.value-1)+1)*6]
            verts =  model.mesh.points()
            # print(model.teeth[i.value].index_vertice_cells, i.value)
            faces = model.teeth[i.value].index_vertice_cells
            mesh = Mesh([verts, faces])
            faces_unique = np.unique(faces)
            idx_bdr = mesh.boundaries(returnPointIds=True)
            idx_for_faces = []
            for b in idx_bdr:
                itemp = np.where(faces_unique == b)
                for jb in np.unique(itemp[0]):
                    idx_for_faces.append(jb)
            faces_unique = np.delete(faces_unique, idx_for_faces)
            teeth_center = model.teeth[i.value].center
            arch_orientation_vec = model.orientatin_vec
            # rotation
            # mesh.rotateX(chr[0], False, teeth_center)
            # model.update_teeth_point_rotation(i.value, "pitch", chr[0], teeth_center)
            mesh.rotate(chr[0], axis=arch_orientation_vec[0], point=teeth_center)
            model.update_teeth_point_rotation_quarrternion(i.value, "pitch", chr[0], teeth_center,arch_orientation_vec[0])
            # mesh.rotateY(chr[1], False, teeth_center)
            # model.update_teeth_point_rotation(i.value, "yaw", chr[1], teeth_center)
            mesh.rotate(chr[1], axis=arch_orientation_vec[1], point=teeth_center)
            model.update_teeth_point_rotation_quarrternion(i.value, "yaw", chr[1], teeth_center,arch_orientation_vec[1])
            # mesh.rotateZ(chr[2], False, teeth_center)
            # model.update_teeth_point_rotation(i.value, "roll", chr[2], teeth_center)
            mesh.rotate(chr[2], axis=arch_orientation_vec[2], point=teeth_center)
            model.update_teeth_point_rotation_quarrternion(i.value, "yaw", chr[2], teeth_center,arch_orientation_vec[2])
            # end rotation

            # movement
            val_direction=[chr[3],chr[4],chr[5]]
            mesh.points(mesh.points()+val_direction)

            # end moving

            temp_p = model.mesh.points()
            temp_p[faces_unique] = mesh.points()[faces_unique]
            model.mesh.points(temp_p)
            model.update_teeth_point_moving(i.value, val_direction)
    return model
        
def de_rotation_and_moving_tooth(tooth_type, model, chr):
    verts = model.mesh.points()
    # print(model.teeth[i.value].index_vertice_cells, i.value)
    faces = model.teeth[tooth_type].index_vertice_cells
    mesh = Mesh([verts, faces])
    faces_unique = np.unique(faces)
    idx_bdr = mesh.boundaries(returnPointIds=True)
    idx_for_faces = []
    for b in idx_bdr:
        itemp = np.where(faces_unique == b)
        for jb in np.unique(itemp[0]):
            idx_for_faces.append(jb)
    faces_unique = np.delete(faces_unique, idx_for_faces)
    teeth_center = model.teeth[tooth_type].center
    arch_orientation_vec = model.orientatin_vec
    # rotation
    # mesh.rotateX(chr[0], False, teeth_center)
    # model.update_teeth_point_rotation(tooth_type, "pitch", chr[0], teeth_center)
    mesh.rotate(chr[0], axis=arch_orientation_vec[0], point=teeth_center)
    model.update_teeth_point_rotation_quarrternion(tooth_type, "pitch", chr[0], teeth_center, arch_orientation_vec[0])
    # mesh.rotateY(chr[1], False, teeth_center)
    # model.update_teeth_point_rotation(tooth_type, "yaw", chr[1], teeth_center)
    mesh.rotate(chr[1], axis=arch_orientation_vec[1], point=teeth_center)
    model.update_teeth_point_rotation_quarrternion(tooth_type, "yaw", chr[1], teeth_center, arch_orientation_vec[1])
    # mesh.rotateZ(chr[2], False, teeth_center)
    # model.update_teeth_point_rotation(tooth_type, "roll", chr[2], teeth_center)
    mesh.rotate(chr[2], axis=arch_orientation_vec[2], point=teeth_center)
    model.update_teeth_point_rotation_quarrternion(tooth_type, "yaw", chr[2], teeth_center, arch_orientation_vec[2])
    # end rotation

    # movement
    val_direction = [chr[3], chr[4], chr[5]]
    mesh.points(mesh.points() + val_direction)

    # end moving

    temp_p = model.mesh.points()
    temp_p[faces_unique] = mesh.points()[faces_unique]
    model.mesh.points(temp_p)
    model.update_teeth_point_moving(tooth_type, val_direction)
    return model

# def get_rotation_teeth_status(models, summary_pts):
#     ArchCopy._clear()
#     total = 0
#     posterior = [
#         ToothType.MOLAR_UL7_LR7.value,
#         ToothType.MOLAR_UL6_LR6.value,
#         ToothType.PREMOLAR_UL5_LR5.value,
#         ToothType.PREMOLAR_UL4_LR4.value,
#         ToothType.PREMOLAR_UR4_LL4.value,
#         ToothType.PREMOLAR_UR5_LL5.value,
#         ToothType.MOLAR_UR6_LL6.value,
#         ToothType.MOLAR_UR7_LL7.value
#     ]
#     for m in models:
#         eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
#         model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
#         summary_line = SplineKu(summary_pts[model_cp.arch_type][1], degree=2, smooth=0, res=600)
#         teeth = copy.deepcopy(model_cp.teeth)
#         center_arch = model_cp.mesh.centerOfMass()
#         center_normalize = np.array([0.0,0.0,0.0])
#         summary_line_normalize = SplineKu(summary_pts[model_cp.arch_type][1]-center_arch, degree=2, smooth=0, res=600)
#         for i in ToothType:        
#             if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
#                 distal=teeth[i.value].landmark_pt[LandmarkType.DISTAL.value]
#                 mesial=teeth[i.value].landmark_pt[LandmarkType.MESIAL.value]
#                 center_arch_used = center_arch[:]
                
#                 if(i.value in posterior):
#                     center_arch_used = find_closest_point_between_a_point_and_a_line(center_arch_used,)
                
#                 distal_normalize = distal - center_arch_used
#                 mesial_normalize = mesial - center_arch_used
                
#                 hitpspln, hitpln = summary_line_normalize.closestPointToAline([center_normalize, distal_normalize], isAwal=(i.value <=7))
#     ArchCopy._clear()


def get_new_model(models,chromosome):
    models_cp = []
    ArchCopy._clear()
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        
        models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
    for i in range(len(models_cp)):
        models_cp[i] = de_rotation_and_moving(models_cp[i], chromosome[(i*(14*6)):(i+1)*(14*6)]) # 6 chromosome per tooth
    ArchCopy._clear()
    return models_cp



def minimize_function_using_delta_current_to_the_first_studi_model_calculation2( arch_type, tooth_type, models, chromosome, flat_pts, summary_pts, Bs, line_centers,  As, destination_tooth):

    i=0
    ArchCopy._clear()
    tempGen = []
    index = Arch._get_index_arch_type(arch_type)
    m = models[index]

    eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
    model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))

    error_arch = []

    tot_error_top_view = 0
    tot_error_side_view = 0

    tot_error_top_view_move = 0
    tot_error_side_view_move = 0

    error_summary = 0
    error_summary_i = 0
    punish_collision = 0
    eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
    model_cp= de_rotation_and_moving_tooth(tooth_type, model_cp, chromosome)
    i+=1
    teeth = copy.deepcopy(model_cp.teeth)
    summary_line = SplineKu(summary_pts[model_cp.arch_type])
    # flat_line = SplineKu(flat_pts[model_cp.arch_type])
    flat_line = [SplineKu(flat_pts[model_cp.arch_type][0]), SplineKu(flat_pts[model_cp.arch_type][1])]
    B = Bs[model_cp.arch_type]
    line_center = line_centers[model_cp.arch_type]
    A = As[model_cp.arch_type]
    destination_pts = destination_tooth[model_cp.arch_type]


    error_top_view = calculate_mesiodistal_balance_to_bonwill_line_from_top_view(teeth[tooth_type], B,line_center,summary_line,eigenvec, False, True,  A, destination_pts)
    error_side_view = calculate_mesiodistal_balance_to_bonwill_line_from_side_view(teeth[tooth_type], summary_line, eigenvec, False, True,  A, destination_pts)

    error_top_view_move = calculate_buccallabial_to_bonwill_line(teeth[tooth_type], summary_line,eigenvec, False,  A, destination_pts)
    error_side_view_move = calculate_cusp_to_flat_level_line(teeth[tooth_type], flat_line,eigenvec, False)

    # print(error_top_view, error_side_view, error_top_view_move, error_side_view_move)
    tot_error_top_view+=error_top_view**2
    tot_error_side_view+=error_side_view**2

    tot_error_top_view_move+=error_top_view_move**2
    tot_error_side_view_move+=error_side_view_move**2
    # print(tot_error_top_view, tot_error_side_view, tot_error_top_view_move, tot_error_side_view_move)
    # error_total = error_top_view+error_side_view+error_top_view_move+error_side_view_move

    # error_summary+=(error_total**2)
    error_summary_i+=1

    tot_error_top_view = math.sqrt(tot_error_top_view / error_summary_i)
    tot_error_top_view_move = math.sqrt(tot_error_top_view_move / error_summary_i)
    tot_error_side_view_move = math.sqrt(tot_error_side_view_move / error_summary_i)
    tot_error_side_view = math.sqrt(tot_error_side_view / error_summary_i)

    ArchCopy._clear()
    # error_summary = math.sqrt(error_summary/error_summary_i)
    error_summary = tot_error_top_view + tot_error_side_view + tot_error_top_view_move + tot_error_side_view_move
    totalerror = error_summary / 4
    # totalerror = (error_top_view + error_side_view + error_top_view_move + error_side_view_move)/4
        # return error_summary

    # print((error_top_view + error_side_view + error_top_view_move + error_side_view_move), totalerror)
    return totalerror
    # return error_summary
    
    

def mutation(x, F): # DE/rand/1
    return x[0] + F * (x[1] - x[2])

def mutation_best(xb, x, F): #DE/best/1
    return xb + F * (x[0] - x[1])
    

def check_bounds(mutated, bounds):
    mutated_bound = [np.clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound


def indvCreate2(arch_type, tooth_type, models, summary_pts, chr): #using bonwill

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
    ArchCopy._clear()
    tempGen = []
    index = Arch._get_index_arch_type(arch_type)
    m = models[index]

    eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
    model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))

    summary_line = SplineKu(summary_pts[model_cp.arch_type])

    tempGen.append(chr[0])
    tempGen.append(chr[1])
    tempGen.append(chr[2])

    if (tooth_type in toCenterArch):
        hitpspln, hitpln = summary_line.closestPointToAline([model_cp.mesh.centerOfMass(), model_cp.teeth[tooth_type].center],
                                                            isAwal=(tooth_type > 7))

    elif (tooth_type in toCrossover):
        labelSeberang = getToothLabelSeberang(tooth_type)
        hitpspln, hitpln = summary_line.closestPointToAline([model_cp.teeth[tooth_type].center, model_cp.teeth[labelSeberang].center],
                                                            isAwal=(tooth_type > 7))
    pt_in_line = hitpspln
    # tempGen.append(pt_in_line[0]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][0])
    # tempGen.append(pt_in_line[1]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][1])
    # tempGen.append(pt_in_line[2]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][2])
    tempGen.append(pt_in_line[0] - model_cp.teeth[tooth_type].center[0])
    tempGen.append(pt_in_line[1] - model_cp.teeth[tooth_type].center[1])
    tempGen.append(pt_in_line[2] - model_cp.teeth[tooth_type].center[2])

    ArchCopy._clear()

    return np.array(tempGen)


def indv_create_rot(arch_type, tooth_type, models, summary_pts, Bs, line_centers, chr,  As, destination_tooth):
    ArchCopy._clear()
    tempGen = []
    index = Arch._get_index_arch_type(arch_type)
    m = models[index]

    eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
    model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))

    summary_line = SplineKu(summary_pts[model_cp.arch_type])
    teeth = copy.deepcopy(model_cp.teeth)
    A = As[model_cp.arch_type]
    destination_pts = destination_tooth[model_cp.arch_type]

    eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
    rx,ry,rz = get_closest_possible_rotations(teeth[tooth_type],summary_line,Bs[model_cp.arch_type],line_centers[model_cp.arch_type],eigenvec,False,True, A, destination_pts)
    tempGen.append(rx)
    tempGen.append(ry)
    tempGen.append(rz)
    tempGen.append(chr[3])
    tempGen.append(chr[4])
    tempGen.append(chr[5])
    ArchCopy._clear()
    
    return np.array(tempGen)

def indv_create_move(arch_type, tooth_type,models, summary_pts,flat_pts, chr,  As, destination_tooth):
    ArchCopy._clear()
    tempGen = []
    index = Arch._get_index_arch_type(arch_type)
    m = models[index]

    eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
    model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))

    summary_line = SplineKu(summary_pts[model_cp.arch_type])
    # flat_line = SplineKu(flat_pts[model_cp.arch_type])
    flat_line = [SplineKu(flat_pts[model_cp.arch_type][0]), SplineKu(flat_pts[model_cp.arch_type][1])]
    teeth = copy.deepcopy(model_cp.teeth)
    A = As[model_cp.arch_type]
    destination_pts = destination_tooth[model_cp.arch_type]

    eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
    mx,my,mz = get_closest_possible_movements(teeth[tooth_type],summary_line, flat_line,eigenvec,False,True,  A, destination_pts)
    tempGen.append(chr[0])
    tempGen.append(chr[1])
    tempGen.append(chr[2])
    tempGen.append(mx)
    tempGen.append(my)
    tempGen.append(mz)
    ArchCopy._clear()
    
    return np.array(tempGen)

def indv_create_rot_and_move(arch_type, tooth_type, models, summary_pts, flat_pts, Bs, line_centers, chr,  As, destination_tooth):
    ArchCopy._clear()
    tempGen = []
    index = Arch._get_index_arch_type(arch_type)
    m = models[index]

    eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
    model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))

    summary_line = SplineKu(summary_pts[model_cp.arch_type])
    # flat_line = SplineKu(flat_pts[model_cp.arch_type])
    flat_line = [SplineKu(flat_pts[model_cp.arch_type][0]), SplineKu(flat_pts[model_cp.arch_type][1])]
    teeth = copy.deepcopy(model_cp.teeth)
    A = As[model_cp.arch_type]
    destination_pts = destination_tooth[model_cp.arch_type]


    eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
    rx,ry,rz,mx,my,mz = get_closest_possible_rotations_and_movements(teeth[tooth_type],summary_line, flat_line,Bs[model_cp.arch_type],line_centers[model_cp.arch_type],eigenvec,False,True,  A, destination_pts)
    tempGen.append(rx)
    tempGen.append(ry)
    tempGen.append(rz)
    tempGen.append(mx)
    tempGen.append(my)
    tempGen.append(mz)
    ArchCopy._clear()
    
    return np.array(tempGen)

def crossover(mutated, target, dims, cr):
    
    # generate a uniform random value for every dimension
    p = np.random.rand(dims)
    # generate trial vector by binomial crossover
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]
    return trial


def de_optimization(arch_type, tooth_type, n_tooth,n_chromosome, gen, models, pop_size, bounds, iter, F, cr, flats, summaries, line_centers, Bs,  As, destination_tooth):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = bounds[:, 0] + (np.random.rand(pop_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))

    if(len(gen)>0):
        # mutated[(i*(14*6)):(i+1)*(14*6)]
        pop[0]=gen[((arch_type-1)*n_tooth*n_chromosome) + (n_chromosome*(tooth_type-1)):
            ((arch_type-1)*n_tooth*n_chromosome) + (n_chromosome*(tooth_type-1+1))]


    myinitIndividu = indvCreate2(arch_type, tooth_type, models, summaries, pop[0])
    myinitIndividu = check_bounds(myinitIndividu, bounds)
    pop[-1]=myinitIndividu

    myinit_indv_rot = indv_create_rot(arch_type, tooth_type, models,summaries,Bs,line_centers,pop[0], As, destination_tooth)
    myinit_indv_rot = check_bounds(myinit_indv_rot, bounds)
    pop[-2]=myinit_indv_rot

    myinit_indv_mov = indv_create_move(arch_type, tooth_type, models,summaries,flats,pop[0],As, destination_tooth)
    myinit_indv_mov = check_bounds(myinit_indv_mov, bounds)
    pop[-3]=myinit_indv_mov

    myinit_indv_rot_mov = indv_create_rot_and_move(arch_type, tooth_type, models,summaries,flats,Bs,line_centers,pop[0],As, destination_tooth)
    myinit_indv_rot_mov = check_bounds(myinit_indv_rot_mov, bounds)
    pop[-4]=myinit_indv_rot_mov

    # print("pop",pop)
    # evaluate initial population of candidate solutions
    # obj_all = [minimize_function_using_delta_current_to_the_first_studi_model_calculation2(models, ind, flats, summaries, Bs, line_centers,  As, destination_tooth) for ind in pop]
    obj_all = np.array([minimize_function_using_delta_current_to_the_first_studi_model_calculation2(arch_type, tooth_type, models, ind, flats,
                                                                                                    summaries, Bs,
                                                                                                    line_centers, As,
                                                                                                    destination_tooth)
                        for ind in pop])
    print(obj_all)
    # print(obj_all)
    
    # find the best performing vector of initial population
    best_vector = pop[np.argmin(obj_all)]

    best_obj = obj_all[np.argmin(obj_all)]
    print(best_obj)
    prev_obj = best_obj
    # run iterations of the algorithm
    for i in range(iter):
        print("iter",i)
        # iterate over all candidate solutions
        for j in range(pop_size):
            # choose three candidates, a, b and c, that are not the current one
            candidates = [candidate for candidate in range(pop_size) if candidate != j]
            a, b= pop[np.random.choice(candidates, 2 , replace=False)]
            # perform mutation
            # print("mutation", "j", j)
            mutated = mutation_best(best_vector,[a, b], F)
            # check that lower and upper bounds are retained after mutation
            # print("check_bounds", "j", j)
            mutated = check_bounds(mutated, bounds)
            # perform crossover
            # print("crossover", "j", j)
            trial = crossover(mutated, pop[j], len(bounds), cr)
            
            # trial = custom_crossover(models, mutated, pop[j],  flats, summaries, Bs, line_centers,  As, destination_tooth)
            
            trial = check_bounds(trial, bounds)
            
            # compute objective function value for target vector
            obj_target = minimize_function_using_delta_current_to_the_first_studi_model_calculation2( arch_type, tooth_type, models, pop[j],flats, summaries,Bs, line_centers,  As, destination_tooth)
            # compute objective function value for trial vector
            obj_trial = minimize_function_using_delta_current_to_the_first_studi_model_calculation2( arch_type, tooth_type, models, trial,flats, summaries,Bs, line_centers,  As, destination_tooth)
            # print("obj_trial",i,j,obj_trial, obj_target)
            # print(pop[j])
            # print(trial)
            # perform selection
            if obj_trial <= obj_target:
                    # replace the target vector with the trial vector
                    pop[j] = trial
                    # store the new objective function value
                    obj_all[j] = obj_trial

        # find the best performing vector at each iteration
        # best_obj = np.min(obj_all)
        # best_obj = [np.min(obj_all[:, 0]), np.min(obj_all[:, 1])]
        best_obj = obj_all[np.argmin(obj_all)]
        # store the lowest objective function value
        if best_obj < prev_obj:

            best_vector = pop[np.argmin(obj_all)]

            prev_obj = best_obj
            # report progress at each iteration
            print('Iteration: ', i, str(prev_obj))
    print("best: ", arch_type, tooth_type, prev_obj, best_vector)
            # print('Iteration: %d f([%s]) = %.5f' % (i, np.around(best_vector, decimals=5), best_obj))
    return [best_vector, prev_obj]
    
    # dilakukan de dan return models yang paling optimum
    # return de models yang paling optimum


def start_de(models, flats, summaries, line_centers, Bs, gen, As, destination_tooth, is_arch_finish, is_tooth_finish, error_opt):
    
    
    pop_size = 7
    n_tooth = 14
    n_chromosome = 6
    # individu_bounds= [[-0.5, 0.5]]*n_tooth*2*n_chromosome
    individu_bounds= [
                [-1, 1],
                [-1, 1],
                [-1, 1],
                [-0.3, 0.3],
                [-0.3, 0.3],
                [-0.3, 0.3]] #*n_tooth*2
    bounds = np.asarray(individu_bounds)
    
    # define number of iterations
    iter = 15
    # define scale factor for mutation
    F = 0.5
    # define crossover rate for recombination
    cr = 0.7
    error_tooth = 3
    final_solution = []
    final_error = []
    seconds_start = time.time()
    for arch_type in ArchType:
        for tooth_type in ToothType:
            if tooth_type.value == ToothType.GINGIVA.value or tooth_type.value == ToothType.DELETED.value:
                continue
            # (i * (14 * 6)): (i + 1) * (14 * 6)]
            tooth_state = is_tooth_finish[((arch_type.value-1)*n_tooth)+tooth_type.value-1]
            if(not tooth_state):
                # solution = chormosome, error val
                solution = de_optimization(arch_type.value, tooth_type.value, n_tooth, n_chromosome, gen, models, pop_size, bounds, iter, F, cr, flats, summaries, line_centers, Bs,  As, destination_tooth)
                final_solution.extend(solution[0])
                final_error.append(solution[1]**2)
                if solution[1] < error_tooth:
                    is_tooth_finish[((arch_type.value - 1) * n_tooth) + tooth_type.value - 1] = True
            else:
                final_solution.extend([0,0,0,0,0,0])
                final_error.append(0)
    seconds_finish = time.time()
    sum_final_error = np.sum(np.array(final_error[:]))/len(final_error)
    rmse_final_error = math.sqrt(sum_final_error)
    timede = seconds_finish-seconds_start
    print("waktu de opt", timede,"detik")
    new_model = get_new_model(models, final_solution)
    return new_model,final_solution, rmse_final_error, is_arch_finish,is_tooth_finish, timede
    