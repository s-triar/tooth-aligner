import copy
import numpy as np
from vedo import Mesh

from constant.enums import ToothType, ArchType, LandmarkType
from optimization.optimization_helper import calculate_buccallabial_to_bonwill_line, calculate_cusp_to_flat_level_line, calculate_mesiodistal_balance_to_bonwill_line_from_side_view, calculate_mesiodistal_balance_to_bonwill_line_from_top_view, get_closest_possible_movements, get_closest_possible_rotations, get_closest_possible_rotations_and_movements
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
            
            # rotation
            mesh.rotateX(chr[0], False, teeth_center)
            model.update_teeth_point_rotation(i.value, "pitch", chr[0], teeth_center)
            mesh.rotateY(chr[1], False, teeth_center)
            model.update_teeth_point_rotation(i.value, "yaw", chr[1], teeth_center)
            mesh.rotateZ(chr[2], False, teeth_center)
            model.update_teeth_point_rotation(i.value, "roll", chr[2], teeth_center)
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



def minimize_function_using_delta_current_to_the_first_studi_model_calculation2( models, chromosome, flat_pts, summary_pts, Bs, line_centers):
    error_summary=0
    error_summary_i=0
    punish_collision = 0
    i=0
    ArchCopy._clear()

    model_upper_cp = None
    model_lower_cp = None
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        if(m.arch_type == ArchType.UPPER.value):
            model_upper_cp = model_cp
        else:
            model_lower_cp = model_cp
    
    models_cps=[model_upper_cp,model_lower_cp]
    
    for model_cp in models_cps:
        eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
        model_cp= de_rotation_and_moving(model_cp, chromosome[(i*(14*6)):(i+1)*(14*6)])
        i+=1
        teeth = copy.deepcopy(model_cp.teeth)
        summary_line = SplineKu(summary_pts[model_cp.arch_type])
        flat_line = SplineKu(flat_pts[model_cp.arch_type])
        B = Bs[model_cp.arch_type]
        line_center = line_centers[model_cp.arch_type]
        for tooth_type in teeth:
            if tooth_type != ToothType.GINGIVA.value and tooth_type != ToothType.DELETED.value:
                
                error_top_view = calculate_mesiodistal_balance_to_bonwill_line_from_top_view(teeth[tooth_type], B,line_center,summary_line,eigenvec, False, True) 
                error_side_view = calculate_mesiodistal_balance_to_bonwill_line_from_side_view(teeth[tooth_type], summary_line, eigenvec, False, True)
                
                error_top_view_move = calculate_buccallabial_to_bonwill_line(teeth[tooth_type], summary_line,eigenvec, False)
                error_side_view_move = calculate_cusp_to_flat_level_line(teeth[tooth_type], flat_line,eigenvec, False)
                
                error_total = error_top_view+error_side_view+error_top_view_move+error_side_view_move
                
                error_summary+=(error_total**2)
                error_summary_i+=1

    
    ArchCopy._clear()
    error_summary = math.sqrt(error_summary/error_summary_i)
    return error_summary+punish_collision
    # return error_summary
    
    

def mutation(x, F): # DE/rand/1
    return x[0] + F * (x[1] - x[2])

def mutation_best(xb, x, F): #DE/best/1
    return xb + F * (x[0] - x[1])
    

