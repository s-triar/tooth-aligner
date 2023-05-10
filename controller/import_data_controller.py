from vedo import load
from constant.enums import ArchType
from controller.step_controller import update_transform_arch
from controller.summary_controller import calculate_studi_model
from utility.app_tool import get_saved_path
from utility.arch import Arch
from pathlib import Path  
import pandas as pd
import os
import glob
from dotenv import load_dotenv
import re
from numpy import array



def load_model(self, path, id):
    model_vedo = load(path)
    model = Arch(id, model_vedo, skip_extract_tooth=True)
    self.models.append(model)
    self.model_paths.append(path)
    self.model_plot.add(self.models[-1].get_mesh())
    self.model_plot.addGlobalAxes(axtype=8)
    self.model_plot.resetCamera()
    # calculate_studi_model(self)
    print(path) #D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segement_refine_manual/Gerry Sihaj LowerJawScan Cleaned 10000_d_predicted_refined a.vtp
    
def load_landmark(self, typearch, filename):
    print(filename)    
    df = pd.read_csv(filename, index_col=0)
    
    
    index_in_models = Arch._get_index_arch_type(typearch)
    arch = self.models[index_in_models]
    for index, row in df.iterrows():
        tooth = arch.teeth[row['label']]
        tooth.landmark_pt[row['landmark']]=array([row['x'],row['y'],row['z']])


def reset_model(self):
    self.model_plot.clear()
    Arch._clear()
    self.models = []
    self.model_paths = []
    self.model_plot.render()

def check_archs_loaded(self):
    return Arch._is_complete()


def load_opt_model(self, path):
    load_dotenv()
    
    c=path.split(os.altsep)
    a=os.altsep.join(c[:-1])
    i=0
    files = glob.glob(a+"/*")
    files.sort(key=lambda x:[int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])
    print(files)
    for step_folder in files:
        if(".json" not in step_folder):
            index = step_folder.split("step_")[-1]
            if(index!=0 and index != "0"):
                self.btn_addmin_step_aligner.btn_increase.click()
                
            reset_model(self)

            for model in glob.glob(step_folder+"/*.vtp"):
                sign_jaw = ArchType.LOWER.value
                print(model.lower())
                if(ArchType.UPPER.name.lower() in model.lower()):
                    sign_jaw = ArchType.UPPER.value

                load_model(self, model, sign_jaw)
            if(i==0):
                if(Arch._is_complete()):
                    temp={
                        ArchType.LOWER.value:None,
                        ArchType.UPPER.value:None
                    }
                    temp_teeth={
                        ArchType.LOWER.value:None,
                        ArchType.UPPER.value:None
                    }
                    for a in ArchType:
                        idx = Arch._get_index_arch_type(a.value)
                        m = self.models[idx]
                        temp[a.value]=m.mesh.clone()
                        temp_teeth[a.value]=m.teeth.copy()
                    self.step_model.add_step_model(temp, temp_teeth)
                    
                    self.attachment_model.copy_attachment(0,0+1)
                    i+=1
                
            for ld in glob.glob(step_folder+"/*.csv"):
                sign_jaw = ArchType.LOWER.value
                if(ArchType.UPPER.name.lower() in ld.lower()):
                    sign_jaw = ArchType.UPPER.value
                load_landmark(self, sign_jaw, ld)
            calculate_studi_model(self, all=not (index!=0 and index != "0"))    
            if(index!=0 and index != "0"):
                update_transform_arch(self,self.step_model.get_current_step())
                # load landmark
    self.btn_import_reset.setDisabled(True)