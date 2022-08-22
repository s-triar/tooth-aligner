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
        self.landmark_index = landmark
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
        
        
            
            
        
        
        
        
        