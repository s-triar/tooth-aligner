from constant.root_length import RootLength
import numpy as np
from vedo import load, Mesh, Point, vtk2numpy, Spline, KSpline, CSpline, Line

from controller.attachment_controller import transform_attachment_on_tooth

def init_var_rotation(self):
    self.tooth_selected_rotation={
        "label":None,
        "mode":None, # mesial, distal, out (buccal or labial), in (lingual or palatal), cusp, pit
        "index":None
    }
    self.mesh_selected_rotation = {
        'arch_type': '',
        'arch': None
    }

def get_point_in_root(self, mesh, arch_type, label):
    # tooth center
    tooth_center = self.mesh_selected_rotation['arch'].teeth[self.tooth_selected_rotation['label']].center
    # room center 
    # i_s_p = get_boundary_mesh(mesh, faces)
    i_s_p = mesh.boundaries(returnPointIds=True)
    pts_boundary = mesh.points()[i_s_p]
    mean_pts_boundary = np.mean(pts_boundary, axis=0)        
    
    # root size
    root_length = RootLength.archs[arch_type][label]
    
    v = mean_pts_boundary-tooth_center
    vv=np.linalg.norm(v)
    u = v/vv
    dd=vv+root_length
    root_point = np.array(mean_pts_boundary) + (dd*u)
    
    # p = Point(tooth_center,r=20,c='green')
    # self.model_plot.add(p)
    
    # p = Point(root_point,r=20,c='black')
    # self.model_plot.add(p)
    
    # p = Point(mean_pts_boundary,r=20,c='blue')
    
    # self.model_plot.add(p)
    
    return root_point, mean_pts_boundary, tooth_center


def do_rotate(self, type, val_rotate, d_root):
    model = self.mesh_selected_rotation['arch']
    modelpoints = vtk2numpy(self.mesh_selected_rotation['arch'].mesh.polydata().GetPoints().GetData())
    verts = modelpoints
    # faces = model.info['labels'][self.mesh_selected_rotation['label']]['cells']
    faces = model.teeth[self.tooth_selected_rotation['label']].index_vertice_cells
    mesh = Mesh([verts, faces])
    faces_unique = np.unique(faces)
    # bdr = mesh.boundaries().points()
    # idx_bdr = []
    # for b in bdr:
    #     itemp = np.where(modelpoints == b)
    #     for jb in np.unique(itemp[0]):
    #         idx_bdr.append(jb)
    idx_bdr = mesh.boundaries(returnPointIds=True)

    # for b in idx_bdr:
    #     pt=Point(modelpoints[b],r=20,c='pink')
    #     self.model_plot.add(pt)
    idx_for_faces = []
    for b in idx_bdr:
        itemp = np.where(faces_unique == b)
        for jb in np.unique(itemp[0]):
            idx_for_faces.append(jb)
    faces_unique = np.delete(faces_unique, idx_for_faces)
    # teeth_center = self.mesh_selected_rotation['model'].info['centers'][self.mesh_selected_rotation['label'].astype(int)]
    teeth_center = model.teeth[self.tooth_selected_rotation['label']].center
    
    # detect collision
    label_before=self.tooth_selected_rotation['label']-1
    label_after=self.tooth_selected_rotation['label']+1
    
    mesh_tooth_before_before_rotation=None
    mesh_tooth_after_before_rotation=None
    
    if(label_before>0):
        faces_before = model.teeth[label_before].index_vertice_cells
        mesh_tooth_before_before_rotation = Mesh([verts, faces_before])
    if(label_after<15):
        faces_after = model.teeth[label_after].index_vertice_cells
        mesh_tooth_after_before_rotation = Mesh([verts, faces_after])
    
    pts_col_before_before_rotation=[]
    pts_col_after_before_rotation=[]
    if(mesh_tooth_before_before_rotation!=None):
        col_before = mesh.clone().cutWithMesh(mesh_tooth_before_before_rotation)
        pts_col_before_before_rotation=col_before.points()

    if(mesh_tooth_after_before_rotation!=None):
        col_after = mesh.clone().cutWithMesh(mesh_tooth_after_before_rotation)
        pts_col_after_before_rotation=col_after.points()
    
    root_point, mean_pts_boundary, tooth_center = get_point_in_root(self, mesh, self.mesh_selected_rotation["arch_type"], self.tooth_selected_rotation['label'])
    

    v=mean_pts_boundary-root_point
    vv=np.linalg.norm(v)
    u = v/vv
    dd=vv-d_root
    new_center = np.array(root_point) + (dd*u)

    new_new_center=(new_center[0], new_center[1], new_center[2])
    if(type=="pitch"):
        mesh.rotateX(val_rotate, False, new_new_center)
    elif(type=="yaw"):
        mesh.rotateY(val_rotate, False, new_new_center)
    elif(type=="roll"):
        mesh.rotateZ(val_rotate, False, new_new_center)
    
    # detect collision
    mesh_tooth_before=None
    mesh_tooth_after=None
    
    if(label_before>0):
        faces_before = model.teeth[label_before].index_vertice_cells
        mesh_tooth_before = Mesh([verts, faces_before])
    if(label_after<15):
        faces_after = model.teeth[label_after].index_vertice_cells
        mesh_tooth_after = Mesh([verts, faces_after])
    
    pts_col_before=[]
    pts_col_after=[]
    if(mesh_tooth_before!=None):
        col_before = mesh.clone().cutWithMesh(mesh_tooth_before)
        pts_col_before=col_before.points()

    if(mesh_tooth_after!=None):
        col_after = mesh.clone().cutWithMesh(mesh_tooth_after)
        pts_col_after=col_after.points()
    # print(len(pts_col_before), len(pts_col_after))
    if(len(pts_col_before)>len(pts_col_before_before_rotation)):
        text = 'Collided with tooth label '+str(label_before)
        print(text)
        # change_log(self, text)
    elif(len(pts_col_after)>len(pts_col_after_before_rotation)):
        text = 'Collided with tooth label '+str(label_after)
        # change_log(self, text)
        print(text)
    else:
        text = "Model: {0}. Label: {1}".format(str(self.mesh_selected_rotation["arch_type"]), str(int(self.tooth_selected_rotation["label"])))
        # change_log(self, text)
        print(text)
    print('before',len(pts_col_before),len(pts_col_before_before_rotation))
    print('after',len(pts_col_after),len(pts_col_after_before_rotation))
    temp_p = self.mesh_selected_rotation['arch'].mesh.points()
    temp_p[faces_unique] = mesh.points()[faces_unique]
    mesh_transform = mesh.getTransform()
    
    transform_attachment_on_tooth(self, self.tooth_selected_rotation['label'], type, val_rotate, False, new_new_center)
    self.mesh_selected_rotation['arch'].mesh.points(temp_p)
    self.mesh_selected_rotation['arch'].extract_tooth()
    self.model_plot.render()
    
    # remove_not_arch(self)
    # self.mesh_selected_rotation['model'].extract_center_tooth_holes()
    # self.mesh_selected_rotation['model'].extract_mesial_distal_points()
    # self.mesh_selected_rotation['model'].calculate_bolton_analysis()


