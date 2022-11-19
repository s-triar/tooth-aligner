from utility.analisa_studi_model import AnalisaStudiModel
from constant.enums import ArchType, LandmarkType
import numpy as np
from utility.arch import Arch

class Bolton(AnalisaStudiModel):
    
    def __init__(self ) -> None:
        
        
        self.anterior=None
        self.overall=None
        self.teeth_width={}
        self.teeth_width[ArchType.LOWER.value]=None
        self.teeth_width[ArchType.UPPER.value]=None
        self.overal_width={}
        self.overal_width[ArchType.LOWER.value]=0
        self.overal_width[ArchType.UPPER.value]=0
        self.anterior_width={}
        self.anterior_width[ArchType.LOWER.value]=0
        self.anterior_width[ArchType.UPPER.value]=0
        self.kmno = None
        self.kmxo = None
        self.kmna = None
        self.kmxa = None
        
        self.correction_anterior=None
        self.correction_arch_anterior = None
        self.correction_overall=None
        self.correction_arch_overall = None
        
        super().__init__()
        
    def get_anterior_overall(self):
        return self.anterior, self.overall

    def get_anterior_overall_width(self):
        return self.overal_width, self.anterior_width
    
    def get_overjet(self):
        return self.kmno,self.kmxo,self.kmna,self.kmxa
    
    def calc_overjet(self):
        if(self.anterior==None or self.overall==None):
            self.kmno = None
            self.kmxo = None
            self.kmna = None
            self.kmxa = None
        else:
            self.kmno = self.overal_width[ArchType.LOWER.value] - (( self.overal_width[ArchType.UPPER.value] *91.3)/100)
            self.kmxo = self.overal_width[ArchType.UPPER.value] - (( self.overal_width[ArchType.LOWER.value] *100)/91.3)
            self.kmna = self.anterior_width[ArchType.LOWER.value] - (( self.anterior_width[ArchType.UPPER.value] *77.2)/100)
            self.kmxa = self.anterior_width[ArchType.UPPER.value] - (( self.anterior_width[ArchType.LOWER.value] *100)/77.2)
            self.calc_correction_anterior()
            self.calc_correction_overall()
        
        
    def calc_anterior_overall(self, archs):
        self.overal_width={}
        self.overal_width[ArchType.LOWER.value]=0 # Total tooth materials
        self.overal_width[ArchType.UPPER.value]=0 # Total tooth materials
        self.anterior_width={}
        self.anterior_width[ArchType.LOWER.value]=0 # Total tooth materials ANTERIOR ONLY
        self.anterior_width[ArchType.UPPER.value]=0 # Total tooth materials ANTERIOR ONLY
        self.anterior=None
        self.overall=None
        self.teeth_width[ArchType.LOWER.value]=None
        self.teeth_width[ArchType.UPPER.value]=None
        if Arch._is_complete():
            self.teeth_width[ArchType.LOWER.value]={}
            self.teeth_width[ArchType.UPPER.value]={}
            for arch in archs:
                for label in arch.teeth:
                    tooth = arch.teeth[label]
                    # mesial_pt = arch.mesh.points()[tooth.landmark_index[LandmarkType.MESIAL.value]]
                    # distal_pt = arch.mesh.points()[tooth.landmark_index[LandmarkType.DISTAL.value]]
                    mesial_pt = tooth.landmark_pt[LandmarkType.MESIAL.value]
                    distal_pt = tooth.landmark_pt[LandmarkType.DISTAL.value]
                    w = np.linalg.norm(mesial_pt - distal_pt)
                    self.teeth_width[arch.arch_type][label]=w
                    if(tooth.label in self.label_all):
                        self.overal_width[arch.arch_type]+=w
                    if(tooth.label in self.label_anterior or tooth.label in self.label_canine):
                        self.anterior_width[arch.arch_type]+=w
            
            if(
                self.anterior_width[ArchType.LOWER.value] != 0 and self.anterior_width[ArchType.UPPER.value] != 0 and
                self.overal_width[ArchType.LOWER.value]!=0 and self.overal_width[ArchType.UPPER.value]!=0
                ):
                self.anterior= self.anterior_width[ArchType.LOWER.value] * 100 / self.anterior_width[ArchType.UPPER.value]
                self.overall= self.overal_width[ArchType.LOWER.value] * 100 / self.overal_width[ArchType.UPPER.value]
            # else:
            #     self.anterior= self.anterior_width[ArchType.LOWER] * 100 / self.anterior_width[ArchType.UPPER]
            #     self.overall= self.overal_width[ArchType.LOWER] * 100 / self.overal_width[ArchType.UPPER]
        print("from bolton", self.anterior, self.overall)
        self.calc_overjet()
        
    def draw_line_correction_anterior(self,
            models,
            correction_arch_anterior,
            correction_anterior,
        ):
        model_idx = Arch._get_index_arch_type(correction_arch_anterior)
        model = models[model_idx]
        pts=[]
        pts_correction=[]
        for k in self.label_all:
            if(k in self.label_anterior or k in self.label_canine):
                center = model.teeth[k].center
                pts.append(center)
                center_arch = model.mesh.centerOfMass()
                v=center-center_arch
                vv=np.linalg.norm(v)
                u = v/vv
                dd=vv-correction_anterior
                new_center = np.array(center_arch) + (dd*u)
                pts_correction.append(new_center)
            else:
                center = model.teeth[k].center
                pts.append(center)
                pts_correction.append(center)
        return pts, pts_correction
    
    def draw_line_correction_overall(self,
            models,
            correction_arch_overall,
            correction_overall,
        ):
        model_idx = Arch._get_index_arch_type(correction_arch_overall)
        model = models[model_idx]
        pts=[]
        pts_correction=[]
        for k in self.label_all:
            if(k in self.label_anterior or k in self.label_canine):
                center = model.teeth[k].center
                pts.append(center)
                center_arch = model.mesh.centerOfMass()
                v=center-center_arch
                vv=np.linalg.norm(v)
                u = v/vv
                dd=vv-correction_overall
                new_center = np.array(center_arch) + (dd*u)
                pts_correction.append(new_center)
            else:
                center = model.teeth[k].center
                pts.append(center)
                pts_correction.append(center)
        return pts, pts_correction
                
    def calc_correction_anterior(self):
        self.correction_anterior=None
        self.correction_arch_anterior = None
        if(self.anterior > 77.2):
            # mandibular terlalu besar
            self.correction_arch_anterior = ArchType.LOWER.value
            self.correction_anterior = self.kmna
        elif(self.anterior < 77.2):
            # maxillary terlalu besar
            self.correction_arch_anterior = ArchType.UPPER.value
            self.correction_anterior = self.kmxa
    
    def calc_correction_overall(self):
        self.correction_overall=None
        self.correction_arch_overall = None
        if(self.overall > 91.3):
            # mandibular terlalu besar
            self.correction_arch_overall = ArchType.LOWER.value
            self.correction_overall = self.kmno
        elif(self.overall < 91.3):
            # maxillary terlalu besar
            self.correction_arch_overall = ArchType.UPPER.value
            self.correction_overall = self.kmxo