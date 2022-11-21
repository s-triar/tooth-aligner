
import numpy as np
import os
# from dotenv import load_dotenv
# load_dotenv()
from constant.enums import ToothType, LandmarkType
from vedo import vtk2numpy, Mesh, Point

class Tooth():    

    def __init__(self, 
                 label:ToothType, 
                 vertices:np.ndarray,
                 index_vertice_cells: np.ndarray,
                 center:np.ndarray,
                 landmark
                 ) -> None:
        self.label=label
        self.vertices=vertices
        self.index_vertice_cells=index_vertice_cells
        self.center=center
        self.landmark_pt = landmark
        
        # self.landmark_index = landmark
        # self.mesial_index=mesial_index
        # self.distal_index=distal_index
        # self.buccal_or_labial_index = buccal_or_labial_index # buccal or labial # out
        # self.lingual_or_palatal_index = lingual_or_palatal_index # palatal or lingual # in
        # self.cusp_indexes=cusp_indexes
        # self.pit_index=pit_index
        # self.generate_mesh()
        
    def generate_mesh(self):
        points_index = np.unique(self.index_vertice_cells)
        # print(points_index)
        points_label = self.vertices[points_index]
        sorted_index_points_index = np.argsort(points_index)
        map_sorted2ori={}
        map_ori2sorted={}
        for sp,p in zip(sorted_index_points_index, points_index):
            map_sorted2ori[sp]=p
            map_ori2sorted[p]=sp
    
    def update_landmark_rotation(self, type, val_rotate, new_new_center):
        new_new_center = [new_new_center[0],new_new_center[1],new_new_center[2]]
        # print("do rotate landmark",type, val_rotate, new_new_center)
        for k in self.landmark_pt:
            pt = self.landmark_pt[k]
            if(pt is not None):
                PT = Point(pt)
                if(type=="pitch"):
                    PT.rotateX(val_rotate, False, new_new_center)
                    # print("rotate x tooth landmark")
                elif(type=="yaw"):
                    PT.rotateY(val_rotate, False, new_new_center)
                    # print("rotate y tooth landmark")
                elif(type=="roll"):
                    PT.rotateZ(val_rotate, False, new_new_center)
                    # print("rotate z tooth landmark")
                # print("self.landmark_pt[k]=PT.points()",PT.points()[0])
                self.landmark_pt[k]=PT.points()[0]
        
    def update_landmark_moving(self, val_direction):
        # print("do moving landmark",val_direction)
        val_direction = [val_direction[0],val_direction[1],val_direction[2]]
        for k in self.landmark_pt:
            pt = self.landmark_pt[k]
            if(pt is not None):
                pt = pt+val_direction
                self.landmark_pt[k]=pt
            
        
        
        
        
        