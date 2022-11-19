# pitch
# roll
# yaw

# pivot

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
    QFormLayout,
    QFrame, 
    QScrollArea,
    QSizePolicy
)
import numpy as np
from PyQt5.QtCore import Qt, QSize
from constant.enums import ArchType, LandmarkType, ToothType
from controller.summary_controller import get_flat_plane
from controller.vedo_plotter_controller import remove_not_arch
from utility.arch import Arch
from utility.names import convert_arch_val_to_name
# from view.components.summary_section_group import PontArchSection
from vedo import Line, Point
from utility.splineku import SplineKu
from view.components.line import QHSeperationLine

def create_panel_summary(self, parent_layout):
    self.summary_panel_widget_container = QWidget()
    self.summary_panel_layout_container = QVBoxLayout()
    
    self.summary_panel_widget = QWidget()
    self.summary_panel_layout = QVBoxLayout()
    
    self.summary_panel_widget_area = QScrollArea()
    self.summary_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.summary_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.summary_panel_widget_area.setWidgetResizable(True)
    self.summary_panel_widget_area.setWidget(self.summary_panel_widget)
    
    self.summary_panel_widget.setLayout(self.summary_panel_layout)
    self.summary_panel_layout_container.addWidget(self.summary_panel_widget_area)
    self.summary_panel_widget_container.setLayout(self.summary_panel_layout_container)
    self.summary_panel_widget_container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    self.summary_panel_widget_container.setFixedWidth(600)
    
    self.pane_archs_summary=QWidget()
    self.pane_archs_summary_layout = QVBoxLayout()
    self.pane_archs_summary.setLayout(self.pane_archs_summary_layout)
    self.summary_panel_layout.addWidget(self.pane_archs_summary)
    
    self.summary_panel_layout.addStretch()
    
        
    parent_layout.addWidget(self.summary_panel_widget_container, 1, 11, 20, 1)

    self.summary_panel_widget_container.hide()
    

def create_pane_summary(self):
    if(not Arch._is_complete()):
        for i in reversed(range(self.pane_archs_summary_layout.count())): 
            self.pane_archs_summary_layout.itemAt(i).widget().setParent(None)
    else:
        for i in reversed(range(self.pane_archs_summary_layout.count())): 
            self.pane_archs_summary_layout.itemAt(i).widget().setParent(None)
        idx_max = Arch._get_index_arch_type(ArchType.UPPER.value)
        idx_man = Arch._get_index_arch_type(ArchType.LOWER.value)
        create_pont_summary(self)
        self.pane_archs_summary_layout.addWidget(QHSeperationLine())
        create_korkhaus_summary(self)
        self.pane_archs_summary_layout.addWidget(QHSeperationLine())
        create_bolton_summary(self)
        self.pane_archs_summary_layout.addWidget(QHSeperationLine())
        create_carey_summay(self)
        # get_flat_plane(self)




