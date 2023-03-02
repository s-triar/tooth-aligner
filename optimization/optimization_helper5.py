
from constant.enums import LandmarkType, ToothType
from utility.calculation import FaceTypeConversion, convert_to_2d, find_closest_point_between_a_point_and_a_line, find_distance_between_two_points, find_new_point_in_a_line_with_delta_distance, get_angle_from_2_2d_lines
from utility.tooth_label import get_tooth_labels
import numpy as np
import math
import copy

INNER_OUTER_MESIODISTAL_BONWILL_ERROR_WEIGHT = 10
BALANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT = 500 #sudut
DISTANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT = 1


DISTANCE_BUCCALLABIAL_BONWILL_ERROR_WEIGHT = 1
DISTANCE_CUSP_FLAT_LEVEL_ERROR_WEIGHT = 1

def get_candidate_chromosome(start, stop, step):
    res=[]
    current = start
    res.append(current)
    while current<=stop:
        current = round(current+step,1)
        res.append(current)
    return res


def get_closest_possible_rotations(tooth,spl,B, line_center, eigenvec,is_upper,is_standalone, A, destination_pts,max_chr=0.5, min_chr=-0.5, step=0.5):
    error = 999999999
    rot_x=0
    rot_y=0
    rot_z=0
    candidate_chr = get_candidate_chromosome(min_chr, max_chr, step)
    # toothmesh = tooth.get_mesh()
    for vx in candidate_chr:
        for vy in candidate_chr:
            for vz in candidate_chr:
                
                tooth_clone =  copy.deepcopy(tooth)
                tx_center = tooth_clone.center
                # tooth_clone.rotateX(vx, False, tx_center)
                tooth_clone.update_landmark_rotation("pitch", vx, tx_center)
                # tooth_clone.rotateY(vy, False, tx_center)
                tooth_clone.update_landmark_rotation("yaw", vy, tx_center)
                # tooth_clone.rotateZ(vz, False, tx_center)
                tooth_clone.update_landmark_rotation("roll", vz, tx_center)
                
                error_top_view = calculate_mesiodistal_balance_to_bonwill_line_from_top_view(tooth_clone, B,line_center,spl,eigenvec, is_upper, is_standalone, A, destination_pts) 
                error_side_view = calculate_mesiodistal_balance_to_bonwill_line_from_side_view(tooth_clone, spl, eigenvec, is_upper, is_standalone, A, destination_pts)
                error_total = error_top_view+error_side_view
                if(error > error_total):
                    error = error_total
                    rot_x=vx
                    rot_y=vy
                    rot_z=vz
                    
    return rot_x, rot_y, rot_z
                
def get_closest_possible_movements(tooth,spl, spl_flat,eigenvec,is_upper,is_standalone, A, destination_pts, max_chr=0.5, min_chr=-0.5, step=0.5):
    error = 999999999
    mov_x=0
    mov_y=0
    mov_z=0
    candidate_chr = get_candidate_chromosome(min_chr, max_chr, step)
    # toothmesh = tooth.get_mesh()
    
    for vx in candidate_chr:
        for vy in candidate_chr:
            for vz in candidate_chr:
                
                tooth_clone =  copy.deepcopy(tooth)

                val_direction=[vx,vy,vz]
                # tooth_clone.points(tooth_clone.points()+val_direction)
                tooth_clone.update_landmark_moving(val_direction)
                error_top_view = calculate_buccallabial_to_bonwill_line(tooth_clone, spl,eigenvec, is_upper,A, destination_pts)
                error_side_view = calculate_cusp_to_flat_level_line(tooth_clone, spl_flat,eigenvec, is_upper)
                error_total = error_top_view+error_side_view
                if(error > error_total):
                    error = error_total
                    mov_x=vx
                    mov_y=vy
                    mov_z=vz
                    
    return mov_x, mov_y, mov_z
                                
