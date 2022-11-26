from constant.enums import ArchType, PanelMode
from controller.attachment_controller import mouse_click_attachment
from controller.grid_controller import mouse_click_grid
from controller.landmarking_controller import change_point
from controller.rotation_controller import mouse_click_rotation
from controller.segmentation_controller import change_face_label

def init_var_vedo_model(self):
    self.models = []
    self.model_paths=[]
    self.plot_click_mode=None

def remove_not_arch(self, not_archs=None, excepts=None, excepts_name_like=None):
    if(not_archs==None):
        arch = excepts if excepts != None else []
        for m in self.models:
            if (ArchType.LOWER.value == m.arch_type or ArchType.UPPER.value == m.arch_type):
                arch.append(m.mesh)
        notArchs = []
        for a in self.model_plot.actors:
            if (a not in arch):
                if(excepts_name_like==None):
                    notArchs.append(a)
                elif(not (excepts_name_like in a.name )):
                    notArchs.append(a)
        if len(notArchs) > 0:
            self.model_plot.clear(actors=notArchs, at=0)
    else:
        self.model_plot.clear(actors=not_archs, at=0)
    self.model_plot.render()
    
def set_plot_click_mode(self, val):
    self.plot_click_mode=val

def reset_plot_click_mode(self):
    set_plot_click_mode(self, None)
    
def vedo_plot_mouse_click(self, event):
    if(self.plot_click_mode == PanelMode.SEGMENTATION.value):
        change_face_label(self,event)
    elif(self.plot_click_mode == PanelMode.LANDMARK.value):
        change_point(self, event)
        # remove_not_arch(self,excepts=self.eigen_landmarking_paints)
    elif(self.plot_click_mode == PanelMode.ROTATION.value):
        remove_not_arch(self, excepts_name_like='attachment')
        mouse_click_rotation(self, event)
    elif(self.plot_click_mode == PanelMode.ATTATCHMENT.value):
        mouse_click_attachment(self, event)
        self.model_plot.render()
    elif(self.plot_click_mode==PanelMode.GRID.value):
        mouse_click_grid(self, event)
        self.model_plot.render()
        
    else:
        pass