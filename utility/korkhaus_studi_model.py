from utility.analisa_studi_model import AnalisaStudiModel
from constant.enums import ArchType, ToothType, LandmarkType
import numpy as np
from utility.arch import Arch

class Korkhaus(AnalisaStudiModel):
    
    def __init__(self) -> None:
        self.center_incisor_points={
            ArchType.LOWER.value:None,
            ArchType.UPPER.value:None,
        }
        self.perpendicular_points={
            ArchType.LOWER.value:None,
            ArchType.UPPER.value:None,
        }
        self.premolar_points={
            ArchType.LOWER.value:None,
            ArchType.UPPER.value:None,
        }
        
        self.incisors_width={} #Sum of Incisors
        self.incisors_width[ArchType.LOWER.value]=None
        self.incisors_width[ArchType.UPPER.value]=None
        
        self.khorkaus_line={} #
        self.khorkaus_line[ArchType.LOWER.value]=None
        self.khorkaus_line[ArchType.UPPER.value]=None
        
        self.d_premolar={} #
        self.d_premolar[ArchType.LOWER.value]=None
        self.d_premolar[ArchType.UPPER.value]=None
        
        self.delta_p1_ideal={}
        self.delta_p1_ideal[ArchType.LOWER.value]=None
        self.delta_p1_ideal[ArchType.UPPER.value]=None
        
        self.width_ideal={}
        self.width_ideal[ArchType.LOWER.value]=None
        self.width_ideal[ArchType.UPPER.value]=None
        
        self.status_line_to_width={}
        self.status_line_to_width[ArchType.LOWER.value]=None
        self.status_line_to_width[ArchType.UPPER.value]=None
        
        self.status_khorkaus=None
        
        super().__init__()
        
    def calculate_khorkaus(self, archs):
        self.delta_p1_ideal={}
        self.delta_p1_ideal[ArchType.LOWER.value]=None
        self.delta_p1_ideal[ArchType.UPPER.value]=None
        
        self.width_ideal={}
        self.width_ideal[ArchType.LOWER.value]=None
        self.width_ideal[ArchType.UPPER.value]=None
        
        self.status_line_to_width={}
        self.status_line_to_width[ArchType.LOWER.value]=None
        self.status_line_to_width[ArchType.UPPER.value]=None
        
        self.status_khorkaus=None
        self.status_khorkaus_meaning=None
        
        self.status_expansion_meaning={}
        self.status_expansion_meaning[ArchType.LOWER.value]=None
        self.status_expansion_meaning[ArchType.UPPER.value]=None
        
        if Arch._is_complete():
            self.calculate_incisors(archs)
            self.calculate_d_pre_and_khorkaus_line(archs)
            self.delta_p1_ideal={}
            self.delta_p1_ideal[ArchType.LOWER.value]=self.incisors_width[ArchType.LOWER.value]+8
            self.delta_p1_ideal[ArchType.UPPER.value]=self.incisors_width[ArchType.UPPER.value]+8
            
            self.width_ideal={}
            self.width_ideal[ArchType.LOWER.value]=self.delta_p1_ideal[ArchType.LOWER.value]/2
            self.width_ideal[ArchType.UPPER.value]=self.delta_p1_ideal[ArchType.UPPER.value]/2
            
            self.status_line_to_width={}
            self.status_line_to_width[ArchType.LOWER.value]=self.khorkaus_line[ArchType.LOWER.value]-self.width_ideal[ArchType.LOWER.value]
            self.status_line_to_width[ArchType.UPPER.value]=self.khorkaus_line[ArchType.UPPER.value]-self.width_ideal[ArchType.UPPER.value]
            
            self.status_expansion_meaning[ArchType.LOWER.value]=self.check_anterior_expansion_status(self.status_line_to_width[ArchType.LOWER.value])
            self.status_expansion_meaning[ArchType.UPPER.value]=self.check_anterior_expansion_status(self.status_line_to_width[ArchType.UPPER.value])
            
            self.status_khorkaus=(self.khorkaus_line[ArchType.UPPER.value]-2)-self.khorkaus_line[ArchType.LOWER.value]
            self.status_khorkaus_meaning = self.check_anterior_klinasi_status(self.status_khorkaus)
            
            
            status_lower = '{} => {}'.format(str(self.status_line_to_width[ArchType.LOWER.value]), self.status_expansion_meaning[ArchType.LOWER.value])
            status_upper = '{} => {}'.format(str(self.status_line_to_width[ArchType.UPPER.value]), self.status_expansion_meaning[ArchType.UPPER.value])
            status_khor  = '{} => {}'.format(str(self.status_khorkaus),self.status_khorkaus_meaning)
            
            # status = 'Lower:\n{}\nUpper:\n{}\nKhorkaus Line:\n{}'.format(status_lower,status_upper,status_khor)
            # print("KHORKAUS")
            # print(status)
    
    def check_anterior_expansion_status(self, val):
        if(val>0):
            return 'Dapat dilakukan retraksi anterior'
        else:
            return 'Dapat dilakukan ekspansi anterior'
    
    def check_anterior_klinasi_status(self,val):
        if(val>0):
            return 'Terdapat Proklinasi anterior atas'
        else:
            return 'Terdapat Retroklinasi anterior atas'
        
    def calculate_d_pre_and_khorkaus_line(self,archs): 
        self.khorkaus_line[ArchType.LOWER.value]=None
        self.khorkaus_line[ArchType.UPPER.value]=None
        self.d_premolar[ArchType.LOWER.value]=None
        self.d_premolar[ArchType.UPPER.value]=None
        if Arch._is_complete():
            UPPER_IDX=Arch._get_index_arch_type(ArchType.UPPER.value)
            LOWER_IDX=Arch._get_index_arch_type(ArchType.LOWER.value)
            # idx_maxi_l = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.PIT.value]
            # idx_maxi_r = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.PIT.value]
            
            # maxi_l = archs[UPPER_IDX].mesh.points()[idx_maxi_l]
            # maxi_r = archs[UPPER_IDX].mesh.points()[idx_maxi_r]
            
            maxi_l = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.PIT.value]
            maxi_r = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.PIT.value]
            
            self.premolar_points[ArchType.UPPER.value]=[maxi_l, maxi_r]
            # idx_mandi_l1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.DISTAL.value]
            # idx_mandi_r1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.DISTAL.value]
            # idx_mandi_l2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.MESIAL.value]
            # idx_mandi_r2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.MESIAL.value]

            # mandi_l1 = archs[LOWER_IDX].mesh.points()[idx_mandi_l1]
            # mandi_r1 = archs[LOWER_IDX].mesh.points()[idx_mandi_r1]
            # mandi_l2 = archs[LOWER_IDX].mesh.points()[idx_mandi_l2]
            # mandi_r2 = archs[LOWER_IDX].mesh.points()[idx_mandi_r2]
            
            mandi_l1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.DISTAL.value]
            mandi_r1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.DISTAL.value]
            mandi_l2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.MESIAL.value]
            mandi_r2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.MESIAL.value]
            
            mandi_l = (mandi_l1+mandi_l2)/2
            mandi_r = (mandi_r1+mandi_r2)/2
            self.premolar_points[ArchType.LOWER.value]=[mandi_l, mandi_r]
            center_incisor_max=np.mean([
                    # archs[UPPER_IDX].mesh.points()[archs[UPPER_IDX].teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]],    
                    # archs[UPPER_IDX].mesh.points()[archs[UPPER_IDX].teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]],
                    archs[UPPER_IDX].teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],    
                    archs[UPPER_IDX].teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value],
                ],axis=0)
            self.center_incisor_points[ArchType.UPPER.value]=center_incisor_max
            center_incisor_man=np.mean([
                    # archs[LOWER_IDX].mesh.points()[archs[LOWER_IDX].teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]],    
                    # archs[LOWER_IDX].mesh.points()[archs[LOWER_IDX].teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]],
                    archs[LOWER_IDX].teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],    
                    archs[LOWER_IDX].teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value],
                ],axis=0)
            self.center_incisor_points[ArchType.LOWER.value]=center_incisor_man
            self.d_premolar[ArchType.LOWER.value]=np.linalg.norm(mandi_l - mandi_r)
            self.d_premolar[ArchType.UPPER.value]=np.linalg.norm(maxi_l - maxi_r)
            
            d = (maxi_l - maxi_r) / np.linalg.norm(maxi_l - maxi_r)
            v = center_incisor_max - maxi_r
            t = np.dot(v,d)
            P = maxi_r + t * d
            # return P.distance(A);
            self.perpendicular_points[ArchType.UPPER.value]=P
            d = (mandi_l - mandi_r) / np.linalg.norm(mandi_l - mandi_r)
            v = center_incisor_man - mandi_r
            t = np.dot(v,d)
            P = mandi_r + t * d
            self.perpendicular_points[ArchType.LOWER.value]=P
            # print('perpendicular_points', self.perpendicular_points)
            self.khorkaus_line[ArchType.LOWER.value]=np.linalg.norm(np.cross(mandi_l - mandi_r, mandi_r - center_incisor_man))/np.linalg.norm(mandi_l - mandi_r)
            self.khorkaus_line[ArchType.UPPER.value]=np.linalg.norm(np.cross(maxi_l - maxi_r, maxi_r - center_incisor_max))/np.linalg.norm(maxi_l - maxi_r)
        
    
    def calculate_incisors(self, archs):
        self.incisors_width[ArchType.LOWER.value]=None
        self.incisors_width[ArchType.UPPER.value]=None
        if Arch._is_complete():
            self.incisors_width[ArchType.LOWER.value]=0
            self.incisors_width[ArchType.UPPER.value]=0
            for arch in archs:
                for label in arch.teeth:
                    tooth = arch.teeth[label]
                    # mesial_pt = arch.mesh.points()[tooth.landmark_index[LandmarkType.MESIAL.value]]
                    # distal_pt = arch.mesh.points()[tooth.landmark_index[LandmarkType.DISTAL.value]]
                    mesial_pt = tooth.landmark_pt[LandmarkType.MESIAL.value]
                    distal_pt = tooth.landmark_pt[LandmarkType.DISTAL.value]
                    w = np.linalg.norm(mesial_pt - distal_pt)
                    if(tooth.label in self.label_anterior):
                        self.incisors_width[arch.arch_type]+=w
    
    
    
    
    
    