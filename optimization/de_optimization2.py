import copy
import numpy as np
from vedo import Mesh

from constant.enums import ToothType, ArchType, LandmarkType
from utility.arch_copy import ArchCopy
from utility.bolton_studi_model import Bolton
from utility.calculation import FaceTypeConversion, convert_to_2d, find_distance_between_two_points
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
    
def get_collision_teeth_status(model, new_model):
    total = 0
    for i in range(1,15):
        label_before=i-1
        label_current = i
        label_after=i+1
        
        archmesh_verts = model.mesh.points()
        new_archmesh_verts = new_model.mesh.points()
        
        mesh_tooth_before_before_rotation=None
        mesh_tooth_after_before_rotation=None
        
        faces_current = model.teeth[label_current].index_vertice_cells
        mesh_tooth_current_current_rotation = Mesh([archmesh_verts, faces_current])
        new_faces_current = new_model.teeth[label_current].index_vertice_cells
        new_mesh_tooth_current_current_rotation = Mesh([new_archmesh_verts, new_faces_current])
        
        if(label_before>0):
            faces_before = model.teeth[label_before].index_vertice_cells
            mesh_tooth_before_before_rotation = Mesh([archmesh_verts, faces_before])
            new_faces_before = new_model.teeth[label_before].index_vertice_cells
            new_mesh_tooth_before_before_rotation = Mesh([new_archmesh_verts, new_faces_before])
            
        pts_col_before_before_rotation=[]
        new_pts_col_before_before_rotation=[]
            
        if(mesh_tooth_before_before_rotation!=None):
            col_before = mesh_tooth_current_current_rotation.clone().cutWithMesh(mesh_tooth_before_before_rotation)
            pts_col_before_before_rotation=col_before.points()
            new_col_before = new_mesh_tooth_current_current_rotation.clone().cutWithMesh(new_mesh_tooth_before_before_rotation)
            new_pts_col_before_before_rotation=new_col_before.points()    
        
        if(len(new_pts_col_before_before_rotation) > len(pts_col_before_before_rotation)):
            total+= 10000
            
        
        
        if(label_after<15):
            faces_after = model.teeth[label_after].index_vertice_cells
            mesh_tooth_after_before_rotation = Mesh([archmesh_verts, faces_after])
            new_faces_after = model.teeth[label_after].index_vertice_cells
            new_mesh_tooth_after_before_rotation = Mesh([new_archmesh_verts, new_faces_after])

        pts_col_after_before_rotation=[]
        new_pts_col_after_before_rotation=[]
        

        if(mesh_tooth_after_before_rotation!=None):
            col_after = mesh_tooth_current_current_rotation.clone().cutWithMesh(mesh_tooth_after_before_rotation)
            pts_col_after_before_rotation=col_after.points()
            new_col_after = new_mesh_tooth_current_current_rotation.clone().cutWithMesh(new_mesh_tooth_after_before_rotation)
            new_pts_col_after_before_rotation=new_col_after.points()
        
        if(len(new_pts_col_after_before_rotation) > len(pts_col_after_before_rotation)):
            total+= 10000

        
    return total
        
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
    ArchCopy._clear()
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        
        models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
    for i in range(len(models_cp)):
        models_cp[i] = de_rotation_and_moving(models_cp[i], chromosome[(i*(14*6)):(i+1)*(14*6)]) # 6 chromosome per tooth
    return models_cp

def minimize_function_using_recalculation_studi_model(models, chromosome):
    models_cp = []
    ArchCopy._clear()
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        # c =copy.deepcopy(m.teeth)
        # print(c[1].index_vertice_cells)
        models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
    for i in range(len(models_cp)):
        models_cp[i] = de_rotation_and_moving(models_cp[i], chromosome[(i*14*6):(i+1)*14*6]) # 6 chromosome per tooth

    studimodels = get_new_perhitungan_studi_model(models_cp)
    total_studi_error = get_total_error_studi_model(studimodels)
    return total_studi_error

