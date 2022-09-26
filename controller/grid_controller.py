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
    if(event.actor and event.actor.name == "Grid Board" and self.var_state_grid['selected'] == None):
        self.var_state_grid['selected']="Grid Board"
        vsty = vtk.vtkInteractorStyleTrackballActor()
        change_plot_interaction(self, vsty)
    elif(self.var_state_grid['selected']==None and isinstance(self.model_plot.interactor.GetInteractorStyle(), vtk.vtkInteractorStyleTrackballCamera)):
        return
    elif((not event.actor) or event.actor.name != "Grid Board"):
        print('not touch grid')
        self.var_state_grid={
            'selected':None, # name 
        }
        vsty = vtk.vtkInteractorStyleTrackballCamera()
        change_plot_interaction(self, vsty)