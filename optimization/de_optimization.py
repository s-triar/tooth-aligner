import copy
import numpy as np
from vedo import Mesh

from constant.enums import ToothType, ArchType, LandmarkType
from utility.arch_copy import ArchCopy
from utility.bolton_studi_model import Bolton
from utility.pont_studi_model import Pont
from utility.korkhaus_studi_model import Korkhaus
from utility.carey_studi_model import Carey
import numpy as np
import math

    
    
    
    
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
            model.update_teeth_point_moving(i.value, val_direction)
            # end moving
            
            temp_p = model.mesh.points()
            temp_p[faces_unique] = mesh.points()[faces_unique]
            model.mesh.points(temp_p)
    return model
        
        
def get_new_perhitungan_studi_model(models):
    bolton_studi = Bolton()
    korkhaus_studi = Korkhaus()
    pont_studi = Pont()
    carey_studi = Carey()
    
    bolton_studi.calc_anterior_overall(models)
    korkhaus_studi.calculate_khorkaus(models)
    pont_studi.calculate_pont(models)
    carey_studi.calculate_carey(models)
    
    return [bolton_studi, korkhaus_studi, pont_studi, carey_studi]
    

def get_total_error_studi_model(st):

    total_studi = 0
    
    bolton_studi_st = st[0]
    korkhaus_studi_st = st[1]
    pont_studi_st = st[2]
    carey_studi_st = st[3]
    
    total_studi = total_studi + abs(pont_studi_st.delta_pv[ArchType.UPPER.value])
    total_studi = total_studi + abs(pont_studi_st.delta_mp[ArchType.UPPER.value])
    total_studi = total_studi + abs(pont_studi_st.delta_pv[ArchType.LOWER.value])
    total_studi = total_studi + abs(pont_studi_st.delta_mp[ArchType.LOWER.value])
    # total_studi = total_studi + abs(carey_studi_st.arch_length_descrepancy[ArchType.UPPER.value])
    # total_studi = total_studi + abs(carey_studi_st.arch_length_descrepancy[ArchType.LOWER.value])
    total_studi = total_studi + abs(korkhaus_studi_st.status_line_to_width[ArchType.UPPER.value])
    total_studi = total_studi + abs(korkhaus_studi_st.status_line_to_width[ArchType.LOWER.value])
    total_studi = total_studi + abs(korkhaus_studi_st.status_khorkaus)
    total_studi = total_studi + abs(bolton_studi_st.correction_anterior)
    total_studi = total_studi + abs(bolton_studi_st.correction_overall)
    
    return total_studi
    
    
    
# def get_punishment(models, splines):
#     idx_max = 0 if models[0].arch_type == ArchType.UPPER.value else 1
#     idx_man = 1 if idx_max == 0 else 0
    
#     for i in ToothType:
#         label = i.value
#         mesial_max = models[idx_max].teeth[label].landmark_pt[LandmarkType.MESIAL.value]
#         distal_max = models[idx_max].teeth[label].landmark_pt[LandmarkType.DISTAL.value]
        
#         mesial_man = models[idx_man].teeth[label].landmark_pt[LandmarkType.MESIAL.value]
#         distal_man = models[idx_man].teeth[label].landmark_pt[LandmarkType.DISTAL.value]
        
#     # TODO give punishment if mesial and distal are inside spline
#     # TODO give punishment if mesial and distal have different distance to spline
#     # TODO give punishment to overlay teeth
#     pass

def get_new_model(models,chromosome):
    models_cp = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        
        models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
    for i in range(len(models_cp)):
        models_cp[i] = de_rotation_and_moving(models_cp[i], chromosome[(i*(14*6)):(i+1)*(14*6)]) # 6 chromosome per tooth
    return models_cp

def minimize_function(models, chromosome):
    models_cp = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        # c =copy.deepcopy(m.teeth)
        # print(c[1].index_vertice_cells)
        models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
    for i in range(len(models_cp)):
        models_cp[i] = de_rotation_and_moving(models_cp[i], chromosome[(i*14*6):(i+1)*14*6]) # 6 chromosome per tooth

    studimodels = get_new_perhitungan_studi_model(models_cp)
    total_studi_error = get_total_error_studi_model(studimodels)
    ArchCopy._clear()
    return total_studi_error

def mutation(x, F):
    return x[0] + F * (x[1] - x[2])

def check_bounds(mutated, bounds):
    mutated_bound = [np.clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound

def crossover(mutated, target, dims, cr):
    
    # generate a uniform random value for every dimension
    p = np.random.rand(dims)
    # generate trial vector by binomial crossover
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]
    return trial

def de_optimization(models, pop_size, bounds, iter, F, cr):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = bounds[:, 0] + (np.random.rand(pop_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))
    # print("pop",pop)
    # evaluate initial population of candidate solutions
    obj_all = [minimize_function(models, ind) for ind in pop]
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
            a, b, c = pop[np.random.choice(candidates, 3 , replace=False)]
            # perform mutation
            print("mutation", "j", j)
            mutated = mutation([a, b, c], F)
            # check that lower and upper bounds are retained after mutation
            print("check_bounds", "j", j)
            mutated = check_bounds(mutated, bounds)
            # perform crossover
            print("crossover", "j", j)
            trial = crossover(mutated, pop[j], len(bounds), cr)
            # compute objective function value for target vector
            obj_target = minimize_function(models, pop[j])
            # compute objective function value for trial vector
            obj_trial = minimize_function(models, trial)
            # perform selection
            if obj_trial < obj_target:
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
            print('Iteration: %d f([%s]) = %.5f' % (i, np.around(best_vector, decimals=5), best_obj))
    return [best_vector, best_obj]
    
    # dilakukan de dan return models yang paling optimum
    # return de models yang paling optimum
    

def start_de(models):
    pop_size = 10
    n_tooth = 14
    n_chromosome = 6
    individu_bounds= [[-0.3, 0.3]]*n_tooth*2*n_chromosome
    bounds = np.asarray(individu_bounds)
    # define number of iterations
    iter = 10
    # define scale factor for mutation
    F = 0.5
    # define crossover rate for recombination
    cr = 0.7
    solution = de_optimization(models, pop_size, bounds, iter, F, cr)
    new_model = get_new_model(models, solution[0])
    return new_model
    