def get_closest_possible_rotations_and_movements(tooth,spl, spl_flat,B, line_center, eigenvec,is_upper,is_standalone, A, destination_pts, max_chr=0.5, min_chr=-0.5, step_rot=0.5, step_move=0.5):                
    error = 999999999
    rot_x=0
    rot_y=0
    rot_z=0
    mov_x=0
    mov_y=0
    mov_z=0
    candidate_chr_rot = get_candidate_chromosome(min_chr, max_chr, step_rot)
    candidate_chr_move = get_candidate_chromosome(min_chr, max_chr, step_move)
    # toothmesh = tooth.get_mesh()
    
    for vx in candidate_chr_rot:
        for vy in candidate_chr_rot:
            for vz in candidate_chr_rot:
                
                tooth_clone =  copy.deepcopy(tooth)
                tx_center = tooth_clone.center
                # tooth_clone.rotateX(vx, False, tx_center)
                tooth_clone.update_landmark_rotation("pitch", vx, tx_center)
                # tooth_clone.rotateY(vy, False, tx_center)
                tooth_clone.update_landmark_rotation("yaw", vy, tx_center)
                # tooth_clone.rotateZ(vz, False, tx_center)
                tooth_clone.update_landmark_rotation("roll", vz, tx_center)
                
                buccal_labial = tooth.landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]
                closest_buccallabial_to_spl = spl.closestPoint(buccal_labial)
                
                
    
                cusp = tooth.landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value]
                if(cusp is None):
                    cusp = tooth.landmark_pt[LandmarkType.CUSP_OUT.value]
                if(cusp is None):
                    cusp = tooth.landmark_pt[LandmarkType.CUSP.value]
                if(cusp is None):
                    cusp = np.mean([tooth.landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],tooth.landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value]],axis=0)
                                    
                closest_cusp_to_spl = spl.closestPoint(cusp)
                
                mx = (closest_buccallabial_to_spl[0]+closest_cusp_to_spl[0])/2
                my = (closest_buccallabial_to_spl[1]+closest_cusp_to_spl[1])/2
                mz = (closest_buccallabial_to_spl[2]+closest_cusp_to_spl[2])/2
                
                
                val_direction=[mx,my,mz]
                # tooth_clone.points(tooth_clone.points()+val_direction)
                tooth_clone.update_landmark_moving(val_direction)
                
                error_top_view = calculate_mesiodistal_balance_to_bonwill_line_from_top_view(tooth_clone, B,line_center,spl,eigenvec, is_upper, is_standalone,A, destination_pts) 
                error_side_view = calculate_mesiodistal_balance_to_bonwill_line_from_side_view(tooth_clone, spl, eigenvec, is_upper, is_standalone,A, destination_pts)
                
                error_top_view_move = calculate_buccallabial_to_bonwill_line(tooth_clone, spl,eigenvec, is_upper, A, destination_pts)
                error_side_view_move = calculate_cusp_to_flat_level_line(tooth_clone, spl_flat,eigenvec, is_upper)
                
                error_total = error_top_view+error_side_view+error_top_view_move+error_side_view_move
                
                if(error > error_total):
                    error = error_total
                    rot_x=vx
                    rot_y=vy
                    rot_z=vz
                    mov_x=mx
                    mov_y=my
                    mov_z=mz
                    
    return rot_x, rot_y, rot_z, mov_x, mov_y, mov_z

