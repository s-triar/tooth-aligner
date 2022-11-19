from vedo import vtk, Box, Mesh, vtk2numpy
import time
import numpy as np

def init_var_grid(self):
    self.var_state_grid={
        'selected':None, # name "Grid Board"
    }

def change_plot_interaction(self, interaction):
    # self.model_plot.interactor.ExitCallback()
    self.model_plot.interactor.SetInteractorStyle(interaction)
    self.model_plot.interactor.Start()
    self.model_plot.render()

def reset_plot_interaction(self):
    vsty = vtk.vtkInteractorStyleTrackballCamera()
    change_plot_interaction(self, vsty)

def mouse_click_grid(self,event):
    print(event)
    ff = self.model_plot.camera.GetDirectionOfProjection()
    ff_asli =np.array([ff[0],ff[1],ff[2]])
    ff =np.array([abs(ff[0]),abs(ff[1]),abs(ff[2])])
    ff_index = np.argmax(ff)
    new_pos = []
    y = 70 if ff_asli[ff_index] < 0 else -70
    if(ff_index==0):
        new_pos = [y,0,0]
    elif(ff_index==1):
        new_pos=[0,y,0]
    elif(ff_index==2):
        new_pos=[0,0,y]
    for a in self.model_plot.actors:
        if("Grid Board" in a.name ):
            a.SetPosition(new_pos)
    # if(event.actor and event.actor.name == "Grid Board" and self.var_state_grid['selected'] == None):
    #     self.var_state_grid['selected']="Grid Board"
    #     vsty = vtk.vtkInteractorStyleTrackballActor()
    #     change_plot_interaction(self, vsty)
    # elif(self.var_state_grid['selected']==None and isinstance(self.model_plot.interactor.GetInteractorStyle(), vtk.vtkInteractorStyleTrackballCamera)):
    #     return
    # elif((not event.actor) or event.actor.name != "Grid Board"):
    #     print('not touch grid')
    #     self.var_state_grid={
    #         'selected':None, # name 
    #     }
    #     vsty = vtk.vtkInteractorStyleTrackballCamera()
    #     change_plot_interaction(self, vsty)