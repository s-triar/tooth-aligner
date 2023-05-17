import glob
import numpy as np
from constant.enums import ArchType, ToothType, LandmarkType, LandmarkDefinition
import pandas as pd
from vedo import load
from landmark_training.landmark_helper import get_candidate_points, get_point_landmark_normalized
from landmark_training.param_landmark_area import candidate_definition
import utility.landmarking_lib as ll
import math

from utility.calculation import find_distance_between_two_points

exception_path = [
    "1 MNF",
    "4. SN",
    "7. GSF",
    "8. UR"
]

path_data_csv=[
"D:\\tesis\\fix\\10. CPL\\CPL_LOWER.csv",
"D:\\tesis\\fix\\10. CPL\\CPL_UPPER.csv",
"D:\\tesis\\fix\\11. SS\\SS_LOWER.csv",
"D:\\tesis\\fix\\11. SS\\SS_UPPER.csv",
"D:\\tesis\\fix\\12. KEC\\KEC_LOWER.csv",
"D:\\tesis\\fix\\12. KEC\\KEC_UPPER.csv",
"D:\\tesis\\fix\\13. HC\\HC_LOWER.csv",
"D:\\tesis\\fix\\13. HC\\HC_UPPER.csv",
"D:\\tesis\\fix\\14. ZR\\ZR_LOWER.csv",
"D:\\tesis\\fix\\14. ZR\\ZR_UPPER.csv",
"D:\\tesis\\fix\\15. YS\\YS_landmark_LOWER.csv",
"D:\\tesis\\fix\\15. YS\\YS_landmark_UPPER.csv",
"D:\\tesis\\fix\\16. FAW\\FAW_LOWER.csv",
"D:\\tesis\\fix\\16. FAW\\FAW_UPPER.csv",
"D:\\tesis\\fix\\18. WPP\\WPP_LOWER.csv",
"D:\\tesis\\fix\\18. WPP\\WPP_UPPER.csv",
"D:\\tesis\\fix\\19. Sam\\Sam_LOWER.csv",
"D:\\tesis\\fix\\19. Sam\\Sam_UPPER.csv",
"D:\\tesis\\fix\\2. MJK\\MJK_LOWER.csv",
"D:\\tesis\\fix\\2. MJK\\MJK_UPPER.csv",
"D:\\tesis\\fix\\21. MRAI\\MRAI_LOWER.csv",
"D:\\tesis\\fix\\21. MRAI\\MRAI_UPPER.csv",
"D:\\tesis\\fix\\22. NS\\NS_LOWER.csv",
"D:\\tesis\\fix\\22. NS\\NS_UPPER.csv",
"D:\\tesis\\fix\\23. AP\\AP_landmark_LOWER.csv",
"D:\\tesis\\fix\\23. AP\\AP_landmark_UPPER.csv",
"D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.csv",
"D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.csv",
"D:\\tesis\\fix\\5. BA\\BA_LOWER.csv",
"D:\\tesis\\fix\\5. BA\\BA_UPPER.csv",
"D:\\tesis\\fix\\6. NR\\NR_LOWER.csv",
"D:\\tesis\\fix\\6. NR\\NR_UPPER.csv",
]
path_data_vtp = [
"D:\\tesis\\fix\\10. CPL\\CPL_LOWER.vtp",
"D:\\tesis\\fix\\10. CPL\\CPL_UPPER.vtp",
"D:\\tesis\\fix\\11. SS\\SS_LOWER.vtp",
"D:\\tesis\\fix\\11. SS\\SS_UPPER.vtp",
"D:\\tesis\\fix\\12. KEC\\KEC_LOWER.vtp",
"D:\\tesis\\fix\\12. KEC\\KEC_UPPER.vtp",
"D:\\tesis\\fix\\13. HC\\HC_LOWER.vtp",
"D:\\tesis\\fix\\13. HC\\HC_UPPER.vtp",
"D:\\tesis\\fix\\14. ZR\\ZR_LOWER.vtp",
"D:\\tesis\\fix\\14. ZR\\ZR_UPPER.vtp",
"D:\\tesis\\fix\\15. YS\\YS_LOWER.vtp",
"D:\\tesis\\fix\\15. YS\\YS_UPPER_.vtp",
"D:\\tesis\\fix\\16. FAW\\FAW_LOWER.vtp",
"D:\\tesis\\fix\\16. FAW\\FAW_UPPER.vtp",
"D:\\tesis\\fix\\18. WPP\\WPP_LOWER.vtp",
"D:\\tesis\\fix\\18. WPP\\WPP_UPPER.vtp",
"D:\\tesis\\fix\\19. Sam\\Sam_LOWER.vtp",
"D:\\tesis\\fix\\19. Sam\\Sam_UPPER.vtp",
"D:\\tesis\\fix\\2. MJK\\MJK_LOWER.vtp",
"D:\\tesis\\fix\\2. MJK\\MJK_UPPER.vtp",
"D:\\tesis\\fix\\21. MRAI\\MRAI_LOWER.vtp",
"D:\\tesis\\fix\\21. MRAI\\MRAI_UPPER.vtp",
"D:\\tesis\\fix\\22. NS\\NS_LOWER.vtp",
"D:\\tesis\\fix\\22. NS\\NS_UPPER.vtp",
"D:\\tesis\\fix\\23. AP\\AP_LOWER.vtp",
"D:\\tesis\\fix\\23. AP\\AP_UPPER.vtp",
"D:\\tesis\\fix\\24. GS\\Gerry Sihaj_LOWER.vtp",
"D:\\tesis\\fix\\24. GS\\Gerry Sihaj_UPPER.vtp",
"D:\\tesis\\fix\\5. BA\\BA_LOWER.vtp",
"D:\\tesis\\fix\\5. BA\\BA_UPPER.vtp",
"D:\\tesis\\fix\\6. NR\\NR_LOWER.vtp",
"D:\\tesis\\fix\\6. NR\\NR_UPPER.vtp",
]
print(len(path_data_vtp), len(path_data_csv))
ld_def = LandmarkDefinition().archs