def create_bolton_summary(self):
    bolton_lbl = QLabel("Bolton")
    self.pane_archs_summary_layout.addWidget(bolton_lbl)
    bolton_summary_widget = QWidget()
    self.pane_archs_summary_layout.addWidget(bolton_summary_widget)
    bolton_summary_layout = QGridLayout()
    bolton_summary_widget.setLayout(bolton_summary_layout)
    
    bolton_max_lbl = QLabel("Max")
    bolton_summary_layout.addWidget(bolton_max_lbl,0,0)
    bolton_max_anterior_lbl = QLabel("Anterior")
    bolton_summary_layout.addWidget(bolton_max_anterior_lbl,1,0)
    bolton_max_anterior = QLabel('{0:.3f}'.format(self.bolton_studi_model.anterior_width[ArchType.UPPER.value]))
    bolton_summary_layout.addWidget(bolton_max_anterior,1,1)
    bolton_max_overall_lbl = QLabel("Overall")
    bolton_summary_layout.addWidget(bolton_max_overall_lbl,2,0)
    bolton_max_overall = QLabel('{0:.3f}'.format(self.bolton_studi_model.overal_width[ArchType.UPPER.value]))
    bolton_summary_layout.addWidget(bolton_max_overall,2,1)
    
    bolton_man_lbl = QLabel("Man")
    bolton_summary_layout.addWidget(bolton_man_lbl,3,0)
    bolton_man_anterior_lbl = QLabel("Anterior")
    bolton_summary_layout.addWidget(bolton_man_anterior_lbl,4,0)
    bolton_man_anterior = QLabel('{0:.3f}'.format(self.bolton_studi_model.anterior_width[ArchType.LOWER.value]))
    bolton_summary_layout.addWidget(bolton_man_anterior,4,1)
    bolton_man_overall_lbl = QLabel("Overall")
    bolton_summary_layout.addWidget(bolton_man_overall_lbl,5,0)
    bolton_man_overall = QLabel('{0:.3f}'.format(self.bolton_studi_model.overal_width[ArchType.LOWER.value]))
    bolton_summary_layout.addWidget(bolton_man_overall,5,1)
    
    bolton_ratio_lbl = QLabel("Ratio")
    bolton_summary_layout.addWidget(bolton_ratio_lbl,6,0)
    bolton_ratio_anterior_lbl = QLabel("Anterior")
    bolton_summary_layout.addWidget(bolton_ratio_anterior_lbl,7,0)
    bolton_ratio_anterior = QLabel('{0:.3f}'.format(self.bolton_studi_model.anterior))
    bolton_summary_layout.addWidget(bolton_ratio_anterior,7,1)
    bolton_ratio_overall_lbl = QLabel("Overall")
    bolton_summary_layout.addWidget(bolton_ratio_overall_lbl,8,0)
    bolton_ratio_overall = QLabel('{0:.3f}'.format(self.bolton_studi_model.overall))
    bolton_summary_layout.addWidget(bolton_ratio_overall,8,1)
    
    bolton_correction_lbl = QLabel("Correction")
    bolton_summary_layout.addWidget(bolton_correction_lbl,9,0)
    bolton_correction_anterior_lbl = QLabel("Anterior")
    bolton_summary_layout.addWidget(bolton_correction_anterior_lbl,10,0)
    bolton_correction_anterior_arch = QLabel(("Max" if self.bolton_studi_model.correction_arch_anterior == ArchType.UPPER.value else "Man"))
    bolton_summary_layout.addWidget(bolton_correction_anterior_arch,10,1)
    bolton_correction_anterior = QLabel('{0:.3f}'.format(self.bolton_studi_model.correction_anterior))
    bolton_summary_layout.addWidget(bolton_correction_anterior,10,2)
    bolton_correction_overall_lbl = QLabel("Overall")
    bolton_summary_layout.addWidget(bolton_correction_overall_lbl,11,0)
    bolton_correction_overall_arch = QLabel(("Max" if self.bolton_studi_model.correction_arch_overall == ArchType.UPPER.value else "Man"))
    bolton_summary_layout.addWidget(bolton_correction_overall_arch,11,1)
    bolton_correction_overall = QLabel('{0:.3f}'.format(self.bolton_studi_model.correction_overall))
    bolton_summary_layout.addWidget(bolton_correction_overall,11,2)
    
    