def check_bounds(mutated, bounds):
    mutated_bound = [np.clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound


def indvCreate2(models, summary_pts, chrs): #using bonwill
    ArchCopy._clear()
    tempGen = []
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
    model_upper_cp = None
    model_lower_cp = None
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        if(m.arch_type == ArchType.UPPER.value):
            model_upper_cp = model_cp
        else:
            model_lower_cp = model_cp
    
    models_cps=[model_upper_cp,model_lower_cp]
    
    for model_cp in models_cps:
        summary_line = SplineKu(summary_pts[model_cp.arch_type])
        teeth = copy.deepcopy(model_cp.teeth)
        for i in ToothType:    
            if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
                chr=chrs[(i.value-1)*6:((i.value-1)+1)*6]
                tempGen.append(chr[0])
                tempGen.append(chr[1])
                tempGen.append(chr[2])
                
                if(m.arch_type == ArchType.UPPER.value):
                    if(i.value in toCenterArch):
                        hitpspln, hitpln = summary_line.closestPointToAline([model_cp.mesh.centerOfMass(), teeth[i.value].center], isAwal=(i.value>7))
                        
                    elif(i.value in toCrossover):
                        labelSeberang = getToothLabelSeberang(i.value)
                        hitpspln, hitpln = summary_line.closestPointToAline([teeth[i.value].center, teeth[labelSeberang].center], isAwal=(i.value>7))
                    pt_in_line = hitpspln
                    # tempGen.append(pt_in_line[0]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][0])
                    # tempGen.append(pt_in_line[1]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][1])
                    # tempGen.append(pt_in_line[2]-teeth[i.value].landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value][2])
                    tempGen.append(pt_in_line[0]-teeth[i.value].center[0])
                    tempGen.append(pt_in_line[1]-teeth[i.value].center[1])
                    tempGen.append(pt_in_line[2]-teeth[i.value].center[2])
                
                else:
                    if(i.value in toCenterArch):
                        labelSeberang = getToothLabelSeberang(i.value)
                        pt_in_line = model_upper_cp.teeth[labelSeberang].landmark_pt[LandmarkType.LINGUAL_OR_PALATAL.value]
                        tempGen.append(pt_in_line[0]-teeth[i.value].landmark_pt[LandmarkType.CUSP.value][0])
                        tempGen.append(pt_in_line[1]-teeth[i.value].landmark_pt[LandmarkType.CUSP.value][1])
                        tempGen.append(pt_in_line[2]-teeth[i.value].landmark_pt[LandmarkType.CUSP.value][2])

                        
                    elif(i.value in toCrossover):
                        labelSeberang = getToothLabelSeberang(i.value)
                        pt_in_line = model_upper_cp.teeth[labelSeberang].landmark_pt[LandmarkType.PIT.value]
                        
                        bawah = teeth[i.value].landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value]
                        if(bawah is None):
                            bawah = teeth[i.value].landmark_pt[LandmarkType.CUSP_OUT.value]
                        if(bawah is None):
                            bawah = np.mean([teeth[i.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],teeth[i.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value]],axis=0)
                        
                        tempGen.append(pt_in_line[0]-bawah[0])
                        tempGen.append(pt_in_line[1]-bawah[1])
                        tempGen.append(pt_in_line[2]-bawah[2])
                    
                
    ArchCopy._clear()
    
    return np.array(tempGen)


def indv_create_rot(models, summary_pts, Bs, line_centers, chrs):
    ArchCopy._clear()
    tempGen = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        if(m.arch_type == ArchType.UPPER.value):
            model_upper_cp = model_cp
        else:
            model_lower_cp = model_cp
    
    models_cps=[model_upper_cp,model_lower_cp]
    for model_cp in models_cps:
        summary_line = SplineKu(summary_pts[model_cp.arch_type])
        teeth = copy.deepcopy(model_cp.teeth)
        for i in ToothType:    
            if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
                chr=chrs[(i.value-1)*6:((i.value-1)+1)*6]
                eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
                rx,ry,rz = get_closest_possible_rotations(teeth[i.value],summary_line,Bs[model_cp.arch_type],line_centers[model_cp.arch_type],eigenvec,False,True)
                tempGen.append(rx)
                tempGen.append(ry)
                tempGen.append(rz)
                tempGen.append(chr[3])
                tempGen.append(chr[4])
                tempGen.append(chr[5])
    ArchCopy._clear()
    
    return np.array(tempGen)

def indv_create_move(models, summary_pts,flat_pts, chrs):
    ArchCopy._clear()
    tempGen = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        if(m.arch_type == ArchType.UPPER.value):
            model_upper_cp = model_cp
        else:
            model_lower_cp = model_cp
    
    models_cps=[model_upper_cp,model_lower_cp]
    for model_cp in models_cps:
        summary_line = SplineKu(summary_pts[model_cp.arch_type])
        flat_line = SplineKu(flat_pts[model_cp.arch_type])
        teeth = copy.deepcopy(model_cp.teeth)
        for i in ToothType:    
            if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
                chr=chrs[(i.value-1)*6:((i.value-1)+1)*6]
                eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
                mx,my,mz = get_closest_possible_movements(teeth[i.value],summary_line, flat_line,eigenvec,False,True)
                tempGen.append(chr[0])
                tempGen.append(chr[1])
                tempGen.append(chr[2])
                tempGen.append(mx)
                tempGen.append(my)
                tempGen.append(mz)
    ArchCopy._clear()
    
    return np.array(tempGen)

