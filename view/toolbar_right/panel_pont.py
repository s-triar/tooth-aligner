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

from PyQt5.QtCore import Qt, QSize
from constant.enums import ArchType
from controller.vedo_plotter_controller import remove_not_arch
from utility.arch import Arch
from utility.names import convert_arch_val_to_name
from view.components.pont_section_group import PontArchSection
from vedo import Line, Point

def create_panel_pont(self, parent_layout):
    self.pont_panel_widget_container = QWidget()
    self.pont_panel_layout_container = QVBoxLayout()
    
    self.pont_panel_widget = QWidget()
    self.pont_panel_layout = QVBoxLayout()
    
    self.pont_panel_widget_area = QScrollArea()
    self.pont_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.pont_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.pont_panel_widget_area.setWidgetResizable(True)
    self.pont_panel_widget_area.setWidget(self.pont_panel_widget)
    
    self.pont_panel_widget.setLayout(self.pont_panel_layout)
    self.pont_panel_layout_container.addWidget(self.pont_panel_widget_area)
    self.pont_panel_widget_container.setLayout(self.pont_panel_layout_container)
    self.pont_panel_widget_container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    self.pont_panel_widget_container.setFixedWidth(600)
    
    self.pane_arch_pont=QWidget()
    self.pont_panel_layout.addWidget(self.pane_arch_pont)
    
    self.pont_summary_label=QLabel()
    self.pont_panel_layout.addWidget(self.pont_summary_label)
    self.pont_panel_layout.addStretch()
    
        
    parent_layout.addWidget(self.pont_panel_widget_container, 1, 11, 20, 1)

    self.pont_panel_widget_container.hide()
    

def create_pane_pont(self):
    if(self.pane_arch_pont!=None):
        self.pont_panel_layout.removeWidget(self.pane_arch_pont)
    self.pane_arch_pont=QWidget()
    pane_arch_layout = QVBoxLayout()
    self.pane_arch_pont.setLayout(pane_arch_layout)
    for i in ArchType:
        arch_section_group = QWidget()
        arch_section_group_layout = QVBoxLayout()
        arch_section_group.setLayout(arch_section_group_layout)
        label = QLabel(convert_arch_val_to_name(i.value))
        # print(self.pont_studi_model.incisors_width)
        incisor_w = self.pont_studi_model.incisors_width[i.value]
        premolar_dist = self.pont_studi_model.mpv[i.value]
        molar_dist = self.pont_studi_model.mmv[i.value]
        premolar_dist_calc = self.pont_studi_model.cpv[i.value]
        molar_dist_calc = self.pont_studi_model.cmv[i.value]
        
        arch_section = PontArchSection(incisor_w, premolar_dist, molar_dist, premolar_dist_calc, molar_dist_calc)
        arch_section_group_layout.addWidget(label)
        arch_section_group_layout.addWidget(arch_section)
        pane_arch_layout.addWidget(arch_section_group)
    
    self.pont_panel_layout.insertWidget(self.pont_panel_layout.layout().count()-2, self.pane_arch_pont)
    
def draw_pont_lines(self):
    remove_not_arch(self,excepts_name_like='attachment')
    for i in ArchType:
        idx = Arch._get_index_arch_type(i.value)
        msh = self.models[idx].mesh
        idx_premolar1l = self.pont_studi_model.premolar_index[i.value][0]
        idx_premolar1r= self.pont_studi_model.premolar_index[i.value][1]
        idx_molar1l= self.pont_studi_model.molar_index[i.value][0]
        idx_molar1r= self.pont_studi_model.molar_index[i.value][1]
        
        premolar1l = msh.points()[idx_premolar1l]
        premolar1r= msh.points()[idx_premolar1r]
        molar1l= msh.points()[idx_molar1l]
        molar1r= msh.points()[idx_molar1r]
        color = 'orange'
        if(i.value == ArchType.UPPER.value):
            color='green'
        line_pre = Line(premolar1l, premolar1r, c=color, lw=2)
        line_mol = Line(molar1l, molar1r, c=color, lw=2)
        p_pre_l = Point(premolar1l, r=20, c=color)
        p_pre_r = Point(premolar1r, r=20, c=color)
        # print(molar1l)
        p_mol_l = Point(molar1l, r=20, c=color)
        p_mol_r = Point(molar1r, r=20, c=color)
        self.model_plot.add(p_pre_l)
        self.model_plot.add(p_pre_r)
        self.model_plot.add(p_mol_l)
        self.model_plot.add(p_mol_r)
        
        
        self.model_plot.add(line_pre)
        self.model_plot.add(line_mol)
        self.model_plot.render()
        