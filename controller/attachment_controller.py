from utility.attachment_model import AttachmentModel
from vedo import vtk, Box, Mesh, vtk2numpy
import time
import numpy as np

def init_var_attachment(self):
    self.attachment_model=AttachmentModel()
    self.var_state_attachment={
        'selected':None, # name or 'create' or 'delete'
        'step':None,
        'arch':None,
        'width':None
    }

def transform_attachment_on_tooth(self, label, rotate_type, val_rot, is_rad, center_pivot):
    attachs, archs, steps, index_k = self.attachment_model.get_attachment_from_label(label)
    for at, ar, st, idx in zip(attachs, archs, steps, index_k):
        mesh =at.mesh
        if(rotate_type=="pitch"):
            mesh.rotateX(val_rot, is_rad, center_pivot)
        elif(rotate_type=="yaw"):
            mesh.rotateY(val_rot, is_rad, center_pivot)
        elif(rotate_type=="roll"):
            mesh.rotateZ(val_rot, is_rad, center_pivot)
        self.attachment_model.update_attachment_with_new_mesh(ar, st, idx, mesh)

def prep_reset_attachment_state(self):
    self.var_state_attachment={
        'selected':None, # name or 'create' or 'delete'
        'step':None,
        'arch':None,
        'width':None
    }

def prep_new_attachment(self, w):
    self.var_state_attachment['selected']='create'
    self.var_state_attachment['width']=w
    
def prep_delete_attachment(self):
    self.var_state_attachment['selected']='delete'
    self.var_state_attachment['width']=None
    
def change_plot_interaction(self, interaction):
    # self.model_plot.interactor.ExitCallback()
    self.model_plot.interactor.SetInteractorStyle(interaction)
    self.model_plot.interactor.Start()
    self.model_plot.render()

def reset_plot_interaction(self):
    vsty = vtk.vtkInteractorStyleTrackballCamera()
    change_plot_interaction(self, vsty)

def toggle_plot_interaction(self):
    # cur = self.var_state_attachment['plot_interaction']
    cur = self.model_plot.interactor.GetInteractorStyle()
    if isinstance(cur, vtk.vtkInteractorStyleTrackballActor):
        vsty = vtk.vtkInteractorStyleTrackballCamera()
        change_plot_interaction(self,vsty)
        
    elif isinstance(cur, vtk.vtkInteractorStyleTrackballCamera):
        vsty = vtk.vtkInteractorStyleTrackballActor()
        change_plot_interaction(self, vsty)
        
def mouse_click_attachment(self,event):
    # if(event.actor):
    #     print(event.actor.name)
    archs = []
    for a in self.models:
        archs.append(a.mesh)
        
        
    # apply new attachment
    if(self.var_state_attachment['selected']=='create'):
        pts = event.picked3d
        for m in self.models:
            if (m.mesh == event.actor):
                teeth_center=[m.teeth[k].center for k in m.teeth]
                diff = np.abs(np.subtract(teeth_center, [event.picked3d]))
                sm = np.sum(diff, axis=1)
                index = np.argmin(sm)
                label = m.teeth[index+1].label
                
                self.var_state_attachment['arch']=m.arch_type
                self.var_state_attachment['step']=self.step_model.get_current_step()
                b = Box(pts,self.var_state_attachment['width'],1,1,c='black')
                N = b.NCells()
                pts = vtk2numpy(b.polydata().GetPoints().GetData()) #vertices (coordinate)
                ids = vtk2numpy(b.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:]
                n = 'attachment_'+str(int(round(time.time() * 1000)))
                b= Mesh([pts,ids],c=(200,190,200))
                b.name = n
                print("add attachment on step",self.var_state_attachment['step'])
                self.attachment_model.add_attachment(self.var_state_attachment['arch'], self.var_state_attachment['step'], b, n, label)
                self.model_plot.add(b)
                self.var_state_attachment['selected']=n
                if(self.var_state_attachment['width']==3):
                    self.btn_attachment_rectangular_3.setChecked(False)
                elif(self.var_state_attachment['width']==4):
                    self.btn_attachment_rectangular_4.setChecked(False)
                elif(self.var_state_attachment['width']==5):
                    self.btn_attachment_rectangular_5.setChecked(False)
                self.model_plot.render()
                # print('apply attachment')
                # print(self.var_state_attachment)
                break

        # return
    
    
    
    # delete attachment
    elif(self.var_state_attachment['selected']=='delete' and event.actor and (not (event.actor in archs))):
        ar, st = self.attachment_model.get_arch_and_step_from_name(event.actor.name)
        self.attachment_model.delete_attachment(ar,st,event.actor.name)
        self.model_plot.remove(event.actor)
        self.btn_delete_attachment.setChecked(False)
        # print('delete attachment')
        # print(self.var_state_attachment)
        # return
        
    # select attachment first
    elif event.actor and (not (event.actor in archs)) and self.var_state_attachment['selected'] != event.actor.name:
        ar, st = self.attachment_model.get_arch_and_step_from_name(event.actor.name)
        self.var_state_attachment={
            'selected':event.actor.name, # name or 'create'
            'step':st,
            'arch':ar,
            'width':None
        }
        # print('touch attachment')
        # print(self.var_state_attachment)
        vsty = vtk.vtkInteractorStyleTrackballActor()
        change_plot_interaction(self, vsty)
        # self.model_plot.render()
        
        # return
    
    elif(self.var_state_attachment['selected']==None and isinstance(self.model_plot.interactor.GetInteractorStyle(), vtk.vtkInteractorStyleTrackballCamera)):
        
        return
    
    elif(event.actor in archs) or (not event.actor):
        # print('not touch attachment')
        self.var_state_attachment={
            'selected':None, # name or 'create'
            'step':None,
            'arch':None,
            'width':None
        }
        vsty = vtk.vtkInteractorStyleTrackballCamera()
        change_plot_interaction(self, vsty)
        # self.model_plot.render()
    
    