def create_korkhaus_summary(self):
    korkhaus_lbl = QLabel("Korkhaus")
    self.pane_archs_summary_layout.addWidget(korkhaus_lbl)
    korkhaus_summary_widget = QWidget()
    self.pane_archs_summary_layout.addWidget(korkhaus_summary_widget)
    korkhaus_summary_layout = QGridLayout()
    korkhaus_summary_widget.setLayout(korkhaus_summary_layout)
    korkhaus_max_lbl = QLabel("Max")
    korkhaus_summary_layout.addWidget(korkhaus_max_lbl,0,0)
    korkhaus_max_val = QLabel('{0:.3f}'.format(self.korkhaus_studi_model.status_line_to_width[ArchType.UPPER.value]))
    korkhaus_summary_layout.addWidget(korkhaus_max_val,0,1)
    korkhaus_max_expansion_meaning = QLabel(self.korkhaus_studi_model.status_expansion_meaning[ArchType.UPPER.value])
    korkhaus_summary_layout.addWidget(korkhaus_max_expansion_meaning,0,2)
    korkhaus_man_lbl = QLabel("Man")
    korkhaus_summary_layout.addWidget(korkhaus_man_lbl,1,0)
    korkhaus_man_val = QLabel('{0:.3f}'.format(self.korkhaus_studi_model.status_line_to_width[ArchType.LOWER.value]))
    korkhaus_summary_layout.addWidget(korkhaus_man_val,1,1)
    korkhaus_man_expansion_meaning = QLabel(self.korkhaus_studi_model.status_expansion_meaning[ArchType.LOWER.value])
    korkhaus_summary_layout.addWidget(korkhaus_man_expansion_meaning,1,2)
    korkhaus_line_lbl = QLabel("Line")
    korkhaus_summary_layout.addWidget(korkhaus_line_lbl,2,0)
    korkhaus_line_val = QLabel('{0:.3f}'.format(self.korkhaus_studi_model.status_khorkaus))
    korkhaus_summary_layout.addWidget(korkhaus_line_val,2,1)
    korkhaus_line_expansion_meaning = QLabel(self.korkhaus_studi_model.status_khorkaus_meaning)
    korkhaus_summary_layout.addWidget(korkhaus_line_expansion_meaning,2,2)



def create_carey_summay(self):
    carey_lbl = QLabel("Carey")
    self.pane_archs_summary_layout.addWidget(carey_lbl)
    carey_summary_widget = QWidget()
    self.pane_archs_summary_layout.addWidget(carey_summary_widget)
    carey_summary_layout = QGridLayout()
    carey_summary_widget.setLayout(carey_summary_layout)
    
    carey_max_lbl = QLabel("Max")
    carey_summary_layout.addWidget(carey_max_lbl,0,0,1,1)
    carey_max_meaning_lbl = QLabel(self.carey_studi_model.arch_length_descrepancy_meaning[ArchType.UPPER.value])
    carey_summary_layout.addWidget(carey_max_meaning_lbl,1,0,1,3)
    
    carey_man_lbl = QLabel("Man")
    carey_summary_layout.addWidget(carey_man_lbl,2,0,1,1)
    carey_man_meaning_lbl = QLabel(self.carey_studi_model.arch_length_descrepancy_meaning[ArchType.LOWER.value])
    carey_summary_layout.addWidget(carey_man_meaning_lbl,3,0,1,3)


