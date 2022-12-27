import numpy as np

from vedo import Point
from constant.enums import ArchType, LandmarkType, ToothType
from utility.arch import Arch
from utility.calculation import find_closest_point_between_a_point_and_a_3pts_plane, find_closest_point_between_a_point_and_a_line, find_new_point_in_a_line_with_delta_distance, find_new_point_in_a_line_with_new_distance
# from controller.step_controller import add_transform_arch


def init_summary(self):
    self.summary_flat_pts = None
    self.studi_model_summary_pts=None

def calculate_studi_model(self):
    if(Arch._is_complete()):
        # for m in self.models:
        #     m.extract_tooth()
        self.bolton_studi_model.calc_anterior_overall(self.models)
        # print("get_anterior_overall",self.bolton_studi_model.get_anterior_overall())
        # print("overjet",self.bolton_studi_model.get_overjet())
        self.korkhaus_studi_model.calculate_khorkaus(self.models)
        self.pont_studi_model.calculate_pont(self.models)
        self.carey_studi_model.calculate_carey(self.models)
        self.summary_flat_pts = calculate_flat_plane_points(self)
        self.studi_model_summary_pts=calculate_studi_model_summary_pts(self)
        print("self.studi_model_summary_pts")
        print(self.studi_model_summary_pts)
        print()
        
        
def get_studi_model_summary_pts(self):
    return self.studi_model_summary_pts

def get_summary_flat_pts(self):
    return self.summary_flat_pts



def calculate_flat_plane_points(self):
    if Arch._is_complete():
        coords = {}
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            pts = np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                np.mean([
                    teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                    teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                ], axis=0),
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
            pts_cusps=np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                
                teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
            new_coords = []
            for pt in pts_cusps:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords.append(new_coord)
            coords[i.value] = new_coords
        return coords
    else:
        return {}
    
def calculate_studi_model_summary_pts(self):
    res = {}
    if(Arch._is_complete()):
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            msh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            preds=[]
            legacies=[]
            teeth_type=[
                ToothType.MOLAR_UL7_LR7.value,
                ToothType.MOLAR_UR7_LL7.value
            ]
            teeth_type_pont=[

                ToothType.MOLAR_UL6_LR6.value,
                ToothType.PREMOLAR_UL4_LR4.value,

                ToothType.PREMOLAR_UR4_LL4.value,
                ToothType.MOLAR_UR6_LL6.value,
            ]
            teeth_type_anterior=[
                ToothType.CANINE_UL3_LR3.value,
                ToothType.INCISOR_UL2_LR2.value,
                ToothType.INCISOR_UL1_LR1.value,
                
                ToothType.INCISOR_UR1_LL1.value,
                ToothType.INCISOR_UR2_LL2.value,
                ToothType.CANINE_UR3_LL3.value,
            ]
            for tooth_type in teeth:
                if (tooth_type in teeth_type or tooth_type in teeth_type_anterior or tooth_type in teeth_type_pont):
                    legacies.append(teeth[tooth_type].center)
                
                if(tooth_type in teeth_type):
                    preds.append(teeth[tooth_type].center)
                elif(tooth_type in teeth_type_anterior ):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    
                    anterior_korkhaus_should_move=self.korkhaus_studi_model.status_line_to_width[i.value]
                    
                    new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(anterior_korkhaus_should_move)))
                    # P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                    # center = new_center
                    # center_arch = P
                    # new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                    preds.append(new_center)
                
                elif(tooth_type in teeth_type_pont):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    P=find_closest_point_between_a_point_and_a_line(teeth[tooth_type].center,[batas_awal,batas_akhir])
                    center = teeth[tooth_type].center
                    center_arch = P
                    val_cor = None
                    val_cor_status=None
                    if(tooth_type in [ToothType.MOLAR_UL6_LR6.value, ToothType.MOLAR_UR6_LL6.value]):
                        val_cor = -1*(self.pont_studi_model.delta_mp[i.value]/2.0)
                        val_cor_status = self.pont_studi_model.status_mp[i.value]
                    elif(tooth_type in [ToothType.PREMOLAR_UL4_LR4.value, ToothType.PREMOLAR_UR4_LL4.value]):
                        val_cor = -1*(self.pont_studi_model.delta_pv[i.value]/2.0)
                        val_cor_status=self.pont_studi_model.status_pv[i.value]
                    new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, val_cor)
                    preds.append(new_center)
            line_molar = [legacies[0],legacies[-1]]
            preds[0] = find_closest_point_between_a_point_and_a_line(preds[1],line_molar)
            preds[-1] = find_closest_point_between_a_point_and_a_line(preds[-2],line_molar)
            res[i.value]=[legacies,preds]
    return res        
                    
