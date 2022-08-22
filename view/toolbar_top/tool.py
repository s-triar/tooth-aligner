from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QAction,
    QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from constant.enums import PanelMode

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton

# from controller.landmarking_controller import init_var_landmarking
from controller.vedo_plotter_controller import set_plot_click_mode, reset_plot_click_mode

def create_tool(self, parent_layout):
    self.container_tool_btn = QWidget()
    self.container_tool_btn_layout = QHBoxLayout()
    self.container_tool_btn.setLayout(self.container_tool_btn_layout)
    
    self.btn_segmentation = ToolTopButton("Segmentation",'icons/teeth-segmentation.png','icons/teeth-segmentation-colors.png',True)
    # self.btn_segmentation.setObjectName('btn_toolbar_tool_segmentation')
    self.btn_segmentation.clicked.connect(lambda e: click_btn_segmentation(self,e))
    self.btn_segmentation.toggled.connect(lambda e: toggle_btn_segmentation(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_segmentation)
    
    self.btn_landmark = ToolTopButton("Landmark",'icons/tooth-landmark-solid.png','icons/tooth-landmark-solid-colors.png',True)
    # self.btn_landmark.setObjectName('btn_toolbar_tool_landmark')
    self.btn_landmark.clicked.connect(lambda e: click_btn_landmark(self,e))
    self.btn_landmark.toggled.connect(lambda e: toggle_btn_landmark(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_landmark)

    self.btn_rotate = ToolTopButton('Rotate','icons/tooth-rotate.png','icons/tooth-rotate-colors.png',True)
    # self.btn_rotate.setObjectName('btn_toolbar_tool_rotate')
    self.btn_rotate.clicked.connect(lambda e: click_btn_rotate(self,e))
    self.btn_rotate.toggled.connect(lambda e: toggle_btn_rotate(self,e))
    
    self.container_tool_btn_layout.addWidget(self.btn_rotate)
    
    section = ToolbarTopSection("Tool",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)
    
    
    
def reset_toggle_tool(self, b):
    btns = self.container_tool_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    # analysis
    btns = self.container_toogle_arch_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    # b.setChecked(True)

def click_btn_segmentation(self, e):
    reset_toggle_tool(self, self.btn_segmentation)

def toggle_btn_segmentation(self, e):
    if e:
        self.panel_segmentation_widget.show()
        set_plot_click_mode(self, PanelMode.SEGMENTATION.value)
    else:
        self.panel_segmentation_widget.hide()

def click_btn_landmark(self, e):
    reset_toggle_tool(self, self.btn_landmark)
    
    
def toggle_btn_landmark(self, e):
    if e:
        self.landmark_max.hide()
        self.landmark_man.hide()
        self.landmark_panel_widget_container.show()
        set_plot_click_mode(self, PanelMode.LANDMARK.value)
    else:
        self.landmark_panel_widget_container.hide()
        # reset_plot_click_mode(self, PanelMode.LANDMARK.value)
    
def click_btn_rotate(self, e):
    reset_toggle_tool(self,self.btn_rotate)

    
def toggle_btn_rotate(self, e):
    if e:
        self.panel_rotation_widget.show()
        set_plot_click_mode(self, PanelMode.ROTATION.value)
    else:
        self.panel_rotation_widget.hide()