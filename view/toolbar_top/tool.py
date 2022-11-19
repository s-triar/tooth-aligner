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
from controller.bite_contact_controller import reset_bite_contact
from controller.segmentation_controller import set_selected_arch, set_selected_label

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton

# from controller.landmarking_controller import init_var_landmarking
from controller.vedo_plotter_controller import remove_not_arch, set_plot_click_mode, reset_plot_click_mode
from view.toolbar_right.panel_bite_contact import draw_bite_contact
from view.toolbar_right.panel_grid import draw_grid_lines, draw_grid_lines_overlay
from view.toolbar_top.reset_toggle_btn import reset_toggle_tooltop_btn

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

    self.btn_rotate = ToolTopButton('Movement','icons/tooth-rotate.png','icons/tooth-rotate-colors.png',True)
    # self.btn_rotate.setObjectName('btn_toolbar_tool_rotate')
    self.btn_rotate.clicked.connect(lambda e: click_btn_rotate(self,e))
    self.btn_rotate.toggled.connect(lambda e: toggle_btn_rotate(self,e))
    
    self.container_tool_btn_layout.addWidget(self.btn_rotate)
    
    self.btn_grid = ToolTopButton("Grid",'icons/table-cells-solid.png','icons/table-cells-solid-colored.png',True)
    # self.btn_grid.setObjectName('btn_toolbar_tool_segmentation')
    self.btn_grid.clicked.connect(lambda e: click_btn_grid(self,e))
    self.btn_grid.toggled.connect(lambda e: toggle_btn_grid(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_grid)
    
    self.btn_bite_contact = ToolTopButton("Bite",'icons/table-cells-solid.png','icons/table-cells-solid-colored.png',True)
    # self.btn_bite_contact.setObjectName('btn_toolbar_tool_segmentation')
    self.btn_bite_contact.clicked.connect(lambda e: click_btn_bite_contact(self,e))
    self.btn_bite_contact.toggled.connect(lambda e: toggle_btn_bite_contact(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_bite_contact)
    
    section = ToolbarTopSection("Tool",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)
    
    
    
# def reset_toggle_tooltop_btn(self, b):
#     btns = self.container_tool_btn.findChildren(ToolTopButton)
#     for btn in btns:
#         if btn.isChecked() and btn != b:
#             btn.setChecked(False)
#     # analysis
#     btns = self.container_toogle_arch_btn.findChildren(ToolTopButton)
#     for btn in btns:
#         if btn.isChecked() and btn != b:
#             btn.setChecked(False)
#     # b.setChecked(True)
#     btns = self.container_utility_btn.findChildren(ToolTopButton)
#     for btn in btns:
#         if(btn.isCheckable() and btn.isChecked() and btn != b):
#             btn.setChecked(False)

def click_btn_segmentation(self, e):
    reset_toggle_tooltop_btn(self, self.btn_segmentation)

def toggle_btn_segmentation(self, e):
    if e:
        self.panel_segmentation_widget.show()
        set_plot_click_mode(self, PanelMode.SEGMENTATION.value)
        id_us = self.combo_box_arch_segmentation.itemData(self.combo_box_arch_segmentation.currentIndex()) # .toPyObject()
        # print('VAL arch',id_us, i)
        set_selected_arch(self, id_us)
        id_us = self.combo_box_label_segmentation.itemData(self.combo_box_label_segmentation.currentIndex()) # .toPyObject()
        # print('VAL tooth',id_us,i)
        set_selected_label(self, id_us)
    else:
        self.panel_segmentation_widget.hide()

def click_btn_landmark(self, e):
    reset_toggle_tooltop_btn(self, self.btn_landmark)
    
    
def toggle_btn_landmark(self, e):
    if e:
        remove_not_arch(self, excepts_name_like='attachment')
        self.landmark_max.hide()
        self.landmark_man.hide()
        self.landmark_panel_widget_container.show()
        set_plot_click_mode(self, PanelMode.LANDMARK.value)
    else:
        self.landmark_panel_widget_container.hide()
        remove_not_arch(self, excepts_name_like='attachment')
        # reset_plot_click_mode(self, PanelMode.LANDMARK.value)
    
def click_btn_rotate(self, e):
    reset_toggle_tooltop_btn(self,self.btn_rotate)

    
def toggle_btn_rotate(self, e):
    if e:
        self.panel_rotation_widget.show()
        set_plot_click_mode(self, PanelMode.ROTATION.value)
    else:
        self.panel_rotation_widget.hide()
        
def click_btn_grid(self, e):
    reset_toggle_tooltop_btn(self,self.btn_grid)

    
def toggle_btn_grid(self, e):
    if e:
        self.grid_panel_widget_container.show()
        draw_grid_lines_overlay(self)
        set_plot_click_mode(self, PanelMode.GRID.value)
    else:
        self.grid_panel_widget_container.hide()
        remove_not_arch(self, excepts_name_like='attachment')
        
def click_btn_bite_contact(self, e):
    reset_toggle_tooltop_btn(self,self.btn_bite_contact)

    
def toggle_btn_bite_contact(self, e):
    if e:
        remove_not_arch(self, excepts_name_like='attachment')
        draw_bite_contact(self)
        # self.bite_contact_panel_widget_container.show()
        # set_plot_click_mode(self, PanelMode.GRID.value)
    else:
        reset_bite_contact(self)
        # self.bite_contact_panel_widget_container.hide()
        remove_not_arch(self, excepts_name_like='attachment')
        