def indv_create_rot_and_move(models, summary_pts, flat_pts, Bs, line_centers, chrs):
    ArchCopy._clear()
    tempGen = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        if(m.arch_type == ArchType.UPPER.value):
            model_upper_cp = model_cp
        else:
            model_lower_cp = model_cp
    
    models_cps=[model_upper_cp,model_lower_cp]
    for model_cp in models_cps:
        summary_line = SplineKu(summary_pts[model_cp.arch_type])
        flat_line = SplineKu(flat_pts[model_cp.arch_type])
        
        teeth = copy.deepcopy(model_cp.teeth)
        for i in ToothType:    
            if i.value != ToothType.GINGIVA.value and i.value != ToothType.DELETED.value:
                chr=chrs[(i.value-1)*6:((i.value-1)+1)*6]
                eigenvec = [model_cp.right_left_vec, model_cp.forward_backward_vec, model_cp.upward_downward_vec]
                rx,ry,rz,mx,my,mz = get_closest_possible_rotations_and_movements(teeth[i.value],summary_line, flat_line,Bs[model_cp.arch_type],line_centers[model_cp.arch_type],eigenvec,False,True)
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

def de_optimization(gen, models, pop_size, bounds, iter, F, cr, flats, summaries, line_centers, Bs):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = bounds[:, 0] + (np.random.rand(pop_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))
    if(len(gen)>0):
        pop[0]=gen
    myinitIndividu = indvCreate2(models, summaries, pop[0])
    myinitIndividu = check_bounds(myinitIndividu, bounds)
    pop[-1]=myinitIndividu
    
    myinit_indv_rot = indv_create_rot(models,summaries,Bs,line_centers,pop[0])
    myinit_indv_rot = check_bounds(myinit_indv_rot, bounds)
    pop[-2]=myinit_indv_rot
    
    myinit_indv_mov = indv_create_move(models,summaries,flats,pop[0])
    myinit_indv_mov = check_bounds(myinit_indv_mov, bounds)
    pop[-3]=myinit_indv_mov
    
    myinit_indv_rot_mov = indv_create_rot_and_move(models,summaries,flats,Bs,line_centers,pop[0])
    myinit_indv_rot_mov = check_bounds(myinit_indv_rot_mov, bounds)
    pop[-4]=myinit_indv_rot_mov
    
    # print("pop",pop)
    # evaluate initial population of candidate solutions
    obj_all = [minimize_function_using_delta_current_to_the_first_studi_model_calculation2(models, ind, flats, summaries, Bs, line_centers) for ind in pop]
    # print(obj_all)
    
    # find the best performing vector of initial population
    best_vector = pop[np.argmin(obj_all)]
    best_obj = np.min(obj_all)
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
            
            # trial = check_bounds(trial, bounds)
            
            # compute objective function value for target vector
            obj_target = minimize_function_using_delta_current_to_the_first_studi_model_calculation2(models, pop[j],flats, summaries,Bs, line_centers)
            # compute objective function value for trial vector
            obj_trial = minimize_function_using_delta_current_to_the_first_studi_model_calculation2(models, trial,flats, summaries,Bs, line_centers)
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
    

def start_de(models, flats, summaries, line_centers, Bs, gen):
    
    
    pop_size = 6
    n_tooth = 14
    n_chromosome = 6
    individu_bounds= [[-0.3, 0.3]]*n_tooth*2*n_chromosome
    bounds = np.asarray(individu_bounds)
    # define number of iterations
    iter = 20
    # define scale factor for mutation
    F = 0.5
    # define crossover rate for recombination
    cr = 0.7
    seconds_start = time.time()
    solution = de_optimization(gen, models, pop_size, bounds, iter, F, cr, flats, summaries, line_centers, Bs)
    seconds_finish = time.time()
    print("waktu de opt", (seconds_finish-seconds_start),"detik")
    new_model = get_new_model(models, solution[0])
    return new_model,solution[0], solution[1]
    