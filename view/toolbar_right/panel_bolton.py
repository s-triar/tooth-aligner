
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
    QSizePolicy,
    QComboBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
from constant.enums import ToothType
from utility.colors import convert_label_to_color
from constant.enums import ArchType
from utility.names import convert_arch_val_to_name
from view.components.landmarking_section_group import LandmarkArchGroup
from view.components.tool_top_button import ToolTopButton
from view.components.bolton_section_group import BoltonArchSection

def create_panel_bolton(self, parent_layout):
    self.bolton_panel_widget_container = QWidget()
    self.bolton_panel_layout_container = QVBoxLayout()
    
    self.bolton_panel_widget = QWidget()
    self.bolton_panel_layout = QVBoxLayout()
    
    self.bolton_panel_widget_area = QScrollArea()
    self.bolton_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.bolton_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.bolton_panel_widget_area.setWidgetResizable(True)
    self.bolton_panel_widget_area.setWidget(self.bolton_panel_widget)
    
    self.bolton_panel_widget.setLayout(self.bolton_panel_layout)
    self.bolton_panel_layout_container.addWidget(self.bolton_panel_widget_area)
    self.bolton_panel_widget_container.setLayout(self.bolton_panel_layout_container)
    self.bolton_panel_widget_container.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    self.bolton_panel_widget_container.setFixedWidth(600)
    
    self.pane_arch_bolton=QWidget()
    self.bolton_panel_layout.addWidget(self.pane_arch_bolton)
    
    self.bolton_summary_label=QLabel()
    self.bolton_panel_layout.addWidget(self.bolton_summary_label)
    self.bolton_panel_layout.addStretch()
    parent_layout.addWidget(self.bolton_panel_widget_container, 1, 11, 20, 1)
    self.bolton_panel_widget_container.hide()
    
    

def create_total_tooth_material_widget(self):
    if(self.pane_arch_bolton!=None):
        self.bolton_panel_layout.removeWidget(self.pane_arch_bolton)
    self.pane_arch_bolton=QWidget()
    pane_arch_layout = QHBoxLayout()
    self.pane_arch_bolton.setLayout(pane_arch_layout)
    for i in ArchType:
        arch_section_group = QWidget()
        arch_section_group_layout = QVBoxLayout()
        arch_section_group.setLayout(arch_section_group_layout)
        label = QLabel(convert_arch_val_to_name(i.value))
        teeth_w = self.bolton_studi_model.teeth_width[i.value]
        arch_section = BoltonArchSection(teeth_w)
        arch_section_group_layout.addWidget(label)
        arch_section_group_layout.addWidget(arch_section)
        pane_arch_layout.addWidget(arch_section_group)
    
    self.bolton_panel_layout.insertWidget(self.bolton_panel_layout.layout().count()-2, self.pane_arch_bolton)
    # self.landmark_panel_widget_container.setObjectName('panel_tool_right')
    
    
    
    
# def reset_toggle_btn_segmentation_arch(self, b, toogle_arch_btn):
#     btns = toogle_arch_btn.findChildren(ToolTopButton)
#     for btn in btns:
#         if btn.isChecked() and btn != b:
#             btn.setChecked(False)
    
# def toggle_btn_segmentation_max(self, e):
#     if e:
#         self.landmark_max.show()
#     else:
#         self.landmark_max.hide()
        
# def toggle_btn_segmentation_man(self, e):
#     if e:
#         self.landmark_man.show()
#     else:
#         self.landmark_man.hide()