def generate_data():
    data={}

    for archtype in ArchType:
        if archtype.value not in data:
            data[archtype.value] = {}
        for toothtype in ToothType:
            if toothtype.value == ToothType.GINGIVA.value or toothtype.value == ToothType.DELETED.value:
                continue
            if toothtype.value not in data[archtype.value]:
                data[archtype.value][toothtype.value] = {}
            for landmark_val in ld_def[archtype.value][toothtype.value]:
                if landmark_val not in data[archtype.value][toothtype.value]:
                    data[archtype.value][toothtype.value][landmark_val] = {
                        'total':0,
                        'n':0
                    }
    return data
# print(data)
#
#
# for p in glob.glob(r"D:\tesis\fix\*\*"):
#     if p.split("\\")[3] in exception_path:
#         continue
#     print(p)

def import_landmark_def(landmark_def_path):
    landmark_definition = {}
    df = pd.read_csv(landmark_def_path, encoding='utf-8', header=None)
    for index, row in df.iterrows():
        idx_arch = 1
        idx_tooth = 3
        idx_landmark = 5
        idx_coord = 7
        arch = int(row[idx_arch])
        tooth = int(row[idx_tooth])
        landmark = int(row[idx_landmark])
        coordinate=str(row[idx_coord])
        coors = []
        coord = coordinate.split("|")
        for c in coord:
            coors.append(float(c))

        if arch in landmark_definition:
            if tooth in landmark_definition[arch]:
                if landmark in landmark_definition[arch][tooth]:
                    landmark_definition[arch][tooth][landmark] = coors
                else:
                    landmark_definition[arch][tooth][landmark] = {}
                    landmark_definition[arch][tooth][landmark] = coors
            else:
                landmark_definition[arch][tooth] = {}
                landmark_definition[arch][tooth][landmark] = coors
        else:
            landmark_definition[arch] = {}
            landmark_definition[arch][tooth] = {}
            landmark_definition[arch][tooth][landmark] = coors
    return  landmark_definition

