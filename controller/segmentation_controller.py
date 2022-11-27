
from controller.summary_controller import calculate_studi_model
from utility.app_tool import get_saved_path
from utility.arch import Arch
from utility.colors import convert_label_to_color
import pandas as pd
from pathlib import Path  
from constant.enums import ArchType, ToothType,LandmarkType
from vedo import write


def init_var_segmentation(self):
    self.var_segmentation={
        'index_model':0,
        'selected_arch':0,
        'selected_label':0
    }
    self.var_history_segmentation=[] # [index_model, arch_id, idx_face, label]
    
def set_selected_arch(self, val):
    set_selected_face_label(self, val, self.var_segmentation['selected_label'])

def set_selected_label(self, val):
    set_selected_face_label(self, self.var_segmentation['selected_arch'], val)
    
def set_selected_face_label(self, arch_type, tooth_label ):
    index_in_models = Arch._get_index_arch_type(arch_type)
    self.var_segmentation={
        'index_model':index_in_models,
        'selected_arch':arch_type,
        'selected_label':tooth_label
    }

def change_face_label(self, event):
    
    msh = self.models[self.var_segmentation['index_model']].mesh
    if(event.actor==msh):
        id_cell = msh.closestPoint(event.picked3d, N=1, returnCellId=True)
        old_label = msh.celldata['Label'][id_cell]
        self.var_history_segmentation.append([self.var_segmentation['index_model'], self.var_segmentation['selected_arch'], id_cell, old_label])
        msh.celldata['Label'][id_cell]=self.var_segmentation['selected_label']
        msh.celldata['Label'][id_cell]=self.var_segmentation['selected_label']
        color = convert_label_to_color(self.var_segmentation['selected_label'])
        msh.celldata['Color'][id_cell] = color
        msh.celldata.select('Color')
        # self.models[self.var_segmentation['index_model']].mesh=msh
        self.model_plot.render()
    dis_enable_apply_undo_reset_button(self)

def dis_enable_apply_undo_reset_button(self):
    if(len(self.var_history_segmentation)>0):
        self.btn_apply_segmentation.setEnabled(True)
        self.btn_undo_segmentation.setEnabled(True)
        self.btn_reset_segmentation.setEnabled(True)
    else:
        self.btn_undo_segmentation.setEnabled(False)
        self.btn_apply_segmentation.setEnabled(False)
        self.btn_reset_segmentation.setEnabled(False)

def apply_change_segmantation(self):
    self.var_history_segmentation=[]
    calculate_studi_model(self)
    # self.model_plot.add(self.models[-1].get_mesh())
    self.model_plot.render()
    dis_enable_apply_undo_reset_button(self)
    

def reset_change_segmentation(self):
    for s in self.var_history_segmentation:
        msh = self.models[s[0]].mesh
        msh.celldata['Label'][s[2]]=s[3]
        color = convert_label_to_color(s[3])
        msh.celldata['Color'][s[2]] = color
        msh.celldata.select('Color')
    apply_change_segmantation(self)
        
def undo_change_segmentation(self):
    if(len(self.var_history_segmentation)>0):
        s = self.var_history_segmentation.pop()
        msh = self.models[s[0]].mesh
        msh.celldata['Label'][s[2]]=s[3]
        color = convert_label_to_color(s[3])
        msh.celldata['Color'][s[2]] = color
        msh.celldata.select('Color')
        self.model_plot.render()
    calculate_studi_model(self)
    dis_enable_apply_undo_reset_button(self)


def save_segmentation(self):
    cur_step = self.step_model.get_current_step()
    for a in ArchType:
        idx = Arch._get_index_arch_type(a.value)
        path_model = self.model_paths[idx]
        model = self.models[idx]
        path_save = get_saved_path(path_model,".vtp","_"+a.name+"_",cur_step,False)
        filepath = Path(path_save)  
        filepath.parent.mkdir(parents=True, exist_ok=True) 
        write(model.mesh,path_save)
        