from pathlib import Path  
from dotenv import load_dotenv
import os
import enum
import pandas as pd
import glob
from constant.enums import ArchType, ToothType
from utility import landmarking_lib as ll
import numpy as np
from vedo import load
# class ArchType(enum.Enum):
#     UPPER=1
#     LOWER=2





def get_saved_path(path_model, extendsion,more_info='',cur_step=None, isProject=False):
    load_dotenv()
    save_path = os.getenv("SAVE")
    c=path_model.split(os.altsep)
    file = c[-1]
    sign_jaw = os.getenv(ArchType.LOWER.name)
    if(os.getenv(ArchType.UPPER.name) in file.lower()):
        sign_jaw = os.getenv(ArchType.UPPER.name)
    file_chunk = file.split(' ')
    person = ''
    for f in file_chunk:
        if(sign_jaw in f.lower()):
            break
        if(person!=''):
            person+=" "
        person+=f
    str_cur_step = str(cur_step)
    if(isProject==False):
        return os.path.join(save_path,person,"step_"+str_cur_step,person+more_info+"_step_"+str_cur_step+extendsion)
    else:
        return os.path.join(save_path,person,person+extendsion)
    

def get_landmark(arch_type, personname):
    load_dotenv()
    save_path = os.getenv("SAVE")
    arch_name = ArchType.UPPER.name if arch_type == ArchType.UPPER.value else ArchType.LOWER.name
    df=None
    for person_folder in glob.glob(save_path+"/*"):
        if personname in person_folder:
            for step in glob.glob(person_folder+"/*"):
                for file_step in glob.glob(step+"/*"+arch_name+"*.csv"):
                    df = pd.read_csv(file_step, index_col=0)
                    break
    return df
# untuk proses landmark model
def load_all_landmarks(arch_type, tooth_label, landmark_type):
    load_dotenv()
    save_path = os.getenv("SAVE")
    incisor_teeth = [
                    ToothType.INCISOR_UL2_LR2.value, 
                    ToothType.INCISOR_UL1_LR1.value,
                    ToothType.INCISOR_UR1_LL1.value,
                    ToothType.INCISOR_UR2_LL2.value
                ]
    arch_name = ArchType.UPPER.name if arch_type == ArchType.UPPER.value else ArchType.LOWER.name
    df_hasil = pd.DataFrame()
    for person_folder in glob.glob(save_path+"/*"):
        person_name = person_folder.split("\\")[-1] #!!!!!!!!!!!!
        for step in glob.glob(person_folder+"/*"):
            mesh = None
            right_left_vec = None
            forward_backward_vec = None
            upward_downward_vec = None
            for file_step in glob.glob(step+"/*"+arch_name+"*.vtp"):
                mesh = load(file_step)
                N = mesh.NCells()
                labels = np.unique(mesh.celldata['Label'])
                center_mesh = mesh.centerOfMass()
                points_mesh = np.array(mesh.points())
                idx_faces_mesh = np.array(mesh.cells())
                points_mesh_normalized = points_mesh-center_mesh
                eigen_val_mesh, eigen_vec_mesh = ll.getEigen(points_mesh_normalized, idx_faces_mesh, mesh.celldata['Label'], incisor_teeth)
                right_left_vec = eigen_vec_mesh[0]
                forward_backward_vec = eigen_vec_mesh[1]
                upward_downward_vec = eigen_vec_mesh[2]
            for file_step in glob.glob(step+"/*"+arch_name+"*.csv"):
                
                df = pd.read_csv(file_step, index_col=0)
                df2 = df.loc[
                    (df['label'] == tooth_label) & (df['landmark'] == landmark_type)
                ]
                df2.insert(0,"person",[person_name]*len(df2),True)
                df2.insert(len(df2.columns),"right_left_vec_x",[right_left_vec[0]]*len(df2),True)
                df2.insert(len(df2.columns),"right_left_vec_y",[right_left_vec[1]]*len(df2),True)
                df2.insert(len(df2.columns),"right_left_vec_z",[right_left_vec[2]]*len(df2),True)
                df2.insert(len(df2.columns),"forward_backward_vec_x",[forward_backward_vec[0]]*len(df2),True)
                df2.insert(len(df2.columns),"forward_backward_vec_y",[forward_backward_vec[1]]*len(df2),True)
                df2.insert(len(df2.columns),"forward_backward_vec_z",[forward_backward_vec[2]]*len(df2),True)
                df2.insert(len(df2.columns),"upward_downward_vec_x",[upward_downward_vec[0]]*len(df2),True)
                df2.insert(len(df2.columns),"upward_downward_vec_y",[upward_downward_vec[1]]*len(df2),True)
                df2.insert(len(df2.columns),"upward_downward_vec_z",[upward_downward_vec[2]]*len(df2),True)
                df2.insert(len(df2.columns),"arch_name",[arch_name]*len(df2),True)
                
                df_hasil = pd.concat([df2,df_hasil])
    return df_hasil
    
if __name__ == '__main__':
    # print(ArchType.LOWER.name)
    # a=r'D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segement_refine_manual/Gerry Sihaj LowerJawScan Cleaned 10000_d_predicted_refined a.vtp'
    # g = get_saved_path(a,".csv",4,isProject=False)
    # print(g)
    # filepath = Path(g)  
    # filepath.parent.mkdir(parents=True, exist_ok=True) 
    # for i in range(1):
    #     print(i)
    pass
    
    