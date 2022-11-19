from typing_extensions import Self
from utility.analisa_studi_model import AnalisaStudiModel
from constant.enums import ArchType, ToothType, LandmarkType
import numpy as np
from utility.arch import Arch
from utility.calculation import find_closest_point_between_a_point_and_a_line, find_distance_between_two_points

class Pont(AnalisaStudiModel):
    
    def __init__(self) -> None:
       
        self.premolar_pts={
            ArchType.LOWER.value:None,
            ArchType.UPPER.value:None,
        }
       
        self.molar_pts={
            ArchType.LOWER.value:None,
            ArchType.UPPER.value:None,
        }
       
        self.teeth_width={}
        self.teeth_width[ArchType.LOWER.value]=None
        self.teeth_width[ArchType.UPPER.value]=None
        
        self.incisors_width={} #Sum of Incisors
        self.incisors_width[ArchType.LOWER.value]=None
        self.incisors_width[ArchType.UPPER.value]=None
        
        self.cpv={} #perhitungan
        self.cpv[ArchType.LOWER.value]=None
        self.cpv[ArchType.UPPER.value]=None
        
        self.cmv={} #perhitungan
        self.cmv[ArchType.LOWER.value]=None
        self.cmv[ArchType.UPPER.value]=None
        
        self.mpv={} #pengukuran 
        self.mpv[ArchType.LOWER.value]=None
        self.mpv[ArchType.UPPER.value]=None
        
        self.mmv={} #pengukuran
        self.mmv[ArchType.LOWER.value]=None
        self.mmv[ArchType.UPPER.value]=None
        
        self.index_cpv = 85
        self.index_cmv = 64
        
        self.delta_pv={} #pengukuran
        self.delta_pv[ArchType.LOWER.value]=None
        self.delta_pv[ArchType.UPPER.value]=None
        
        self.delta_mp={} #pengukuran
        self.delta_mp[ArchType.LOWER.value]=None
        self.delta_mp[ArchType.UPPER.value]=None
        
        self.status_pv={} #status dari hasil pengukuran
        self.status_pv[ArchType.LOWER.value]=None
        self.status_pv[ArchType.UPPER.value]=None
        
        self.status_mp={} #status dari hasil pengukuran
        self.status_mp[ArchType.LOWER.value]=None
        self.status_mp[ArchType.UPPER.value]=None
        
        self.degree_status_pv={} #degree status dari hasil pengukuran
        self.degree_status_pv[ArchType.LOWER.value]=None
        self.degree_status_pv[ArchType.UPPER.value]=None
        
        self.degree_status_mp={} #degree status dari hasil pengukuran
        self.degree_status_mp[ArchType.LOWER.value]=None
        self.degree_status_mp[ArchType.UPPER.value]=None
        
        self.status=None
        super().__init__()
        
    def calculate_pont(self, archs):
        self.status = None
        if Arch._is_complete():
            
            self.calculate_incisors(archs)
            
            self.calculate_cpv()
            self.calculate_mpv(archs)
            self.calculate_cmv()
            self.calculate_mmv(archs)
            
            self.delta_pv[ArchType.LOWER.value]=self.mpv[ArchType.LOWER.value]-self.cpv[ArchType.LOWER.value]
            self.delta_pv[ArchType.UPPER.value]=self.mpv[ArchType.UPPER.value]-self.cpv[ArchType.UPPER.value]
            self.delta_mp[ArchType.LOWER.value]=self.mmv[ArchType.LOWER.value]-self.cmv[ArchType.LOWER.value]
            self.delta_mp[ArchType.UPPER.value]=self.mmv[ArchType.UPPER.value]-self.cmv[ArchType.UPPER.value]
            
            self.status_pv[ArchType.LOWER.value]=self.check_delta(self.delta_pv[ArchType.LOWER.value])
            self.status_pv[ArchType.UPPER.value]=self.check_delta(self.delta_pv[ArchType.UPPER.value])
            self.status_mp[ArchType.LOWER.value]=self.check_delta(self.delta_mp[ArchType.LOWER.value])
            self.status_mp[ArchType.UPPER.value]=self.check_delta(self.delta_mp[ArchType.UPPER.value])
            
            self.degree_status_pv[ArchType.LOWER.value]=self.check_degree(self.delta_pv[ArchType.LOWER.value])
            self.degree_status_pv[ArchType.UPPER.value]=self.check_degree(self.delta_pv[ArchType.UPPER.value])
            self.degree_status_mp[ArchType.LOWER.value]=self.check_degree(self.delta_mp[ArchType.LOWER.value])
            self.degree_status_mp[ArchType.UPPER.value]=self.check_degree(self.delta_mp[ArchType.UPPER.value])
            
            status_pv_lower= '{} => {}/{}'.format(str(self.delta_pv[ArchType.LOWER.value]), self.status_pv[ArchType.LOWER.value], self.degree_status_pv[ArchType.LOWER.value] )
            status_pv_upper= '{} => {}/{}'.format(str(self.delta_pv[ArchType.UPPER.value]), self.status_pv[ArchType.UPPER.value], self.degree_status_pv[ArchType.UPPER.value] )
            status_mp_lower= '{} => {}/{}'.format(str(self.delta_mp[ArchType.LOWER.value]), self.status_mp[ArchType.LOWER.value], self.degree_status_mp[ArchType.LOWER.value] )
            status_mp_upper= '{} => {}/{}'.format(str(self.delta_mp[ArchType.UPPER.value]), self.status_mp[ArchType.UPPER.value], self.degree_status_mp[ArchType.UPPER.value] )
            
            self.status = 'Premolar Lower:\n{}\nPremolar Upper:\n{}\nMolar Lower:\n{}\nMolar Upper:\n{}'.format(status_pv_lower, status_pv_upper, status_mp_lower, status_mp_upper)
            print("PONT")
            print(self.status)
            # delta => negative = kontraksi, positif = distraksi, 0 = normal
            # degree=>0-5mm = mild, 5-10mm = medium, >10mm = extreme
        
            
        
    def check_delta(self, val):
        if(val>0):
            return 'distraksi'
        elif(val<0):
            return 'kontraksi'
        else:
            return 'normal'
    
    def check_degree(self, val):
        temp = abs(val)
        if(temp>10):
            return 'ekstrem'
        elif(temp>5):
            return 'medium'
        else:
            return 'mild'
    
    def calculate_incisors(self, archs):
        self.incisors_width[ArchType.LOWER.value]=None
        self.incisors_width[ArchType.UPPER.value]=None
        if Arch._is_complete():
            self.teeth_width[ArchType.LOWER.value]={}
            self.teeth_width[ArchType.UPPER.value]={}
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
                        self.teeth_width[arch.arch_type][label]=w
                        self.incisors_width[arch.arch_type]+=w
    
    def calculate_mpv(self, archs):
        self.mpv[ArchType.LOWER.value]=None
        self.mpv[ArchType.UPPER.value]=None
        if Arch._is_complete():
            UPPER_IDX=Arch._get_index_arch_type(ArchType.UPPER.value)
            LOWER_IDX=Arch._get_index_arch_type(ArchType.LOWER.value)
            # idx_maxi_l = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.PIT.value]
            # idx_maxi_r = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.PIT.value]
            
            # maxi_l = archs[UPPER_IDX].mesh.points()[idx_maxi_l]
            # maxi_r = archs[UPPER_IDX].mesh.points()[idx_maxi_r]
            
            maxi_l = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.PIT.value]
            maxi_r = archs[UPPER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.PIT.value]
            self.premolar_pts[ArchType.UPPER.value]=[maxi_l,maxi_r]
            
            # idx_mandi_l1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.DISTAL.value]
            # idx_mandi_l2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.MESIAL.value]
            # idx_mandi_r1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.DISTAL.value]
            # idx_mandi_r2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.MESIAL.value]

            # idx_mandi_l1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.PIT.value]
            # idx_mandi_l2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.PIT.value]
            # idx_mandi_r1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.PIT.value]
            # idx_mandi_r2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.PIT.value]
            
            
            mandi_l1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.DISTAL.value]
            mandi_l2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.MESIAL.value]
            mandi_r1 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.DISTAL.value]
            mandi_r2 = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.MESIAL.value]

            mandi_l1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.PIT.value]
            mandi_l2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.PIT.value]
            mandi_r1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.PIT.value]
            mandi_r2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.PIT.value]


            # mandi_l1_pit = archs[LOWER_IDX].mesh.points()[idx_mandi_l1_pit]
            # mandi_l2_pit = archs[LOWER_IDX].mesh.points()[idx_mandi_l2_pit]
            # mandi_r1_pit = archs[LOWER_IDX].mesh.points()[idx_mandi_r1_pit]
            # mandi_r2_pit = archs[LOWER_IDX].mesh.points()[idx_mandi_r2_pit]
            
            mandi_l1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL4_LR4.value].center
            mandi_l2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UL5_LR5.value].center
            mandi_r1_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR4_LL4.value].center
            mandi_r2_pit = archs[LOWER_IDX].teeth[ToothType.PREMOLAR_UR5_LL5.value].center
            
            

            # mandi_l1 = archs[LOWER_IDX].mesh.points()[idx_mandi_l1]
            # mandi_r1 = archs[LOWER_IDX].mesh.points()[idx_mandi_r1]
            # mandi_l2 = archs[LOWER_IDX].mesh.points()[idx_mandi_l2]
            # mandi_r2 = archs[LOWER_IDX].mesh.points()[idx_mandi_r2]
            
            mandi_l = np.mean([mandi_l1, mandi_l2],axis=0)
            mandi_r = np.mean([mandi_r1, mandi_r2],axis=0)
            
            mandi_l = find_closest_point_between_a_point_and_a_line(mandi_l, np.array([mandi_l1_pit,mandi_l2_pit]))
            mandi_r = find_closest_point_between_a_point_and_a_line(mandi_r, np.array([mandi_r1_pit,mandi_r2_pit]))
            
            self.premolar_pts[ArchType.LOWER.value]=[mandi_l,mandi_r]
        
            self.mpv[ArchType.LOWER.value]=find_distance_between_two_points(mandi_l, mandi_r)
            self.mpv[ArchType.UPPER.value]=find_distance_between_two_points(maxi_l, maxi_r)
            
        
            
    def calculate_mmv(self, archs):
        self.mmv[ArchType.LOWER.value]=None
        self.mmv[ArchType.UPPER.value]=None
        if Arch._is_complete():
            UPPER_IDX=Arch._get_index_arch_type(ArchType.UPPER.value)
            LOWER_IDX=Arch._get_index_arch_type(ArchType.LOWER.value)
            # idx_maxi_l = archs[UPPER_IDX].teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.PIT.value]
            # idx_maxi_r = archs[UPPER_IDX].teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.PIT.value]
            # maxi_l = archs[UPPER_IDX].mesh.points()[idx_maxi_l]
            # maxi_r = archs[UPPER_IDX].mesh.points()[idx_maxi_r]
            maxi_l = archs[UPPER_IDX].teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.PIT.value]
            maxi_r = archs[UPPER_IDX].teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.PIT.value]
            self.molar_pts[ArchType.UPPER.value]=[maxi_l,maxi_r]
            
            # idx_mandi_l = archs[LOWER_IDX].teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.PIT.value]
            # idx_mandi_r = archs[LOWER_IDX].teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.PIT.value]

            # mandi_l = archs[LOWER_IDX].mesh.points()[idx_mandi_l]
            # mandi_r = archs[LOWER_IDX].mesh.points()[idx_mandi_r]    
            
            mandi_l = archs[LOWER_IDX].teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.PIT.value]
            mandi_r = archs[LOWER_IDX].teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.PIT.value]
            self.molar_pts[ArchType.LOWER.value]=[mandi_l,mandi_r]
            
            
        
            self.mmv[ArchType.LOWER.value]=np.linalg.norm(mandi_l - mandi_r)
            self.mmv[ArchType.UPPER.value]=np.linalg.norm(maxi_l - maxi_r)
        
    def calculate_cpv(self):
        self.cpv[ArchType.LOWER.value]=None
        self.cpv[ArchType.UPPER.value]=None
        if Arch._is_complete():
            self.cpv[ArchType.LOWER.value]=self.incisors_width[ArchType.LOWER.value]*100 /self.index_cpv
            self.cpv[ArchType.UPPER.value]=self.incisors_width[ArchType.UPPER.value]*100 /self.index_cpv

    def calculate_cmv(self):
            self.cmv[ArchType.LOWER.value]=None
            self.cmv[ArchType.UPPER.value]=None
            if Arch._is_complete():
                self.cmv[ArchType.LOWER.value]=self.incisors_width[ArchType.LOWER.value]*100 /self.index_cmv
                self.cmv[ArchType.UPPER.value]=self.incisors_width[ArchType.UPPER.value]*100 /self.index_cmv
         