from constant.enums import ArchType, LandmarkType, ToothType
from utility.analisa_studi_model import AnalisaStudiModel
from utility.arch import Arch


class Carey(AnalisaStudiModel):
    
    def __init__(self) -> None:
        # mesial aspect first molar ->
        # bucal cusp premolar ->
        # incisal edges of anterior
        
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
        
    def calculate_carey(self,archs):
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
            pass
    
    def get_points(self, mesh_points, teeth):
        temp =[]
        temp.append(mesh_points[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.MESIAL.value]])
        temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        temp.append(mesh_points[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        temp.append(mesh_points[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.MESIAL.value]])
        temp.append(mesh_points[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]])
        
        temp.append(mesh_points[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]])
        temp.append(mesh_points[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.MESIAL.value]])
        temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        temp.append(mesh_points[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.CUSP_OUT.value]])
        temp.append(mesh_points[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.MESIAL.value]])