def calculate_mesiodistal_balance_to_bonwill_line_from_top_view(tooth,B, line_center, spl, eigvector, is_upper, is_spl_standalone, A, destination_pts, for_cr=False):
    
    tooth_labels = get_tooth_labels()
    
    if(tooth.label in tooth_labels['anterior'] or tooth.label in tooth_labels['canine']):
        
        mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
        distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
        closest_spl_mesial = destination_pts[tooth.label][0]
        closest_spl_distal = destination_pts[tooth.label][1]
        mesial2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[mesial])[0]
        distal2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[distal])[0]
        closest_spl_mesial2d=convert_to_2d(FaceTypeConversion.UP.value,eigvector,[closest_spl_mesial])[0]
        closest_spl_distal2d=convert_to_2d(FaceTypeConversion.UP.value,eigvector,[closest_spl_distal])[0]
        B_mesial2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[B])[0]
        B_distal2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[B])[0]
        
    elif(tooth.label in tooth_labels['posterior']): #posterior
        mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
        distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
        central_mesial_pt = find_closest_point_between_a_point_and_a_line(mesial, line_center)
        central_distal_pt = find_closest_point_between_a_point_and_a_line(distal, line_center)
        closest_spl_mesial = destination_pts[tooth.label][0]
        closest_spl_distal = destination_pts[tooth.label][1]
        mesial2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[mesial])[0]
        distal2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[distal])[0]
        closest_spl_mesial2d=convert_to_2d(FaceTypeConversion.UP.value,eigvector,[closest_spl_mesial])[0]
        closest_spl_distal2d=convert_to_2d(FaceTypeConversion.UP.value,eigvector,[closest_spl_distal])[0]
        B_mesial2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[central_mesial_pt])[0]
        B_distal2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[central_distal_pt])[0]
    
    
    out_of_spl_err = 0
    mesial_distal_to_spl_err=0
    mesial_distal_balance_err=0 #sudut
    
    mesial_to_center = find_distance_between_two_points(mesial2d,B_mesial2d)
    distal_to_center = find_distance_between_two_points(distal2d,B_distal2d)
    mesial_spl_to_center = find_distance_between_two_points(closest_spl_mesial2d,B_mesial2d)
    distal_spl_to_center = find_distance_between_two_points(closest_spl_distal2d,B_distal2d)
    
    # is_upper jika spl bukan standalone
    out_of_spl_err += 0 if (mesial_to_center-mesial_spl_to_center)<0 else abs(mesial_to_center-mesial_spl_to_center)
    out_of_spl_err += 0 if (distal_to_center-distal_spl_to_center)<0 else abs(distal_to_center-distal_spl_to_center)
    out_of_spl_err *= INNER_OUTER_MESIODISTAL_BONWILL_ERROR_WEIGHT
    
    mesial_to_spl = find_distance_between_two_points(mesial2d,closest_spl_mesial2d)
    distal_to_spl = find_distance_between_two_points(distal2d,closest_spl_distal2d)
    
    
    
    temp_mes += abs(mesial_to_spl)
    temp_dis += abs(distal_to_spl)
    # mesial_distal_to_spl_err += abs(mesial_to_spl)
    # mesial_distal_to_spl_err += abs(distal_to_spl)
    mesial_distal_to_spl_err += abs(temp_mes-temp_dis)
    mesial_distal_to_spl_err *= DISTANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
    
    check_same_in_or_out_spl = ((mesial_to_center-mesial_spl_to_center) < 0 and (distal_to_center-distal_spl_to_center)<0) or ((mesial_to_center-mesial_spl_to_center) >= 0 and (distal_to_center-distal_spl_to_center)>=0) 
    if(check_same_in_or_out_spl == True):
        if(mesial_to_spl < distal_to_spl):
            ext = find_new_point_in_a_line_with_delta_distance(closest_spl_distal2d,distal2d,mesial_to_spl-distal_to_spl)    
            anchor = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[1]])
            spl_pt = np.array([closest_spl_distal2d[0],closest_spl_distal2d[1]])
        else:
            ext = find_new_point_in_a_line_with_delta_distance(closest_spl_mesial2d,mesial2d,distal_to_spl-mesial_to_spl)    
            anchor = np.array([closest_spl_distal2d[0],closest_spl_distal2d[1]])
            spl_pt = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[1]])
    else:
        if(mesial_to_spl < distal_to_spl):
            ext = find_new_point_in_a_line_with_delta_distance(closest_spl_distal2d,distal2d,mesial_to_spl-distal_to_spl)    
            anchor = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[1]])
            spl_pt = np.array([closest_spl_distal2d[0],closest_spl_distal2d[1]])
        else:
            ext = find_new_point_in_a_line_with_delta_distance(closest_spl_mesial2d,mesial2d,distal_to_spl-mesial_to_spl)    
            anchor = np.array([closest_spl_distal2d[0],closest_spl_distal2d[1]])
            spl_pt = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[1]])
        # ext = find_new_point_in_a_line_with_delta_distance(closest_spl_distal2d,distal2d,mesial_to_spl)
        # ext = np.array([ext[0],ext[1]])
        # anchor = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[1]])
        # spl_pt = np.array([closest_spl_distal2d[0],closest_spl_distal2d[1]])
    
    angle = get_angle_from_2_2d_lines([anchor,ext],[anchor,spl_pt],True)
    
    mesial_distal_balance_err+=angle
    mesial_distal_balance_err*=BALANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
    if(math.isnan(mesial_distal_balance_err)):
        # mesial_distal_balance_err=3.14*BALANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
        mesial_distal_balance_err=90*BALANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
        print(tooth.label,"ada NaN", [anchor,ext],[anchor,spl_pt])
    # print("calculate_mesiodistal_balance_to_bonwill_line_from_top_view",tooth.label ,out_of_spl_err,mesial_distal_to_spl_err,mesial_distal_balance_err)
    out_of_spl_err=out_of_spl_err*0.2
    mesial_distal_to_spl_err=mesial_distal_to_spl_err*0.1
    mesial_distal_balance_err=mesial_distal_balance_err*0.7
    if(for_cr):
        return out_of_spl_err+mesial_distal_balance_err, mesial_distal_to_spl_err
    return out_of_spl_err+mesial_distal_to_spl_err+mesial_distal_balance_err
    
    

