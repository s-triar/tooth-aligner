from constant.enums import ArchType, LandmarkType, ToothType
from utility.analisa_studi_model import AnalisaStudiModel
from utility.arch import Arch
from utility.calculation import FaceTypeConversion, convert_to_2d, find_distance_between_two_points
from utility.splineku import SplineKu
import numpy as np

class Carey(AnalisaStudiModel):
    
    def __init__(self) -> None:
        # mesial aspect first molar ->
        # bucal cusp premolar ->
        # incisal edges of anterior
        
        self.ttm_points={}
        self.ttm_points[ArchType.LOWER.value]=None
        self.ttm_points[ArchType.UPPER.value]=None
        
        self.brasswire_points={}
        self.brasswire_points[ArchType.LOWER.value]=None
        self.brasswire_points[ArchType.UPPER.value]=None
        
        self.total_tooth_material = {}
        self.total_tooth_material[ArchType.LOWER.value]=None
        self.total_tooth_material[ArchType.UPPER.value]=None
                
        self.brass_wire_step_length ={}
        self.brass_wire_step_length[ArchType.LOWER.value]=None
        self.brass_wire_step_length[ArchType.UPPER.value]=None
        
        self.arch_length_descrepancy={}
        self.arch_length_descrepancy[ArchType.LOWER.value]=None
        self.arch_length_descrepancy[ArchType.UPPER.value]=None
        
        self.arch_length_descrepancy_meaning={}
        self.arch_length_descrepancy_meaning[ArchType.LOWER.value]=None
        self.arch_length_descrepancy_meaning[ArchType.UPPER.value]=None
        
        super().__init__()
        
    
    def get_arch_length_discrepancy_meaning(self, val):
        temp = abs(val)
        if(temp <= 2.5):
            return "Proximal stripping"
        elif(temp > 2.5 and temp <= 5):
            return "Extraction of second premolar"
        else:
            return "Extraction of first premolar"
        
    def calculate_carey(self,archs ):
        self.total_tooth_material = {}
        self.total_tooth_material[ArchType.LOWER.value]=None
        self.total_tooth_material[ArchType.UPPER.value]=None
                
        self.brass_wire_step_length ={}
        self.brass_wire_step_length[ArchType.LOWER.value]=None
        self.brass_wire_step_length[ArchType.UPPER.value]=None
        
        self.arch_length_descrepancy={}
        self.arch_length_descrepancy[ArchType.LOWER.value]=None
        self.arch_length_descrepancy[ArchType.UPPER.value]=None
        
        self.arch_length_descrepancy_meaning={}
        self.arch_length_descrepancy_meaning[ArchType.LOWER.value]=None
        self.arch_length_descrepancy_meaning[ArchType.UPPER.value]=None
        
        if Arch._is_complete():
             for a in ArchType:
                idx = Arch._get_index_arch_type(a.value)
                brasswire_pts = self.get_points_brasswire(archs[idx].mesh.points(), archs[idx].teeth)
                ttm_pts = self.get_points_ttm(archs[idx].mesh.points(), archs[idx].teeth)
                
                self.brasswire_points[a.value]=brasswire_pts
                self.ttm_points[a.value]=ttm_pts
                
                temp_eigenvec_arch = [archs[idx].right_left_vec, archs[idx].forward_backward_vec,archs[idx].upward_downward_vec]
                print(brasswire_pts)
                brasswire_pts = convert_to_2d(FaceTypeConversion.UP.value, temp_eigenvec_arch, brasswire_pts)
                ttm_pts = convert_to_2d(FaceTypeConversion.UP.value, temp_eigenvec_arch, ttm_pts)
                
                # print("brasswire_pts",brasswire_pts)
                # print("ttm_pts",ttm_pts)
                brasswire_spline = SplineKu(brasswire_pts, degree=3, smooth=0, res=600)
                # ttm_spline = SplineKu(ttm_pts, degree=3, smooth=0, res=600)
                
                brasswire_length = brasswire_spline.length()
                ttm_length = self.calculate_ttm(ttm_pts)
                
                self.total_tooth_material[a.value]=ttm_length
                self.brass_wire_step_length[a.value]=brasswire_length
                
                descrepancy = brasswire_length - ttm_length
                self.arch_length_descrepancy[a.value]=descrepancy
                
                descrrepancy_meaning = self.get_descrepancy_meaning(descrepancy)
                self.arch_length_descrepancy_meaning[a.value]=descrrepancy_meaning
                
                
                
                
                
    
    def get_descrepancy_meaning(self, descrepancy):
        if(descrepancy>0 and descrepancy <= 2.5):
            return 'proximal stripping can be carried out to reduce the minimal tooth material excess'
        elif(descrepancy>2.5 and descrepancy <= 5):
            return 'extraction of 2nd premolar is indicated'
        elif(descrepancy>5):
            return 'extraction of first premolar is usually required'
        else:
            return '-'
    
    def get_points_brasswire(self, mesh_points, teeth):
        temp =[]
        
        # temp.append(mesh_points[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.CUSP.value]])
        # # temp.append(mesh_points[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.MESIAL.value]])
        # # temp.append(mesh_points[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(teeth[ToothType.INCISOR_UL2_LR2.value].center)
        # temp.append(teeth[ToothType.INCISOR_UL1_LR1.value].center)

        
        # temp.append(teeth[ToothType.INCISOR_UR1_LL1.value].center)
        # temp.append(teeth[ToothType.INCISOR_UR2_LL2.value].center)
        # # temp.append(mesh_points[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]])
        # # temp.append(mesh_points[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.CUSP.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        # temp.append(mesh_points[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.MESIAL.value]])
        
        temp.append(teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value])
        temp.append(teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value])
        temp.append(teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value])
        temp.append(teeth[ToothType.INCISOR_UL2_LR2.value].center)
        temp.append(teeth[ToothType.INCISOR_UL1_LR1.value].center)

        
        temp.append(teeth[ToothType.INCISOR_UR1_LL1.value].center)
        temp.append(teeth[ToothType.INCISOR_UR2_LL2.value].center)
        temp.append(teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value])
        temp.append(teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value])
        temp.append(teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value])
        temp.append(teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.MESIAL.value])
        
        
        return np.array(temp)
        
    def get_points_ttm(self, mesh_points, teeth):
        temp = []
        # temp.append(mesh_points[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]])
        
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.MESIAL.value]])
        # temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.DISTAL.value]])
        # temp.append(mesh_points[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.MESIAL.value]])
        temp.append(teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value])
        
        temp.append(teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.MESIAL.value])
        temp.append(teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.DISTAL.value])
        temp.append(teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.MESIAL.value])
        return np.array(temp)
    
    def calculate_ttm(self, points):
        total = 0
        total += find_distance_between_two_points(points[0],points[1])
        total += find_distance_between_two_points(points[20],points[21])
        for i in range(1,21,2):
            total += find_distance_between_two_points(points[i],points[i+1])
        return total