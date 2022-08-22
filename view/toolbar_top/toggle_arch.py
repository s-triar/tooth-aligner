from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QToolButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt
from PyQt5 import QtWidgets

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton

from constant.enums import ArchType
from controller.toggle_model_controller import toggle_model

def create_toggle_arch_menu(self, parent_layout):
    self.container_toogle_arch_btn = QWidget()
    self.container_toogle_arch_btn_layout = QHBoxLayout()
    
    self.btn_menu_toggle_max = ToolTopButton("Max",'icons/teeth-open-solid-top.png','icons/teeth-open-solid-colored-top.png',True)
    self.btn_menu_toggle_max.setChecked(False)
    
    self.btn_menu_toggle_max.toggled.connect(lambda e: toggle_arch_model(self,e, ArchType.UPPER.value))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_max)
    
    self.btn_menu_toggle_man = ToolTopButton("Man",'icons/teeth-open-solid-bottom.png','icons/teeth-open-solid-colored-bottom.png',True)
    self.btn_menu_toggle_man.setChecked(False)
    self.btn_menu_toggle_man.toggled.connect(lambda e: toggle_arch_model(self,e, ArchType.LOWER.value))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_man)
    
    self.container_toogle_arch_btn.setLayout(self.container_toogle_arch_btn_layout)
    section = ToolbarTopSection("Toggle",self.container_toogle_arch_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)

def check_btn_toggle_arch(self, arch_type, val):
    if(arch_type == ArchType.UPPER.value):
        self.btn_menu_toggle_max.setChecked(val)
    else:
        self.btn_menu_toggle_man.setChecked(val)    

def toggle_arch_model(self, event, arch_type):
    toggle_model(self,event,arch_type)