def get_landmark_point(parameter, arch_type, tooth_type, landmark_type, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth, vertices_tooth):
    # candidate_def = candidate_definition[arch_type][tooth_type][landmark_type]
    # vertices_tooth_new = get_candidate_points(candidate_def, eigen_vec_mesh, norm_center_tooth, norm_vertices_tooth)
    # print(arch_type, tooth_type, landmark_type)
    normalized_point = get_point_landmark_normalized(eigen_vec_mesh, norm_vertices_tooth, parameter)
    landmark_index = np.argwhere(np.isin(norm_vertices_tooth, normalized_point).all(axis=1))[0][0]
    return vertices_tooth[landmark_index]

def extract_eigen_mesh(mesh):
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
    return eigen_vec_mesh

def extract_mesh_tooth(mesh, label):
    center_mesh = mesh.centerOfMass()
    points_mesh = np.array(mesh.points())
    idx_faces_mesh = np.array(mesh.cells())
    points_mesh_normalized = points_mesh - center_mesh
    cells_tooth_index = np.where(mesh.celldata['Label'] == label)
    label = math.floor(label)
    cells_tooth = idx_faces_mesh[cells_tooth_index]
    points_tooth_index = np.unique(cells_tooth)
    points_tooth = points_mesh[points_tooth_index]
    points_tooth_normalized = points_mesh_normalized[points_tooth_index]
    center_tooth = np.mean(points_tooth, axis=0)
    center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)
    return points_tooth, points_tooth_normalized, center_tooth_normalized

folder = 'f_cr'
path_landmark_files =[
    # folder = f_cr
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.5_cr0.3_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.5_cr0.5_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.5_cr0.7_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.25_cr0.3_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.25_cr0.5_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.25_cr0.7_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.75_cr0.3_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.75_cr0.5_no_candidate.csv",
    folder+"\\"+"ld_saved_de_pop1000_iter10_f0.75_cr0.7_no_candidate.csv"


    # folder = popiter
    # folder+"\\"+"ld_saved_de_iter10_pop1000_f05_cr07.csv",
    # folder+"\\"+"ld_saved_de_iter100_pop100_f05_cr07.csv",
    # folder+"\\"+"ld_saved_de_iter1000_pop10_f05_cr07.csv"

    # folder+"\\"+"ld_saved_de_pop10_iter1000_f05_cr07_no_candidate.csv",
    # folder+"\\"+"ld_saved_de_pop100_iter100_f05_cr07_no_candidate.csv",
    # folder+"\\"+"ld_saved_de_pop1000_iter10_f05_cr07_no_candidate.csv"
]
df_res = pd.DataFrame.from_dict({
        'FILE':[],
        'Rahang':[],
        'Total':[],
        'RMSE':[]
    })
df_res_ld = pd.DataFrame.from_dict({
        'FILE':[],
        'Rahang':[],
        'Landmark':[],
        'Total':[],
        'RMSE':[]
    })
def getarchname(archval):
    if archval == 0:
        return "BOTH"
    elif archval == 1:
        return "UPPER"
    else:
        return "LOWER"

def getldname(ldval):
    for ld in LandmarkType:
        if ld.value == ldval:
            return ld.name

