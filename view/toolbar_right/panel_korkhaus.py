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
from view.components.korkhaus_section_group import KorkhausArchSection

def create_panel_korkhaus(self, parent_layout):
    self.korkhaus_panel_widget_container = QWidget()
    self.korkhaus_panel_layout_container = QVBoxLayout()
    
    self.korkhaus_panel_widget = QWidget()
    self.korkhaus_panel_layout = QVBoxLayout()
    
    self.korkhaus_panel_widget_area = QScrollArea()
    self.korkhaus_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.korkhaus_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.korkhaus_panel_widget_area.setWidgetResizable(True)
    self.korkhaus_panel_widget_area.setWidget(self.korkhaus_panel_widget)
    
    self.korkhaus_panel_widget.setLayout(self.korkhaus_panel_layout)
    self.korkhaus_panel_layout_container.addWidget(self.korkhaus_panel_widget_area)
    self.korkhaus_panel_widget_container.setLayout(self.korkhaus_panel_layout_container)
    self.korkhaus_panel_widget_container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    self.korkhaus_panel_widget_container.setFixedWidth(600)
    
    self.pane_arch_korkhaus=QWidget()
    self.korkhaus_panel_layout.addWidget(self.pane_arch_korkhaus)
    
    self.korkhaus_summary_label=QLabel()
    self.korkhaus_panel_layout.addWidget(self.korkhaus_summary_label)
    self.korkhaus_panel_layout.addStretch()
    
        
    parent_layout.addWidget(self.korkhaus_panel_widget_container, 1, 11, 20, 1)

    self.korkhaus_panel_widget_container.hide()
    

def create_pane_korkhaus(self):
    if(self.pane_arch_korkhaus!=None):
        self.korkhaus_panel_layout.removeWidget(self.pane_arch_korkhaus)
    self.pane_arch_korkhaus=QWidget()
    pane_arch_layout = QVBoxLayout()
    self.pane_arch_korkhaus.setLayout(pane_arch_layout)
    for i in ArchType:
        arch_section_group = QWidget()
        arch_section_group_layout = QVBoxLayout()
        arch_section_group.setLayout(arch_section_group_layout)
        label = QLabel(convert_arch_val_to_name(i.value))
        k_line = self.korkhaus_studi_model.khorkaus_line[i.value]
        arch_section = KorkhausArchSection(k_line)
        arch_section_group_layout.addWidget(label)
        arch_section_group_layout.addWidget(arch_section)
        pane_arch_layout.addWidget(arch_section_group)
    self.korkhaus_panel_layout.insertWidget(self.korkhaus_panel_layout.layout().count()-2, self.pane_arch_korkhaus)


def draw_korkhaus_lines(self):
    remove_not_arch(self, excepts_name_like='attachment')
    for i in ArchType:
        center_i = self.korkhaus_studi_model.center_incisor_points[i.value]
        perpendi = self.korkhaus_studi_model.perpendicular_points[i.value]
        
        color = 'red'
        if(i.value == ArchType.UPPER.value):
            color='orange'
        
        p_c = Point(center_i,c=color,r=20)
        p_p = Point(perpendi,c=color, r=20)
        l = Line(center_i, perpendi, c=color, lw=2)
        self.model_plot.add(p_c)
        self.model_plot.add(p_p)
        self.model_plot.add(l)
        self.model_plot.render()
        
        