def pitch(self, rotate_type, d_root):
    val_rotate = +1 if rotate_type == '+' else -1
    do_rotate(self,"pitch",val_rotate, d_root)


def yaw(self, rotate_type, d_root):
    val_rotate = +1 if rotate_type == '+' else -1
    do_rotate(self,"yaw",val_rotate, d_root)

def roll(self, rotate_type, d_root):
    val_rotate = +1 if rotate_type == '+' else -1
    do_rotate(self,"roll",val_rotate, d_root)
    
def mouse_click_rotation(self, event):
    # print('masuk mouse click rotation')
    self.tooth_selected_rotation={
        "label":None,
        "mode":None, # mesial, distal, out (buccal or labial), in (lingual or palatal), cusp, pit
        "index":None
    }
    self.mesh_selected_rotation = {
        'arch_type': '',
        'arch': None
    }
    if not event.actor:
        self.btn_pitch.btn_increase.setDisabled(True)
        self.btn_pitch.btn_decrease.setDisabled(True)
        self.btn_roll.btn_increase.setDisabled(True)
        self.btn_roll.btn_decrease.setDisabled(True)
        self.btn_yaw.btn_increase.setDisabled(True)
        self.btn_yaw.btn_decrease.setDisabled(True)
        return
    for m in self.models:
        if (m.mesh == event.actor):
            # teeth = m.teeth
            teeth_center=[m.teeth[k].center for k in m.teeth]
            diff = np.abs(np.subtract(teeth_center, [event.picked3d]))
            sm = np.sum(diff, axis=1)
            index = np.argmin(sm)
            # idx_arch = Arch._get_index_arch_type(m.arch_type)
            self.mesh_selected_rotation = {
                'arch_type': m.arch_type,
                'arch': m
            }
            # self.mesh_selected["arch_type"] = m.arch_type
            # self.mesh_selected["arch"] = m
            self.tooth_selected_rotation={
                "label":m.teeth[index+1].label,
                "mode":None, # mesial, distal, out (buccal or labial), in (lingual or palatal), cusp, pit
                "index":index+1
            }
            model = self.mesh_selected_rotation['arch']
            modelpoints = vtk2numpy(self.mesh_selected_rotation['arch'].mesh.polydata().GetPoints().GetData())
            verts = modelpoints
            # faces = model.info['labels'][self.mesh_selected_rotation['label']]['cells']
            faces = model.teeth[self.tooth_selected_rotation['label']].index_vertice_cells
            mesh = Mesh([verts, faces])
            root_point, mean_pts_boundary, tooth_center = get_point_in_root(self, mesh, self.mesh_selected_rotation["arch_type"], self.tooth_selected_rotation['label'])
            d = abs(np.linalg.norm(root_point - mean_pts_boundary))
            self.slider_pivot_root.setTickInterval(d)
            
    
    
    text = "Model: {0}. Label: {1}".format(str(self.mesh_selected_rotation["arch_type"]), str(int(self.tooth_selected_rotation["label"])))
    print(text)
    # change_log(self, text)
    self.btn_pitch.btn_increase.setDisabled(False)
    self.btn_pitch.btn_decrease.setDisabled(False)
    self.btn_roll.btn_increase.setDisabled(False)
    self.btn_roll.btn_decrease.setDisabled(False)
    self.btn_yaw.btn_increase.setDisabled(False)
    self.btn_yaw.btn_decrease.setDisabled(False)