def calculate_studi_model_summary_pts_lama(self): #DEPRECETED
    res = {}
    if(Arch._is_complete()):
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            msh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            preds=[]
            legacies=[]
            teeth_type=[
                ToothType.MOLAR_UL7_LR7.value,
                ToothType.MOLAR_UR7_LL7.value
            ]
            teeth_type_pont=[

                ToothType.MOLAR_UL6_LR6.value,
                ToothType.PREMOLAR_UL4_LR4.value,

                ToothType.PREMOLAR_UR4_LL4.value,
                ToothType.MOLAR_UR6_LL6.value,
            ]
            teeth_type_anterior=[
                ToothType.CANINE_UL3_LR3.value,
                ToothType.INCISOR_UL2_LR2.value,
                ToothType.INCISOR_UL1_LR1.value,
                
                ToothType.INCISOR_UR1_LL1.value,
                ToothType.INCISOR_UR2_LL2.value,
                ToothType.CANINE_UR3_LL3.value,
            ]
            for tooth_type in teeth:
                if (tooth_type in teeth_type or tooth_type in teeth_type_anterior or tooth_type in teeth_type_pont):
                    legacies.append(teeth[tooth_type].center)
                
                if(tooth_type in teeth_type):
                    preds.append(teeth[tooth_type].center)

                elif(tooth_type in teeth_type_anterior ):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    proklinasi_atas=0
                    if(i.value == ArchType.UPPER.value):
                        proklinasi_atas=self.korkhaus_studi_model.status_khorkaus
                    if(self.bolton_studi_model.correction_arch_anterior == i.value):
                        new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(self.bolton_studi_model.correction_anterior+proklinasi_atas)))
                        P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                        center = new_center
                        center_arch = P
                        new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                        preds.append(new_center)
                    else:
                        new_center = find_new_point_in_a_line_with_delta_distance( msh.centerOfMass(), teeth[tooth_type].center, (-1*(proklinasi_atas)))
                        P=find_closest_point_between_a_point_and_a_line(new_center,[batas_awal,batas_akhir])
                        center = new_center
                        center_arch = P
                        new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, self.korkhaus_studi_model.status_line_to_width[i.value])
                        preds.append(new_center)
                        
                elif(tooth_type in teeth_type_pont):
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.MESIAL.value],
                        teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.MESIAL.value]
                    ], axis=0)
                    P=find_closest_point_between_a_point_and_a_line(teeth[tooth_type].center,[batas_awal,batas_akhir])
                    center = teeth[tooth_type].center
                    center_arch = P
                    val_cor = None
                    val_cor_status=None
                    if(tooth_type in [ToothType.MOLAR_UL6_LR6.value, ToothType.MOLAR_UR6_LL6.value]):
                        val_cor = self.pont_studi_model.delta_mp[i.value]/2.0
                        val_cor_status = self.pont_studi_model.status_mp[i.value]
                    elif(tooth_type in [ToothType.PREMOLAR_UL4_LR4.value, ToothType.PREMOLAR_UR4_LL4.value]):
                        val_cor = self.pont_studi_model.delta_pv[i.value]/2.0
                        val_cor_status=self.pont_studi_model.status_pv[i.value]
                    new_center = find_new_point_in_a_line_with_delta_distance(center_arch, center, val_cor)
                    preds.append(new_center)
            res[i.value]=[legacies,preds]
    return res
                        
def get_flat_plane_DEPRECATED(self): # deprecated
    if Arch._is_complete():
        coords = []
        for i in ArchType:
            idx = Arch._get_index_arch_type(i.value)
            mesh = self.models[idx].mesh
            teeth = self.models[idx].teeth
            
            # pts = np.array([
            #     mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            #     np.mean([
            #         mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
            #         mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]]
            #     ], axis=0),
            #     mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]]
            # ])
            pts = np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                np.mean([
                    teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                    teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                ], axis=0),
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
            for pp in pts:
                self.model_plot.add(Point(pp, c="violet"))
            print("pts plane",pts)
            # n = np.cross(pts[0]-pts[1],pts[2]-pts[1])
            # n = n/np.linalg.norm(n)
            # pts_cusps=np.array([
            #     mesh.points()[teeth[ToothType.MOLAR_UL7_LR7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UL6_LR6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.CANINE_UL3_LR3.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UL2_LR2.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.CUSP.value]],
                
            #     mesh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.INCISOR_UR2_LL2.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.CANINE_UR3_LL3.value].landmark_index[LandmarkType.CUSP.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_index[LandmarkType.CUSP_OUT.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UR6_LL6.value].landmark_index[LandmarkType.CUSP_OUT_MESIAL.value]],
            #     mesh.points()[teeth[ToothType.MOLAR_UR7_LL7.value].landmark_index[LandmarkType.CUSP_OUT_DISTAL.value]],
            # ])
            pts_cusps=np.array([
                teeth[ToothType.MOLAR_UL7_LR7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
                teeth[ToothType.MOLAR_UL6_LR6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.PREMOLAR_UL5_LR5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UL4_LR4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.CANINE_UL3_LR3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL2_LR2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UL1_LR1.value].landmark_pt[LandmarkType.CUSP.value],
                
                teeth[ToothType.INCISOR_UR1_LL1.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.INCISOR_UR2_LL2.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.CANINE_UR3_LL3.value].landmark_pt[LandmarkType.CUSP.value],
                teeth[ToothType.PREMOLAR_UR4_LL4.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.PREMOLAR_UR5_LL5.value].landmark_pt[LandmarkType.CUSP_OUT.value],
                teeth[ToothType.MOLAR_UR6_LL6.value].landmark_pt[LandmarkType.CUSP_OUT_MESIAL.value],
                teeth[ToothType.MOLAR_UR7_LL7.value].landmark_pt[LandmarkType.CUSP_OUT_DISTAL.value],
            ])
            
            print("pts_cusps",pts_cusps)
            new_coords = []
            for pt in pts_cusps:
                # new_coord = abs(np.dot(pt - pts[1],n))
                new_coord = find_closest_point_between_a_point_and_a_3pts_plane(pt, pts)
                new_coords.append(new_coord)
            coords.append(new_coords)
        return coords
    else:
        return []
            
            

    