def calculate_mesiodistal_balance_to_bonwill_line_from_side_view(tooth, spl, eigvector, is_upper, is_spl_standalone, A, destination_pts, for_cr=False):
    tooth_labels = get_tooth_labels()
    eig_up_down = eigvector[2]
    mesial = tooth.landmark_pt[LandmarkType.MESIAL.value]
    distal = tooth.landmark_pt[LandmarkType.DISTAL.value]
    buccal_labial = tooth.landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]
    # point_between_mesial_distal_to_buccallabial = find_closest_point_between_a_point_and_a_line(buccal_labial,[mesial,distal])
    # closest_spl_mesial = spl.closestPoint(mesial)
    # closest_spl_distal = spl.closestPoint(distal)
    # closest_spl_buccallabial, closest_ln_buccallabial  = spl.closestPointToAline([buccal_labial, point_between_mesial_distal_to_buccallabial],isAwal=(tooth.label>7))
    closest_spl_mesial = destination_pts[tooth.label][0]
    closest_spl_distal = destination_pts[tooth.label][1]
    closest_spl_buccallabial = destination_pts[tooth.label][2]
    
    
    
    if(tooth.label in tooth_labels['anterior'] or tooth.label in tooth_labels['canine']):
        mesial2d = convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[mesial])[0]
        distal2d = convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[distal])[0]
        buccal_labial2d=convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[buccal_labial])[0]
        closest_spl_buccallabial2d = convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[closest_spl_buccallabial])[0]
        closest_spl_mesial2d =convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[closest_spl_mesial])[0]
        closest_spl_distal2d =convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[closest_spl_distal])[0]
        
        buccal_labial2d_real = np.array([buccal_labial2d[0],buccal_labial2d[2]])
        closest_spl_buccallabial2d_real = np.array([closest_spl_buccallabial2d[0],closest_spl_buccallabial2d[2]])
        closest_spl_mesial2d_real = np.array([closest_spl_mesial2d[0],closest_spl_mesial2d[2]])
        
        
    elif(tooth.label in tooth_labels['posterior']): #posterior
        mesial2d = convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[mesial])[0]
        distal2d = convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[distal])[0]
        buccal_labial2d=convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[buccal_labial])[0]
        closest_spl_buccallabial2d = convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[closest_spl_buccallabial])[0]
        closest_spl_mesial2d =convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[closest_spl_mesial])[0]
        closest_spl_distal2d =convert_to_2d(FaceTypeConversion.LEFT.value,eigvector,[closest_spl_distal])[0]
        
        buccal_labial2d_real = np.array([buccal_labial2d[1],buccal_labial2d[2]])
        closest_spl_buccallabial2d_real = np.array([closest_spl_buccallabial2d[1],closest_spl_buccallabial2d[2]])
        closest_spl_mesial2d_real = np.array([closest_spl_mesial2d[1],closest_spl_mesial2d[2]])
        
    out_of_spl_err = 0
    mesial_distal_to_spl_err=0
    mesial_distal_balance_err=0 #sudut
    
    mesial_to_upper = np.dot(mesial2d,eig_up_down)
    distal_to_upper = np.dot(distal2d,eig_up_down)
    mesial_spl_to_upper = np.dot(closest_spl_mesial2d,eig_up_down)
    distal_spl_to_upper = np.dot(closest_spl_distal2d,eig_up_down)
    
    # is_upper jika spl bukan standalone
    out_of_spl_err += 0 if mesial_to_upper < mesial_spl_to_upper else abs(mesial_to_upper-mesial_spl_to_upper)
    out_of_spl_err += 0 if distal_to_upper < distal_spl_to_upper else abs(distal_to_upper-distal_spl_to_upper)
    out_of_spl_err *= INNER_OUTER_MESIODISTAL_BONWILL_ERROR_WEIGHT
    
    mesial_to_spl = find_distance_between_two_points(mesial2d,closest_spl_mesial2d)
    distal_to_spl = find_distance_between_two_points(distal2d,closest_spl_distal2d)
    
    temp_mes += abs(mesial_to_spl)
    temp_dis += abs(distal_to_spl)
    # mesial_distal_to_spl_err += abs(mesial_to_spl)
    # mesial_distal_to_spl_err += abs(distal_to_spl)
    mesial_distal_to_spl_err += abs(temp_mes-temp_dis)
    mesial_distal_to_spl_err *= DISTANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
    
    
    
    
    
    angle = get_angle_from_2_2d_lines([closest_spl_buccallabial2d_real,buccal_labial2d_real],[closest_spl_buccallabial2d_real,closest_spl_mesial2d_real], True)
    # angle = abs((math.pi/2)-angle)
    angle = abs(90-angle)
    mesial_distal_balance_err+=angle
    mesial_distal_balance_err*=BALANCE_MESIODISTAL_BONWILL_ERROR_WEIGHT
    out_of_spl_err=out_of_spl_err*0.2
    mesial_distal_to_spl_err=mesial_distal_to_spl_err*0.1
    mesial_distal_balance_err=mesial_distal_balance_err*0.7
    if(for_cr):
        return out_of_spl_err+mesial_distal_balance_err, mesial_distal_to_spl_err
    return out_of_spl_err+mesial_distal_to_spl_err+mesial_distal_balance_err

