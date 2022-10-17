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
    pass
    # if(self.pane_arch_carey!=None):
    #     self.carey_panel_layout.removeWidget(self.pane_arch_carey)
    # self.pane_arch_carey=QWidget()
    # pane_arch_layout = QVBoxLayout()
    # self.pane_arch_carey.setLayout(pane_arch_layout)
    # for i in ArchType:
    #     arch_section_group = QWidget()
    #     arch_section_group_layout = QVBoxLayout()
    #     arch_section_group.setLayout(arch_section_group_layout)
    #     label = QLabel(convert_arch_val_to_name(i.value))
    #     k_line = self.carey_studi_model.khorkaus_line[i.value]
    #     arch_section = KorkhausArchSection(k_line)
    #     arch_section_group_layout.addWidget(label)
    #     arch_section_group_layout.addWidget(arch_section)
    #     pane_arch_layout.addWidget(arch_section_group)
    # self.carey_panel_layout.insertWidget(self.carey_panel_layout.layout().count()-2, self.pane_arch_carey)


        
        