for path_landmark_file in path_landmark_files:
    landmark_constant = import_landmark_def(path_landmark_file)
    data = generate_data()
    for vtp_path, ld_path in (zip(path_data_vtp, path_data_csv)):
        arch_type = ArchType.UPPER.value
        if "LOWER" in vtp_path:
            arch_type = ArchType.LOWER.value
        df_gt = pd.read_csv(ld_path, index_col=0)
        mesh = load(vtp_path)
        eigen_vec_mesh = extract_eigen_mesh(mesh)
        for tooth_type in landmark_constant[arch_type]:
            vertices_tooth, norm_vertices_tooth, norm_center_tooth = extract_mesh_tooth(mesh,tooth_type)
            if len(vertices_tooth) == 0:
                continue
            for landmark_type in landmark_constant[arch_type][tooth_type]:
                print(vtp_path, ArchType.UPPER.value, tooth_type, landmark_type)
                # if "NR" in vtp_path and "LOWER" in vtp_path:
                #     print(vertices_tooth)
                row = df_gt[(df_gt['label'] == tooth_type) & (df_gt['landmark'] == landmark_type)]
                landmark_point_gt = np.ndarray.flatten(np.array([row['x'], row['y'], row['z']]))
                landmark_point = get_landmark_point(landmark_constant[arch_type][tooth_type][landmark_type],
                                                    arch_type,
                                                    tooth_type,
                                                    landmark_type,
                                                    eigen_vec_mesh,
                                                    norm_center_tooth,
                                                    norm_vertices_tooth,
                                                    vertices_tooth)
                eu_error = find_distance_between_two_points(landmark_point_gt,landmark_point)
                se = math.pow(eu_error, 2)
                data[arch_type][tooth_type][landmark_type]['total'] = data[arch_type][tooth_type][landmark_type]['total'] + se
                data[arch_type][tooth_type][landmark_type]['n'] = data[arch_type][tooth_type][landmark_type]['n'] + 1


    both_rmse=0
    upper_rmse=0
    lower_rmse=0
    both_n = 0
    upper_n = 0
    lower_n = 0
    data_eval_ld={0:{}}
    for arch_type in data:
        if arch_type not in data_eval_ld:
            data_eval_ld[arch_type] = {}
        for tooth_type in data[arch_type]:
            for landmark_type in data[arch_type][tooth_type]:
                if landmark_type not in data_eval_ld[arch_type]:
                    data_eval_ld[arch_type][landmark_type]={
                        'total':0,
                        'n': 0,
                    }
                if landmark_type not in data_eval_ld[0]:
                    data_eval_ld[0][landmark_type] = {
                        'total': 0,
                        'n': 0,
                    }
                data_eval_ld[arch_type][landmark_type]['total'] = data_eval_ld[arch_type][landmark_type]['total'] + data[arch_type][tooth_type][landmark_type]['total']
                data_eval_ld[arch_type][landmark_type]['n'] = data_eval_ld[arch_type][landmark_type]['n'] + data[arch_type][tooth_type][landmark_type]['n']

                data_eval_ld[0][landmark_type]['total'] = data_eval_ld[0][landmark_type]['total'] + data[arch_type][tooth_type][landmark_type]['total']
                data_eval_ld[0][landmark_type]['n'] = data_eval_ld[0][landmark_type]['n'] + data[arch_type][tooth_type][landmark_type]['n']

                both_rmse += data[arch_type][tooth_type][landmark_type]['total']
                both_n += data[arch_type][tooth_type][landmark_type]['n']
                if arch_type == ArchType.LOWER.value:
                    lower_rmse+= data[arch_type][tooth_type][landmark_type]['total']
                    lower_n += data[arch_type][tooth_type][landmark_type]['n']
                if arch_type == ArchType.UPPER.value:
                    upper_rmse += data[arch_type][tooth_type][landmark_type]['total']
                    upper_n += data[arch_type][tooth_type][landmark_type]['n']

    for arch in data_eval_ld:
        for ld in data_eval_ld[arch]:
            total = data_eval_ld[arch][ld]['total']
            n = data_eval_ld[arch][ld]['n']
            rmse_final = math.sqrt(total / n)
            df_res_ld_temp = pd.DataFrame.from_dict({
                'FILE': [path_landmark_file],
                'Rahang': [getarchname(arch)],
                'Landmark': [getldname(ld)],
                'Total': [total],
                'RMSE': [rmse_final]
            })
            df_res_ld = pd.concat([df_res_ld, df_res_ld_temp], ignore_index=True)
    both_rmse_final = math.sqrt(both_rmse / both_n)
    upper_rmse_final = math.sqrt(upper_rmse / both_n)
    lower_rmse_final = math.sqrt(lower_rmse / both_n)
    df_arch = pd.DataFrame.from_dict({
        'FILE':[path_landmark_file,path_landmark_file,path_landmark_file],
        'Rahang':["BOTH","UPPER","LOWER"],
        'Total':[both_rmse, upper_rmse, lower_rmse],
        'RMSE':[both_rmse_final, upper_rmse_final, lower_rmse_final]
    })
    df_res = pd.concat([df_res, df_arch], ignore_index=True)
df_res.to_csv("hasil_evaluation_ld_based_on_arch_fcr_variation_no_candidate.csv",encoding='utf-8')
df_res_ld.to_csv("hasil_evaluation_ld_based_on_ld_fcr_variation_no_candidate.csv",encoding='utf-8')