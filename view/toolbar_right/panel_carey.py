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
from vedo import Line, Point
from PyQt5.QtCore import Qt, QSize
from constant.enums import ArchType
from controller.vedo_plotter_controller import remove_not_arch
from utility.names import convert_arch_val_to_name
from utility.splineku import SplineKu
from view.components.carey_section_group import CareyArchSection
# from view.components.carey_section_group import KorkhausArchSection

def create_panel_carey(self, parent_layout):
    self.carey_panel_widget_container = QWidget()
    self.carey_panel_layout_container = QVBoxLayout()
    
    self.carey_panel_widget = QWidget()
    self.carey_panel_layout = QVBoxLayout()
    
    self.carey_panel_widget_area = QScrollArea()
    self.carey_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.carey_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.carey_panel_widget_area.setWidgetResizable(True)
    self.carey_panel_widget_area.setWidget(self.carey_panel_widget)
    
    self.carey_panel_widget.setLayout(self.carey_panel_layout)
    self.carey_panel_layout_container.addWidget(self.carey_panel_widget_area)
    self.carey_panel_widget_container.setLayout(self.carey_panel_layout_container)
    self.carey_panel_widget_container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    self.carey_panel_widget_container.setFixedWidth(600)
    
    self.pane_arch_carey=QWidget()
    self.carey_panel_layout.addWidget(self.pane_arch_carey)
    
    self.carey_summary_label=QLabel()
    self.carey_panel_layout.addWidget(self.carey_summary_label)
    self.carey_panel_layout.addStretch()
    
        
    parent_layout.addWidget(self.carey_panel_widget_container, 1, 11, 20, 1)

    self.carey_panel_widget_container.hide()
    

def create_pane_carey(self):
    if(self.pane_arch_carey!=None):
        self.carey_panel_layout.removeWidget(self.pane_arch_carey)
    self.pane_arch_carey=QWidget()
    pane_arch_layout = QVBoxLayout()
    self.pane_arch_carey.setLayout(pane_arch_layout)
    for i in ArchType:
        arch_section_group = QWidget()
        arch_section_group_layout = QVBoxLayout()
        arch_section_group.setLayout(arch_section_group_layout)
        label = QLabel(convert_arch_val_to_name(i.value))
        ttm = self.carey_studi_model.total_tooth_material[i.value]
        brasswire = self.carey_studi_model.brass_wire_step_length[i.value]
        descrepancy = self.carey_studi_model.arch_length_descrepancy[i.value]
        
        arch_section = CareyArchSection(ttm, brasswire,descrepancy)
        arch_section_group_layout.addWidget(label)
        arch_section_group_layout.addWidget(arch_section)
        pane_arch_layout.addWidget(arch_section_group)
    self.carey_panel_layout.insertWidget(self.carey_panel_layout.layout().count()-2, self.pane_arch_carey)


def draw_carey_lines(self):
    remove_not_arch(self,excepts_name_like='attachment')
    for i in ArchType:
        ttm = self.carey_studi_model.ttm_points[i.value]
        brasswire = self.carey_studi_model.brasswire_points[i.value]
        color_ttm='red'
        color_brass='blue'
        if(i.value == ArchType.UPPER.value):
            color_ttm='yellow'
            color_brass='green'
        brasswire_spline = SplineKu(brasswire, degree=3, smooth=0, res=600).lineColor(color_brass)
        ttm_line = []
        ttm_line.append(Line(ttm[0],ttm[1]).lineColor(color_ttm))
        for j in range(1,21,2):
            ttm_line.append(Line(ttm[j],ttm[j+1]).lineColor(color_ttm))
        ttm_line.append(Line(ttm[20],ttm[21]).lineColor(color_ttm))
        self.model_plot.add(brasswire_spline)
        self.model_plot.add(ttm_line)
        self.model_plot.render()
        

