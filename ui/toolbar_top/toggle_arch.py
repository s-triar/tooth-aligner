from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QToolButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt
from PyQt5 import QtWidgets

from ui.components.toolbar_top_section import ToolbarTopSection
from ui.components.tool_top_button import ToolTopButton

def create_toggle_arch_menu(self, parent_layout):
    self.container_toogle_arch_btn = QWidget()
    self.container_toogle_arch_btn_layout = QHBoxLayout()
    
    self.btn_menu_toggle_max = ToolTopButton("Max",'icons/teeth-open-solid-top.png',True)
    self.btn_menu_toggle_max.clicked.connect(lambda e: toggle_btn_arch_max(self,e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_max)
    
    self.btn_menu_toggle_man = ToolTopButton("Man",'icons/teeth-open-solid-bottom.png',True)
    self.btn_menu_toggle_man.clicked.connect(lambda e: toggle_btn_arch_man(self, e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_man)
    
    self.container_toogle_arch_btn.setLayout(self.container_toogle_arch_btn_layout)
    section = ToolbarTopSection("Toggle",self.container_toogle_arch_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)

def toggle_btn_arch_max(self, e):
    icon = 'icons/teeth-open-solid-colored-top.png' if e else 'icons/teeth-open-solid-top.png'
    self.btn_menu_toggle_max.setIcon(QIcon(icon))
def toggle_btn_arch_man(self, e):
    icon = 'icons/teeth-open-solid-colored-bottom.png' if e else 'icons/teeth-open-solid-bottom.png'
    self.btn_menu_toggle_man.setIcon(QIcon(icon))