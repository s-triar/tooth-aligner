from controller.summary_controller import calculate_studi_model
from utility.app_tool import get_saved_path
from utility.arch import Arch
from constant.enums import ArchType, ToothType,LandmarkType
from vedo import Line, Point
from PyQt5.QtWidgets import (
    QLabel,
    QFileDialog
    
)
from utility.colors import convert_landmark_to_color
import pandas as pd
from pathlib import Path  
from numpy import array

def init_var_landmarking(self):
    self.selected_q_label_landmark=None
    self.selected_arch_show_landmark=None
    self.var_landmarking={
        'index_model':0,
        'selected_arch':0,
        'selected_label':0,
        'selected_landmark':0
    }
    # self.var_history_landmarking=[] # [index_model, arch_id, label, landmark, id_point]

def set_selected_q_label_landmarking(self, obj):
    self.selected_q_label_landmark=obj

def set_selected_arch_show_landmarking(self, val):
    self.selected_arch_show_landmark=val
    

def reset_selected_q_label_landmarking(self):
    set_selected_q_label_landmarking(self, None)

def set_selected_face_label(self,landmark, tooth_label, arch_type):
    index_in_models = Arch._get_index_arch_type(arch_type)
    # self.var_landmarking={
    #     'index_model':index_in_models,
    #     'selected_arch':arch_type,
    #     'selected_label':tooth_label,
    #     'selected_landmark':landmark
    # }
    self.var_landmarking['index_model']=index_in_models
    self.var_landmarking['selected_arch']=arch_type
    self.var_landmarking['selected_label']=tooth_label
    self.var_landmarking['selected_landmark']=landmark
    

def change_point(self, event):
    if self.selected_q_label_landmark == None:
        return
    arch = self.models[self.var_landmarking['index_model']]
    tooth = arch.teeth[self.var_landmarking['selected_label']]
    msh = arch.mesh
    if msh == event.actor:
        coordinate = event.picked3d
        id_pt = msh.closestPoint(coordinate, N=1, returnPointId=True)
        # old_id = tooth.landmark_index[self.var_landmarking['selected_landmark']]
        # tooth.landmark_index[self.var_landmarking['selected_landmark']]=id_pt
        tooth.landmark_pt[self.var_landmarking['selected_landmark']]=coordinate
    # self.var_history_landmarking.push([self.var_landmarking['index_model'], self.var_landmarking['selected_arch'], self.var_landmarking['selected_label'], self.var_landmarking['selected_landmark'], old_id])
    
    # render?
        text = "[ {0:.3f} ; {1:.3f} ; {2:.3f} ]".format(coordinate[0],coordinate[1],coordinate[2])
        set_val_to_selected_q_label_landmarking(self, text)
        show_landmark(self)

# def apply_change_landmark(self):
#     self.var_history_landmarking=[]
#     # self.model_plot.add(self.models[-1].get_mesh())
#     self.model_plot.render()

# def reset_landmark(self):
#     for s in self.var_history_landmarking:
#         arch = self.models[s[0]].mesh
#         tooth = arch.teeth[s[2]]
#         tooth.landmark_index[s[3]]=s[4]
#     apply_change_landmark(self)

def set_val_to_selected_q_label_landmarking(self, text):
    self.selected_q_label_landmark.setText(text)

def draw_eigen_arch(self):
    # arch = self.models[self.selected_arch_show_landmark['index_model']]
    arch = get_selected_arch_landmark(self)
    eigen_vec_mesh=[]
    eigen_vec_mesh.append(arch.right_left_vec)
    eigen_vec_mesh.append(arch.forward_backward_vec)
    eigen_vec_mesh.append(arch.upward_downward_vec)

    center = arch.mesh.centerOfMass()
    return eigen_vec_mesh, center
    # eig_pts = draw_eigen_vec(eigen_vec_mesh, center)
    # self.model_plot.add(eig_pts)

