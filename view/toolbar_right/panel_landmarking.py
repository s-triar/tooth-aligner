
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
from vedo import Line, Point
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5 import QtWidgets
from constant.enums import PanelMode, ToothType
from controller.landmarking_controller import draw_eigen_arch, get_selected_arch_landmark, set_selected_arch_show_landmarking, show_landmark
from controller.vedo_plotter_controller import remove_not_arch
from utility.colors import convert_label_to_color, convert_landmark_to_color
from constant.enums import ArchType
from view.components.landmarking_section_group import LandmarkArchGroup
from view.components.tool_top_button import ToolTopButton

def create_panel_landmarking(self, parent_layout):
    self.landmark_panel_widget_container = QWidget()
    self.landmark_panel_layout_container = QVBoxLayout()
    
    self.landmark_panel_widget = QWidget()
    self.landmark_panel_layout = QVBoxLayout()
    
    self.landmark_panel_widget_area = QScrollArea()
    self.landmark_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.landmark_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.landmark_panel_widget_area.setWidgetResizable(True)
    self.landmark_panel_widget_area.setWidget(self.landmark_panel_widget)
    
    self.landmark_panel_widget.setLayout(self.landmark_panel_layout)
    self.landmark_panel_layout_container.addWidget(self.landmark_panel_widget_area)
    self.landmark_panel_widget_container.setLayout(self.landmark_panel_layout_container)
    self.landmark_panel_widget_container.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    self.landmark_panel_widget_container.setFixedWidth(600)
    
    toogle_arch_btn = QWidget()
    toogle_arch_btn_layout = QHBoxLayout()
    
    self.btn_toggle_landmarking_max = ToolTopButton("Max",'icons/teeth-open-solid-top.png','icons/teeth-open-solid-colored-top.png',True)
    self.btn_toggle_landmarking_max.clicked.connect(lambda e: reset_toggle_btn_landmarking_arch(self, self.btn_toggle_landmarking_max, toogle_arch_btn))
    self.btn_toggle_landmarking_max.toggled.connect(lambda e: toggle_btn_landmarking_max(self,e))
    toogle_arch_btn_layout.addWidget(self.btn_toggle_landmarking_max)
    
    self.btn_toggle_landmarking_man = ToolTopButton("Man",'icons/teeth-open-solid-bottom.png','icons/teeth-open-solid-colored-bottom.png',True)
    self.btn_toggle_landmarking_man.clicked.connect(lambda e: reset_toggle_btn_landmarking_arch(self, self.btn_toggle_landmarking_man, toogle_arch_btn))
    self.btn_toggle_landmarking_man.toggled.connect(lambda e: toggle_btn_landmarking_man(self, e))
    toogle_arch_btn_layout.addWidget(self.btn_toggle_landmarking_man)
    
    toogle_arch_btn.setLayout(toogle_arch_btn_layout)
    self.landmark_panel_layout.addWidget(toogle_arch_btn)
    separator = QFrame()
    separator.setFrameShape(QFrame.HLine)
    self.landmark_panel_layout.addWidget(separator)
    
    self.landmark_max = LandmarkArchGroup(self,ArchType.UPPER.value)
    self.landmark_man = LandmarkArchGroup(self, ArchType.LOWER.value)

    self.landmark_panel_layout.addWidget(self.landmark_max)  
    self.landmark_panel_layout.addWidget(self.landmark_man)  
    self.landmark_panel_layout.addStretch()  
    
    parent_layout.addWidget(self.landmark_panel_widget_container, 1, 11, 20, 1)
    self.eigen_landmarking_paints=None
    self.landmark_max.hide()
    self.landmark_man.hide()
    self.landmark_panel_widget_container.hide()
    # self.landmark_panel_widget_container.setObjectName('panel_tool_right')
    
    
    

def reset_toggle_btn_landmarking_arch(self, b, toogle_arch_btn):
    btns = toogle_arch_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    
def toggle_btn_landmarking_max(self, e):
    if e:
        remove_not_arch(self, excepts_name_like='attachment')
        set_selected_arch_show_landmarking(self, ArchType.UPPER.value)
        self.landmark_max.show()
        show_landmark(self)
        draw_eigen_vec(self)
    else:
        self.landmark_max.hide()
        remove_not_arch(self, excepts_name_like='attachment')
        
        
def toggle_btn_landmarking_man(self, e):
    if e:
        remove_not_arch(self, excepts_name_like='attachment')
        set_selected_arch_show_landmarking(self, ArchType.LOWER.value)
        self.landmark_man.show()
        show_landmark(self)
        draw_eigen_vec(self)
    else:
        self.landmark_man.hide()
        remove_not_arch(self, excepts_name_like='attachment')
        

def draw_eigen_vec(self):
    remove_not_arch(self,not_archs=self.eigen_landmarking_paints, excepts_name_like='attachment')
    eigen_vec, center = draw_eigen_arch(self)
    left_right = eigen_vec[0]
    forward_backward = eigen_vec[1]
    upward_downward = eigen_vec[2]
    line_lr = Line(center-left_right, center+left_right, c="red")
    line_fb = Line(center-forward_backward, center+forward_backward, c="green")
    line_ud = Line(center-upward_downward, center+upward_downward, c="blue")
    point_lr = Point((center-left_right), c="red", r=15)
    point_fb = Point((center-forward_backward), c="green", r=15)
    point_ud = Point((center-upward_downward), c="blue", r=15)
    point_lr2 = Point((center+left_right), c="pink", r=15)
    point_fb2 = Point((center+forward_backward), c="yellow", r=15)
    point_ud2 = Point((center+upward_downward), c="violet", r=15)
    self.eigen_landmarking_paints= [line_lr, line_fb, line_ud, point_fb, point_fb2, point_lr, point_lr2, point_ud, point_ud2]
    self.model_plot.add(self.eigen_landmarking_paints)



    