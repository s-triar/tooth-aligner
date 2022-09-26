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
from controller.attachment_controller import reset_plot_interaction

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton

# from controller.landmarking_controller import init_var_landmarking
from controller.vedo_plotter_controller import remove_not_arch, set_plot_click_mode, reset_plot_click_mode
from view.toolbar_top.reset_toggle_btn import reset_toggle_tooltop_btn

def create_utility(self, parent_layout):
    self.container_utility_btn = QWidget()
    self.container_utility_btn_layout = QHBoxLayout()
    self.container_utility_btn.setLayout(self.container_utility_btn_layout)
    
    self.btn_attachment = ToolTopButton("Attachment",'icons/circle-stop-solid.png','icons/circle-stop-solid-colored.jpg',True)
    self.btn_segmentation.setObjectName('btn_utilitybar_utility_segmentation')
    self.btn_attachment.clicked.connect(lambda e: click_btn_attachment(self,e))
    self.btn_attachment.toggled.connect(lambda e: toggle_btn_attachment(self,e))
    self.container_utility_btn_layout.addWidget(self.btn_attachment)
    
    self.btn_collision = ToolTopButton("Collision",'icons/teeth-solid.png','icons/teeth-solid-colored.jpg',True)
    self.btn_segmentation.setObjectName('btn_utilitybar_utility_segmentation')
    self.btn_collision.clicked.connect(lambda e: click_btn_collision(self,e))
    self.btn_collision.toggled.connect(lambda e: toggle_btn_collision(self,e))
    self.container_utility_btn_layout.addWidget(self.btn_collision)
    
    self.btn_save_step = ToolTopButton("Save",'icons/floppy-disk-solid.png','icons/floppy-disk-solid-colored.jpg',False)
    # self.btn_segmentation.setObjectName('btn_utilitybar_utility_segmentation')
    # self.btn_save_step.clicked.connect(lambda e: click_btn_save_step(self,e))
    # self.btn_save_step.toggled.connect(lambda e: toggle_btn_save_step(self,e))
    self.container_utility_btn_layout.addWidget(self.btn_save_step)
    
    
    section = ToolbarTopSection("Tool",self.container_utility_btn)
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

def click_btn_attachment(self, e):
    reset_toggle_tooltop_btn(self, self.btn_attachment)

def toggle_btn_attachment(self, e):
    if e:
        self.panel_attachment_widget.show()
        remove_not_arch(self, excepts_name_like='attachment')
        set_plot_click_mode(self, PanelMode.ATTATCHMENT.value)
    else:
        reset_plot_interaction(self)
        self.panel_attachment_widget.hide()

def click_btn_collision(self, e):
    reset_toggle_tooltop_btn(self, self.btn_collision)

def toggle_btn_collision(self, e):
    if e:
        # self.panel_collision_widget.show()
        remove_not_arch(self)
        set_plot_click_mode(self, PanelMode.COLLISION.value)
    else:
        reset_plot_interaction(self)
        # self.panel_collision_widget.hide()