def create_pont_summary(self):
    pont_lbl = QLabel("Pont")
    self.pane_archs_summary_layout.addWidget(pont_lbl)
    pont_summary_widget = QWidget()
    self.pane_archs_summary_layout.addWidget(pont_summary_widget)
    pont_summary_layout = QGridLayout()
    pont_summary_widget.setLayout(pont_summary_layout)
    pont_max_lbl = QLabel("Max")
    pont_summary_layout.addWidget(pont_max_lbl,0,0,1,1)
    pont_max_p_lbl = QLabel("Premolar")
    pont_summary_layout.addWidget(pont_max_p_lbl,1,0,1,1)
    pont_max_p_result = QLabel('{0:.3f}'.format(self.pont_studi_model.delta_pv[ArchType.UPPER.value]))
    pont_summary_layout.addWidget(pont_max_p_result,1,1,1,1)
    pont_max_p_status = QLabel(self.pont_studi_model.status_pv[ArchType.UPPER.value])
    pont_summary_layout.addWidget(pont_max_p_status,1,2,1,1)
    pont_max_p_degree_status = QLabel(self.pont_studi_model.degree_status_pv[ArchType.UPPER.value])
    pont_summary_layout.addWidget(pont_max_p_degree_status,1,3,1,1)
    
    pont_max_m_lbl = QLabel("Molar")
    pont_summary_layout.addWidget(pont_max_m_lbl,2,0,1,1)
    pont_max_m_result = QLabel('{0:.3f}'.format(self.pont_studi_model.delta_mp[ArchType.UPPER.value]))
    pont_summary_layout.addWidget(pont_max_m_result,2,1,1,1)
    pont_max_m_status = QLabel(self.pont_studi_model.status_mp[ArchType.UPPER.value])
    pont_summary_layout.addWidget(pont_max_m_status,2,2,1,1)
    pont_max_m_degree_status = QLabel(self.pont_studi_model.degree_status_mp[ArchType.UPPER.value])
    pont_summary_layout.addWidget(pont_max_m_degree_status,2,3,1,1)
    
    pont_man_lbl = QLabel("Man")
    pont_summary_layout.addWidget(pont_man_lbl,3,0,1,1)
    pont_man_p_lbl = QLabel("Premolar")
    pont_summary_layout.addWidget(pont_man_p_lbl,4,0,1,1)
    pont_man_p_result = QLabel('{0:.3f}'.format(self.pont_studi_model.delta_pv[ArchType.LOWER.value]))
    pont_summary_layout.addWidget(pont_man_p_result,4,1,1,1)
    pont_man_p_status = QLabel(self.pont_studi_model.status_pv[ArchType.LOWER.value])
    pont_summary_layout.addWidget(pont_man_p_status,4,2,1,1)
    pont_man_p_degree_status = QLabel(self.pont_studi_model.degree_status_pv[ArchType.LOWER.value])
    pont_summary_layout.addWidget(pont_man_p_degree_status,4,3,1,1)
    
    pont_man_m_lbl = QLabel("Molar")
    pont_summary_layout.addWidget(pont_man_m_lbl,5,0,1,1)
    pont_man_m_result = QLabel('{0:.3f}'.format(self.pont_studi_model.delta_mp[ArchType.LOWER.value]))
    pont_summary_layout.addWidget(pont_man_m_result,5,1,1,1)
    pont_man_m_status = QLabel(self.pont_studi_model.status_mp[ArchType.LOWER.value])
    pont_summary_layout.addWidget(pont_man_m_status,5,2,1,1)
    pont_man_m_degree_status = QLabel(self.pont_studi_model.degree_status_mp[ArchType.LOWER.value])
    pont_summary_layout.addWidget(pont_man_m_degree_status,5,3,1,1)