def draw_eigen_vec(eigen_vec, center):
    left_right = eigen_vec[0]
    forward_backward = eigen_vec[1]
    upward_downward = eigen_vec[2]
    line_lr = Line(center-left_right, center+left_right, c="red")
    line_fb = Line(center-forward_backward, center+forward_backward, c="green")
    line_ud = Line(center-upward_downward, center+upward_downward, c="blue")
    point_lr = Point((center-left_right), c="red", r=15)
    point_fb = Point((center-forward_backward), c="green", r=15)
    point_ud = Point((center-upward_downward), c="blue", r=15)
    point_lr2 = Point((center+left_right), c="pink", r=15)
    point_fb2 = Point((center+forward_backward), c="yellow", r=15)
    point_ud2 = Point((center+upward_downward), c="violet", r=15)
    return [line_lr, line_fb, line_ud, point_fb, point_fb2, point_lr, point_lr2, point_ud, point_ud2]

def draw_landmark_point(self):
    pass

def get_selected_arch_landmark(self):
    arch =  self.models[Arch._get_index_arch_type(self.selected_arch_show_landmark)]
    return arch

def show_landmark(self):
    
    arch =  get_selected_arch_landmark(self)
    teeth = arch.teeth
    
    for child in self.landmark_panel_widget_container.findChildren(QLabel):
        if('coordinate_ld_' in child.objectName() ):
            obj_names = child.objectName().split('_')
            arch_id = int(obj_names[2])
            if(arch.arch_type == arch_id):
                tooth_label = int(obj_names[3])
                landmark_label = int(obj_names[4])
                if(tooth_label in teeth):
                    # if landmark_label!= 3 and landmark_label!=4:
                        tooth = teeth[tooth_label]
                        # landmark = tooth.landmark_index[landmark_label]
                        # coordinate = arch.mesh.points(landmark)
                        coordinate = tooth.landmark_pt[landmark_label]
                        text = "[ {0:.3f} ; {1:.3f} ; {2:.3f} ]".format(coordinate[0],coordinate[1],coordinate[2])
                        child.setText(text)
                        p=Point(coordinate,c=convert_landmark_to_color(landmark_label),r=20)
                        self.model_plot.add(p) 
    self.model_plot.render()
    
def save_landmark(self):
    cur_step = self.step_model.get_current_step()
    for a in ArchType:
        idx = Arch._get_index_arch_type(a.value)
        path_model = self.model_paths[idx]
        path_save_landmark=get_saved_path(path_model,".csv","_landmark_"+a.name+"_",cur_step,False)
        # path_save_landmark = path_model.split(".")
        # path_save_landmark = ".".join(path_save_landmark[:-1])
        # path_save_landmark = path_save_landmark+"_step_"+cur_step+".csv"
        landmark_dict = {}
        landmark_dict["label"]=[]
        landmark_dict["landmark"]=[]
        landmark_dict["x"]=[]
        landmark_dict["y"]=[]
        landmark_dict["z"]=[]
        model = self.models[idx]
        teeth = model.teeth
        for tooth in teeth:
            for ld in teeth[tooth].landmark_pt:
                pt = teeth[tooth].landmark_pt[ld]
                if(pt is not None):
                    landmark_dict["x"].append(pt[0])
                    landmark_dict["y"].append(pt[1])
                    landmark_dict["z"].append(pt[2])
                    landmark_dict["landmark"].append(ld)
                    landmark_dict["label"].append(tooth)
        df = pd.DataFrame(data=landmark_dict)
        filepath = Path(path_save_landmark)  
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        df.to_csv(filepath)  
        
def load_landmark(self, typearch, filename):
    print(filename)    
    df = pd.read_csv(filename, index_col=0)
    
    
    index_in_models = Arch._get_index_arch_type(typearch)
    arch = self.models[index_in_models]
    for index, row in df.iterrows():
        tooth = arch.teeth[row['label']]
        tooth.landmark_pt[row['landmark']]=array([row['x'],row['y'],row['z']])
    calculate_studi_model(self)
    # load_model(self, filenames[0], arch_type)
    # btn.setDisabled(True)
    # check_btn_toggle_arch(self, arch_type, True)