def calculate_buccallabial_to_bonwill_line(tooth, spl, eigvector, is_upper, A, destination_pts):
    buccal_labial = tooth.landmark_pt[LandmarkType.BUCCAL_OR_LABIAL.value]
    # closest_buccallabial_to_spl = spl.closestPoint(buccal_labial)
    closest_buccallabial_to_spl = destination_pts[tooth.label][2]
    buccal_labial2d = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[buccal_labial])[0]
    closest_buccallabial_to_spl2D = convert_to_2d(FaceTypeConversion.UP.value,eigvector,[closest_buccallabial_to_spl])[0]
    dst = find_distance_between_two_points(buccal_labial2d,closest_buccallabial_to_spl2D)
    return dst*DISTANCE_BUCCALLABIAL_BONWILL_ERROR_WEIGHT

def calculate_cusp_to_flat_level_line(tooth, spl, eigvector, is_upper):
    cusp = tooth.landmark_pt[LandmarkType.CUSP_OUT_MIDDLE.value]
    if(cusp is None):
        cusp = tooth.landmark_pt[LandmarkType.CUSP_OUT.value]
    if(cusp is None):
        cusp = tooth.landmark_pt[LandmarkType.CUSP.value]
    if(cusp is None):
        cusp = np.mean([tooth.landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],tooth.landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value]],axis=0)
                        
    closest_cusp_to_spl = spl.closestPoint(cusp)
    cusp2d = convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[cusp])[0]
    closest_cusp_to_spl2D = convert_to_2d(FaceTypeConversion.FRONT.value,eigvector,[closest_cusp_to_spl])[0]
    dst = find_distance_between_two_points(cusp2d,closest_cusp_to_spl2D)
    return dst*DISTANCE_CUSP_FLAT_LEVEL_ERROR_WEIGHT