def draw_summary_lines(self):
    remove_not_arch(self,excepts_name_like='attachment')
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
                
            # elif(t in teeth_type_korkhaus):
            #     center = teeth[t].center
            #     center_arch = msh.centerOfMass()
            #     v=center-center_arch
            #     vv=np.linalg.norm(v)
            #     u = v/vv
            #     xx = self.korkhaus_studi_model.status_line_to_width[i.value]
            #     # if("ekspansi" in self.korkhaus_studi_model.status_expansion_meaning[i.value]):
            #     # elif ("retraksi" in self.korkhaus_studi_model.status_expansion_meaning[i.value])
            #     xx *= -1
            #     dd=vv-xx
            #     new_center = np.array(center_arch) + (dd*u)
            #     preds.append(new_center)
                
            elif(tooth_type in teeth_type_anterior ):
                if(self.bolton_studi_model.correction_arch_anterior == i.value):
                    center = teeth[tooth_type].center
                    center_arch = msh.centerOfMass()
                    v=center-center_arch
                    vv=np.linalg.norm(v)
                    u = v/vv
                    proklinasi_atas=0
                    if(i.value == ArchType.UPPER.value):
                        proklinasi_atas=self.korkhaus_studi_model.status_khorkaus
                    print("proklinasi atas", proklinasi_atas)
                    dd=vv-(self.bolton_studi_model.correction_anterior+proklinasi_atas)
                    new_center = np.array(center_arch) + (dd*u)
                    # calc korkhaus
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        msh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]],
                        msh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]]
                    ], axis=0)
                    d=(batas_awal - batas_akhir) / np.linalg.norm(batas_awal - batas_akhir)
                    v = new_center - batas_akhir
                    t = np.dot(v,d)
                    P = batas_akhir + t * d
                    center = new_center
                    center_arch = P
                    v=center-center_arch
                    vv=np.linalg.norm(v)
                    u = v/vv
                    xx = self.korkhaus_studi_model.status_line_to_width[i.value]
                    xx *= -1
                    dd=vv-xx
                    new_center = np.array(center_arch) + (dd*u)
                    preds.append(new_center)
                else:
                    center = teeth[tooth_type].center
                    center_arch = msh.centerOfMass()
                    v=center-center_arch
                    vv=np.linalg.norm(v)
                    u = v/vv
                    proklinasi_atas=0
                    if(i.value == ArchType.UPPER.value):
                        proklinasi_atas=self.korkhaus_studi_model.status_khorkaus
                    print("proklinasi atas bukan di bolton", proklinasi_atas)
                    dd=vv-(proklinasi_atas)
                    new_center = np.array(center_arch) + (dd*u)
                    
                    
                    batas_awal = msh.centerOfMass()
                    batas_akhir = np.mean([
                        msh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]],
                        msh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]]
                    ], axis=0)
                    d=(batas_awal - batas_akhir) / np.linalg.norm(batas_awal - batas_akhir)
                    v = new_center - batas_akhir
                    t = np.dot(v,d)
                    P = batas_akhir + t * d
                    center = new_center
                    center_arch = P
                    v=center-center_arch
                    vv=np.linalg.norm(v)
                    u = v/vv
                    xx = self.korkhaus_studi_model.status_line_to_width[i.value]
                    xx *= -1
                    dd=vv-xx
                    new_center = np.array(center_arch) + (dd*u)
                    preds.append(new_center)
            
            elif(tooth_type in teeth_type_pont):
                batas_awal = msh.centerOfMass()
                batas_akhir = np.mean([
                    msh.points()[teeth[ToothType.INCISOR_UL1_LR1.value].landmark_index[LandmarkType.MESIAL.value]],
                    msh.points()[teeth[ToothType.INCISOR_UR1_LL1.value].landmark_index[LandmarkType.MESIAL.value]]
                ], axis=0)
                d=(batas_awal - batas_akhir) / np.linalg.norm(batas_awal - batas_akhir)
                v = teeth[tooth_type].center - batas_akhir
                t = np.dot(v,d)
                P = batas_akhir + t * d
                
                center = teeth[tooth_type].center
                center_arch = P
                v=center-center_arch
                vv=np.linalg.norm(v)
                u = v/vv
                val_cor = None
                val_cor_status=None
                if(tooth_type in [ToothType.MOLAR_UL6_LR6.value, ToothType.MOLAR_UR6_LL6.value]):
                    val_cor = self.pont_studi_model.delta_mp[i.value]/2.0
                    val_cor_status = self.pont_studi_model.status_mp[i.value]
                elif(tooth_type in [ToothType.PREMOLAR_UL4_LR4.value, ToothType.PREMOLAR_UR4_LL4.value]):
                    val_cor = self.pont_studi_model.delta_pv[i.value]/2.0
                    val_cor_status=self.pont_studi_model.status_pv[i.value]
                # if(val_cor_status=="kontraksi"):
                val_cor*=-1
                dd=vv-val_cor
                new_center = np.array(center_arch) + (dd*u)
                preds.append(new_center)
            
            
            
        print("legacies", legacies)
        print("preds",preds)
        
        draw_spline(self, legacies, False, i.value)
        draw_spline(self, preds, True, i.value)

def draw_spline(self, pts, isPred, arch):
    c = 'orange'
    if(isPred):
        c='green'
    if(arch == ArchType.UPPER.value):
        c+='5'
    line = SplineKu(pts, degree=3, smooth=0, res=600)
    line.ps(8)
    line.c(c)
    self.model_plot.add(line)
    for pt in pts:
        self.model_plot.add(Point(pt))
    self.model_plot.render()
    
def draw_spline_flat(self):
    coords = get_flat_plane(self)
    for pts in coords:
        print(pts)
        c = 'blue4'
        line = SplineKu(pts, degree=3, smooth=0, res=600)
        line.ps(8)
        line.c(c)
        self.model_plot.add(line)
        for pt in pts:
            self.model_plot.add(Point(pt))
        self.model_plot.render()
    