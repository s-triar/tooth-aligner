from controller.vedo_plotter_controller import remove_not_arch
from utility.arch import Arch
from utility.step_model import StepModel
from constant.enums import ArchType

def init_var_step(self):
    self.step_model=StepModel()

def update_transform_arch(self, e):
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
    self.step_model.update_step_model(e,temp, temp_teeth)

def add_transform_arch(self, e): #save arch transform when add step    
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
        temp[a.value]=m.mesh
        temp[a.value]=m.mesh.clone()
        temp_teeth[a.value]=m.teeth.copy()
    self.step_model.add_step_model(temp, temp_teeth)
    # if(e>0):
    self.attachment_model.copy_attachment(e,e+1)

def remove_transform_arch(self, e): #remove arch transform when add step
    self.step_model.remove_step_model(self.models)

def change_step(self, e):
    
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
        temp[a.value]=m.mesh
        temp[a.value]=m.mesh.clone()
        temp_teeth[a.value]=m.teeth.copy()
        
    self.step_model.update_current(temp, temp_teeth)
    
    self.step_model.change_current_step(e)
    apply_transform_arch(self,e)
    
# def generate_view(self, e): # based on what panel is showing
    
#     self.models=self.step_model.get_step_model(e)    
#     self.model_plot.add()

def apply_transform_arch(self,e): # based on what panel is showing
    print("ck",len(self.step_model.step_models))
    if(e<=len(self.step_model.step_models)):
        try:
            mdls, teeth=self.step_model.get_step_model(e)
            remove_not_arch(self)
            for a in ArchType:
                idx = Arch._get_index_arch_type(a.value)
                self.models[idx].mesh = mdls[a.value].clone()
                self.models[idx].teeth = teeth[a.value].copy()
            for m in self.models:
                self.model_plot.add(m.mesh)
                m.mesh.celldata.select('Color')
            res = self.attachment_model.get_attachment_on_step(e)
            print("resres",res)
            for a_res in res:
                if(res[a_res]):
                    for ee in res[a_res]:
                        self.model_plot.add(ee.mesh)
            self.model_plot.render()
        except:
            print()
    
    

