import math
from statistics import median
import numpy as np
from sklearn.metrics import euclidean_distances
from vedo import vtk2numpy, Mesh, Point
from scipy.spatial import KDTree
import os
# from dotenv import load_dotenv
# load_dotenv()
from constant.enums import ArchType, LandmarkType, ToothType
from utility.tooth import Tooth
from utility.colors import convert_labels_to_colors
from utility import landmarking_lib as ll
import copy


class ArchCopy():
    ids=[]
    # static
    def _is_complete():
        return True if ArchType.LOWER.value in ArchCopy.ids and  ArchType.UPPER.value in ArchCopy.ids else False
    def _clear()->None:
        ArchCopy.ids.clear()
    def _remove_arch(arch_type:ArchType, models)->object:
        if(len(ArchCopy.ids)>0):
            idx = ArchCopy.ids.index(arch_type)
            ArchCopy.ids.remove(arch_type)
            temp = models.pop(idx)
            return temp.mesh
    def _get_index_arch_type(arch_type):
        idx = ArchCopy.ids.index(arch_type)
        return idx
        
    # class
    def __init__(self, arch_type:ArchType, mesh, eigenvec, teeth, gingiva) -> None:
        if(arch_type not in ArchCopy.ids):
            ArchCopy.ids.append(arch_type)
        else:
            raise Exception("Duplicate id on class Model")
        self.arch_type = arch_type
        # temp_mesh = Mesh([mesh.points(), mesh.cells()])
        # temp_mesh.celldata['Label'] = mesh.celldata['Label']
        # temp_mesh.celldata['Color'] = mesh.celldata['Color']
        # self.mesh = temp_mesh
        self.mesh = mesh.copy()
        self.right_left_vec = eigenvec[0]
        self.forward_backward_vec = eigenvec[1]
        self.upward_downward_vec = eigenvec[2]
        
        self.gingiva=gingiva
        self.teeth=teeth
        # self.extract_tooth()
        # self.convert_to_colors()
    
    def get_mesh(self):
        return self.mesh
    
    def convert_to_colors(self):
        colors = convert_labels_to_colors(self.mesh.celldata['Label'])
        self.mesh.celldata['Color'] = colors
        self.mesh.celldata.select('Color')
    
    def update_teeth_point_rotation(self, label, type, val_rotate, new_new_center):
        points_mesh = np.array(self.mesh.points())
        idx_faces_mesh = np.array(self.mesh.cells())
        cells_tooth_index = np.where(self.mesh.celldata['Label'] == label)
        label = math.floor(label)    
        cells_tooth = idx_faces_mesh[cells_tooth_index]
        points_tooth_index = np.unique(cells_tooth)
        points_tooth = points_mesh[points_tooth_index]
        center_tooth = np.mean(points_tooth,axis=0)
        self.teeth[label].vertices=points_tooth
        self.teeth[label].index_vertice_cells=cells_tooth
        self.teeth[label].center=center_tooth
        
        self.teeth[label].update_landmark_rotation(type, val_rotate, new_new_center)
        
    def update_teeth_point_moving(self, label, val_direction):
        points_mesh = np.array(self.mesh.points())
        idx_faces_mesh = np.array(self.mesh.cells())
        cells_tooth_index = np.where(self.mesh.celldata['Label'] == label)
        label = math.floor(label)    
        cells_tooth = idx_faces_mesh[cells_tooth_index]
        points_tooth_index = np.unique(cells_tooth)
        points_tooth = points_mesh[points_tooth_index]
        center_tooth = np.mean(points_tooth,axis=0)
        self.teeth[label].vertices=points_tooth
        self.teeth[label].index_vertice_cells=cells_tooth
        self.teeth[label].center=center_tooth
        self.teeth[label].update_landmark_moving(val_direction)
    
    def extract_tooth(self):
        N = self.mesh.NCells()
        labels = np.unique(self.mesh.celldata['Label'])
        # points = vtk2numpy(self.mesh.polydata().GetPoints().GetData()) #vertices (coordinate)
        # ids = vtk2numpy(self.mesh.polydata().GetPolys().GetData()).reshape((N, -1))[:,1:] #faces (list of index of vertices)
        
        center_mesh = self.mesh.centerOfMass()
        points_mesh = np.array(self.mesh.points())
        idx_faces_mesh = np.array(self.mesh.cells())
        points_mesh_normalized = points_mesh-center_mesh
        # print(points_mesh[:10], points_mesh_normalized[:10])
        # print(idx_faces_mesh)
        eigen_val_mesh, eigen_vec_mesh = ll.getEigen(points_mesh_normalized, idx_faces_mesh)
        self.right_left_vec = eigen_vec_mesh[0]
        self.forward_backward_vec = eigen_vec_mesh[1]
        self.upward_downward_vec = eigen_vec_mesh[2]
        # print("eigen vec mesh", eigen_vec_mesh)
        incisor_teeth = [
            ToothType.INCISOR_UL2_LR2.value, 
            ToothType.INCISOR_UL1_LR1.value,
            ToothType.INCISOR_UR1_LL1.value,
            ToothType.INCISOR_UR2_LL2.value
        ]

        canine_teeth = [
            ToothType.CANINE_UL3_LR3.value,
            ToothType.CANINE_UR3_LL3.value
        ]

        premolar_teeth = [
            ToothType.PREMOLAR_UL4_LR4.value,
            ToothType.PREMOLAR_UL5_LR5.value,
            ToothType.PREMOLAR_UR4_LL4.value,
            ToothType.PREMOLAR_UR5_LL5.value
        ]
        
        molar_teeth = [
            ToothType.MOLAR_UL6_LR6.value,
            ToothType.MOLAR_UL7_LR7.value,
            ToothType.MOLAR_UR6_LL6.value,
            ToothType.MOLAR_UR7_LL7.value
        ]
        for label in labels:
            cells_tooth_index = np.where(self.mesh.celldata['Label'] == label)
            label = math.floor(label)
            cells_tooth = idx_faces_mesh[cells_tooth_index]
            points_tooth_index = np.unique(cells_tooth)
            points_tooth = points_mesh[points_tooth_index]
            points_tooth_normalized = points_mesh_normalized[points_tooth_index]
            center_tooth = np.mean(points_tooth,axis=0)
            center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)
            
            point_tooth_index_map = ll.map_point_index(points_tooth_index)
            cells_tooth_mapped = ll.mapping_point_index(point_tooth_index_map, cells_tooth)
            tooth_mesh = Mesh([points_tooth, cells_tooth_mapped]).subdivide(1, method=0)
            points_tooth_normalized = tooth_mesh.points()-center_mesh
            center_tooth_normalized = np.mean(points_tooth_normalized, axis=0)
            
            
            landmark ={}
            landmark[LandmarkType.MESIAL.value]=None
            landmark[LandmarkType.DISTAL.value]=None
            landmark[LandmarkType.BUCCAL_OR_LABIAL.value]=None
            landmark[LandmarkType.LINGUAL_OR_PALATAL.value]=None
            landmark[LandmarkType.PIT.value]=None
            landmark[LandmarkType.CUSP.value]=None
            landmark[LandmarkType.CUSP_OUT.value]=None
            landmark[LandmarkType.CUSP_IN.value]=None
            landmark[LandmarkType.CUSP_OUT_MESIAL.value]=None
            landmark[LandmarkType.CUSP_OUT_MIDDLE.value]=None
            landmark[LandmarkType.CUSP_OUT_DISTAL.value]=None
            landmark[LandmarkType.CUSP_IN_MESIAL.value]=None
            landmark[LandmarkType.CUSP_IN_DISTAL.value]=None
            
            if(math.floor(label)==ToothType.GINGIVA.value):
                gingiva =  Tooth(
                        math.floor(label), 
                        points_tooth,
                        cells_tooth,
                        center_tooth,
                        landmark
                    )
                self.gingiva = gingiva
            else:
                
                is_awal = True if label in [ToothType.INCISOR_UR1_LL1.value,
                                            ToothType.INCISOR_UR2_LL2.value, 
                                            ToothType.CANINE_UR3_LL3.value,
                                            ToothType.PREMOLAR_UR4_LL4.value,
                                            ToothType.PREMOLAR_UR5_LL5.value,
                                            ToothType.MOLAR_UR6_LL6.value,
                                            ToothType.MOLAR_UR7_LL7.value,] else False
                is_upper = True if self.arch_type == ArchType.UPPER.value else False
                
                if(label in incisor_teeth):
                    if(label in [ToothType.INCISOR_UL1_LR1.value, ToothType.INCISOR_UR1_LL1.value]):
                        mesial, distal = ll.get_mesial_distal_anterior(is_awal, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                        buccal_or_labial, lingual_or_palatal = ll.get_buccal_or_labial_andlingual_or_palatal_anterior(label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    else:
                        mesial, distal = ll.get_mesial_distal_anterior_second(is_awal, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                        buccal_or_labial, lingual_or_palatal = ll.get_buccal_or_labial_andlingual_or_palatal_anterior_second(is_awal, is_upper, label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    cusp = ll.get_cusp_anterior(eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    
                    mesial_index = ll.get_index_point_from_mesh_vertices(mesial, points_tooth_normalized) #points_mesh_normalized
                    distal_index = ll.get_index_point_from_mesh_vertices(distal, points_tooth_normalized) #points_mesh_normalized
                    buccal_or_labial_index = ll.get_index_point_from_mesh_vertices(buccal_or_labial, points_tooth_normalized) #points_mesh_normalized
                    lingual_or_palatal_index = ll.get_index_point_from_mesh_vertices(lingual_or_palatal, points_tooth_normalized) #points_mesh_normalized
                    cusp_index = ll.get_index_point_from_mesh_vertices(cusp, points_tooth_normalized) #points_mesh_normalized
                    
                    landmark[LandmarkType.MESIAL.value]=tooth_mesh.points()[mesial_index]
                    landmark[LandmarkType.DISTAL.value]=tooth_mesh.points()[distal_index]
                    landmark[LandmarkType.BUCCAL_OR_LABIAL.value]=tooth_mesh.points()[buccal_or_labial_index]
                    landmark[LandmarkType.LINGUAL_OR_PALATAL.value]=tooth_mesh.points()[lingual_or_palatal_index]
                    landmark[LandmarkType.CUSP.value]=tooth_mesh.points()[cusp_index]
                    tooth = Tooth(
                                label, 
                                points_tooth,
                                cells_tooth,
                                center_tooth,
                                landmark
                            )
                    self.teeth[label]=tooth
                    # if(label==1):
                    #     print(landmark)
                
                elif(label in canine_teeth):
                    mesial, distal = ll.get_mesial_distal_canine(is_awal, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    buccal_or_labial, lingual_or_palatal = ll.get_buccal_or_labial_andlingual_or_palatal_canine(is_awal, is_upper,eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    cusp= ll.get_cusp_anterior(eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    
                    mesial_index = ll.get_index_point_from_mesh_vertices(mesial, points_tooth_normalized) #points_mesh_normalized
                    distal_index = ll.get_index_point_from_mesh_vertices(distal, points_tooth_normalized) #points_mesh_normalized
                    buccal_or_labial_index = ll.get_index_point_from_mesh_vertices(buccal_or_labial, points_tooth_normalized) #points_mesh_normalized
                    lingual_or_palatal_index = ll.get_index_point_from_mesh_vertices(lingual_or_palatal, points_tooth_normalized) #points_mesh_normalized
                    cusp_index = ll.get_index_point_from_mesh_vertices(cusp, points_tooth_normalized) #points_mesh_normalized
                    landmark[LandmarkType.MESIAL.value]=tooth_mesh.points()[mesial_index]
                    landmark[LandmarkType.DISTAL.value]=tooth_mesh.points()[distal_index]
                    landmark[LandmarkType.BUCCAL_OR_LABIAL.value]=tooth_mesh.points()[buccal_or_labial_index]
                    landmark[LandmarkType.LINGUAL_OR_PALATAL.value]=tooth_mesh.points()[lingual_or_palatal_index]
                    landmark[LandmarkType.CUSP.value]=tooth_mesh.points()[cusp_index]
                    tooth = Tooth(
                                label, 
                                points_tooth,
                                cells_tooth,
                                center_tooth,
                                landmark
                            )
                    self.teeth[label]=tooth
                
                elif(label in premolar_teeth):
                    mesial, distal = ll.get_mesial_distal_premolar(is_awal, is_upper,label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    buccal_or_labial, lingual_or_palatal = ll.get_buccal_or_labial_andlingual_or_palatal_premolar(is_awal,is_upper,label,eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    cusps = ll.get_cusp_posterior(is_upper, label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    pit = ll.get_pit(eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    
                    mesial_index = ll.get_index_point_from_mesh_vertices(mesial, points_tooth_normalized) #points_mesh_normalized
                    distal_index = ll.get_index_point_from_mesh_vertices(distal, points_tooth_normalized) #points_mesh_normalized
                    buccal_or_labial_index = ll.get_index_point_from_mesh_vertices(buccal_or_labial, points_tooth_normalized) #points_mesh_normalized
                    lingual_or_palatal_index = ll.get_index_point_from_mesh_vertices(lingual_or_palatal, points_tooth_normalized) #points_mesh_normalized
                    cusp_indexes=[]
                    for cusp in cusps:
                        cusp_index = ll.get_index_point_from_mesh_vertices(cusp, points_tooth_normalized)  #points_mesh_normalized           
                        cusp_indexes.append(cusp_index)
                            
                    pit_index = ll.get_index_point_from_mesh_vertices(pit, points_tooth_normalized) #points_mesh_normalized            
                    landmark[LandmarkType.MESIAL.value]=tooth_mesh.points()[mesial_index]
                    landmark[LandmarkType.DISTAL.value]=tooth_mesh.points()[distal_index]
                    landmark[LandmarkType.BUCCAL_OR_LABIAL.value]=tooth_mesh.points()[buccal_or_labial_index]
                    landmark[LandmarkType.LINGUAL_OR_PALATAL.value]=tooth_mesh.points()[lingual_or_palatal_index]
                    landmark[LandmarkType.PIT.value]=tooth_mesh.points()[pit_index]
                    if(len(cusp_indexes)==3):
                        # in mesial, in distal, out
                        landmark[LandmarkType.CUSP_IN_MESIAL.value]=tooth_mesh.points()[cusp_indexes[0]]
                        landmark[LandmarkType.CUSP_IN_DISTAL.value]=tooth_mesh.points()[cusp_indexes[1]]
                        landmark[LandmarkType.CUSP_OUT.value]=tooth_mesh.points()[cusp_indexes[2]]
                    else:
                        # in, out
                        landmark[LandmarkType.CUSP_IN.value]=tooth_mesh.points()[cusp_indexes[0]]
                        landmark[LandmarkType.CUSP_OUT.value]=tooth_mesh.points()[cusp_indexes[1]]
                    
                    tooth = Tooth(
                                label, 
                                points_tooth,
                                cells_tooth,
                                center_tooth,
                                landmark
                            )
                    self.teeth[label]=tooth
                
                elif(label in molar_teeth):
                    mesial, distal = ll.get_mesial_distal_molar(is_awal, is_upper,label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    buccal_or_labial, lingual_or_palatal = ll.get_buccal_or_labial_andlingual_or_palatal_molar(is_awal,is_upper,label,eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    cusps = ll.get_cusp_posterior(is_upper, label, eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    pit = ll.get_pit(eigen_vec_mesh, center_tooth_normalized, points_tooth_normalized)
                    
                    mesial_index = ll.get_index_point_from_mesh_vertices(mesial, points_tooth_normalized) #points_mesh_normalized
                    distal_index = ll.get_index_point_from_mesh_vertices(distal, points_tooth_normalized) #points_mesh_normalized
                    buccal_or_labial_index = ll.get_index_point_from_mesh_vertices(buccal_or_labial, points_tooth_normalized) #points_mesh_normalized
                    lingual_or_palatal_index = ll.get_index_point_from_mesh_vertices(lingual_or_palatal, points_tooth_normalized) #points_mesh_normalized
                    cusp_indexes=[]
                    for cusp in cusps:
                        cusp_index = ll.get_index_point_from_mesh_vertices(cusp, points_tooth_normalized) #points_mesh_normalized            
                        cusp_indexes.append(cusp_index)
                            
                    # print("pit molar", label, pit)
                    pit_index = ll.get_index_point_from_mesh_vertices(pit, points_tooth_normalized) #points_mesh_normalized            
                    landmark[LandmarkType.MESIAL.value]=tooth_mesh.points()[mesial_index]
                    landmark[LandmarkType.DISTAL.value]=tooth_mesh.points()[distal_index]
                    landmark[LandmarkType.BUCCAL_OR_LABIAL.value]=tooth_mesh.points()[buccal_or_labial_index]
                    landmark[LandmarkType.LINGUAL_OR_PALATAL.value]=tooth_mesh.points()[lingual_or_palatal_index]
                    landmark[LandmarkType.PIT.value]=tooth_mesh.points()[pit_index]
                    if(len(cusp_indexes)==5):
                        # in mesial, in distal, out mesial, out middle, out distal
                        landmark[LandmarkType.CUSP_IN_MESIAL.value]=tooth_mesh.points()[cusp_indexes[0]]
                        landmark[LandmarkType.CUSP_IN_DISTAL.value]=tooth_mesh.points()[cusp_indexes[1]]
                        landmark[LandmarkType.CUSP_OUT_MESIAL.value]=tooth_mesh.points()[cusp_indexes[2]]
                        landmark[LandmarkType.CUSP_OUT_MIDDLE.value]=tooth_mesh.points()[cusp_indexes[3]]
                        landmark[LandmarkType.CUSP_OUT_DISTAL.value]=tooth_mesh.points()[cusp_indexes[4]]
                    else:
                        # in mesial, in distal, out mesial, out distal
                        landmark[LandmarkType.CUSP_IN_MESIAL.value]=tooth_mesh.points()[cusp_indexes[0]]
                        landmark[LandmarkType.CUSP_IN_DISTAL.value]=tooth_mesh.points()[cusp_indexes[1]]
                        landmark[LandmarkType.CUSP_OUT_MESIAL.value]=tooth_mesh.points()[cusp_indexes[2]]
                        landmark[LandmarkType.CUSP_OUT_DISTAL.value]=tooth_mesh.points()[cusp_indexes[3]]
                   
                    tooth = Tooth(
                                label, 
                                points_tooth,
                                cells_tooth,
                                center_tooth,
                                landmark
                            )
                    self.teeth[label]=tooth
                #=============================================================================            
            
            
    