def minimize_function_using_delta_current_to_the_first_studi_model_calculation( models, chromosome, flat_pts, summary_pts):
    error_flat=0
    error_summary=0
    error_flat_i=0
    error_summary_i=0
    punish_collision = 0
    i=0
    ArchCopy._clear()
    
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        model_cp= de_rotation_and_moving(model_cp, chromosome[(i*(14*6)):(i+1)*(14*6)])
        i+=1
        
        # models_cp.append(ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva)))
        
        # begin calc error flat
        teeth = copy.deepcopy(model_cp.teeth)
        pts_cusps=np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                
                teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
        pts_flat = flat_pts[model_cp.arch_type]
        for ipt in range(len(pts_cusps)):
            a = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [pts_flat[ipt]])[0]
            b = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [pts_cusps[ipt]])[0]
            dst = find_distance_between_two_points(a,b)
            error_flat+=(dst**2)
            error_flat_i+=1
        # end calc error flat
        
        # begin calc error summary
        # print("summary_pts[model_cp.arch_type]", summary_pts[model_cp.arch_type][1])
        summary_line = SplineKu(summary_pts[model_cp.arch_type][1], degree=3, smooth=0, res=600)
        for tooth_type in teeth:
            pt_in_line = summary_line.closestPoint(teeth[tooth_type].center)
            a = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [pt_in_line])[0]
            b = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [teeth[tooth_type].center])[0]
            # a = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [pt_in_line])[0]
            # b = convert_to_2d(FaceTypeConversion.RIGHT.value, eigenvec, [teeth[tooth_type].center])[0]
            dst = find_distance_between_two_points(a,b)
            error_summary+=(dst**2)
            error_summary_i+=1
        # end calc error summary
        
        # begin calc error rotate
        
        
        
        # end calc error rotate
        
        # calculate punishment
        # punish_collision += get_collision_teeth_status(m, model_cp)
        
    error_summary = math.sqrt(error_summary/error_summary_i)
    error_flat = math.sqrt(error_flat/error_flat_i)
    return error_flat+error_summary+punish_collision
    

def mutation(x, F):
    return x[0] + F * (x[1] - x[2])



def check_bounds(mutated, bounds):
    mutated_bound = [np.clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound

def new_crossover(models, summary_pts):
    tempGen = []
    for m in models:
        eigenvec = [m.right_left_vec, m.forward_backward_vec, m.upward_downward_vec]
        model_cp = ArchCopy(m.arch_type, m.mesh, eigenvec, copy.deepcopy(m.teeth), copy.deepcopy(m.gingiva))
        summary_line = SplineKu(summary_pts[model_cp.arch_type][1], degree=3, smooth=0, res=600)
        teeth = copy.deepcopy(model_cp.teeth)
        for tooth_type in teeth:
            pt_in_line = summary_line.closestPoint(teeth[tooth_type].center)
            tempGen.append(pt_in_line[0]-teeth[tooth_type].center[0])
        
    return tempGen
    

def crossover(mutated, target, dims, cr):
    
    # generate a uniform random value for every dimension
    p = np.random.rand(dims)
    # generate trial vector by binomial crossover
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]
    return trial

def de_optimization(gen, models, pop_size, bounds, iter, F, cr, flats, summaries):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = bounds[:, 0] + (np.random.rand(pop_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))
    if(len(gen)>0):
        pop[0]=gen
    # print("pop",pop)
    # evaluate initial population of candidate solutions
    obj_all = [minimize_function_using_delta_current_to_the_first_studi_model_calculation(models, ind, flats, summaries) for ind in pop]
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
            # print("mutation", "j", j)
            mutated = mutation([a, b, c], F)
            # check that lower and upper bounds are retained after mutation
            # print("check_bounds", "j", j)
            mutated = check_bounds(mutated, bounds)
            # perform crossover
            # print("crossover", "j", j)
            # trial = crossover(mutated, pop[j], len(bounds), cr)
            trial = new_crossover(models, summaries)
            # compute objective function value for target vector
            obj_target = minimize_function_using_delta_current_to_the_first_studi_model_calculation(models, pop[j],flats, summaries)
            # compute objective function value for trial vector
            obj_trial = minimize_function_using_delta_current_to_the_first_studi_model_calculation(models, trial,flats, summaries)
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
            print('Iteration: %d = %.5f' % (i, best_obj))
            # print('Iteration: %d f([%s]) = %.5f' % (i, np.around(best_vector, decimals=5), best_obj))
    return [best_vector, best_obj]
    
    # dilakukan de dan return models yang paling optimum
    # return de models yang paling optimum
    

def start_de(models, flats, summaries, gen):
    
    
    pop_size = 6
    n_tooth = 14
    n_chromosome = 3
    individu_bounds= [[-0.3, 0.3]]*n_tooth*2*n_chromosome
    bounds = np.asarray(individu_bounds)
    # define number of iterations
    iter = 5
    # define scale factor for mutation
    F = 0.5
    # define crossover rate for recombination
    cr = 0.7
    seconds_start = time.time()
    solution = de_optimization(gen, models, pop_size, bounds, iter, F, cr, flats, summaries)
    seconds_finish = time.time()
    print("waktu de opt", (seconds_finish-seconds_start),"detik")
    new_model = get_new_model(models, solution[0])
    return new_model,solution[0], solution[1]
    