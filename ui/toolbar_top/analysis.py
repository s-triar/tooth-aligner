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

def create_analysis_menu(self, parent_layout):
    self.container_toogle_arch_btn = QWidget()
    self.container_toogle_arch_btn_layout = QHBoxLayout()
    
    self.btn_menu_toggle_bolton = ToolTopButton("Bolton",'icons/teeth-open-solid-top.png',True)
    self.btn_menu_toggle_bolton.clicked.connect(lambda e: toggle_btn_menu_bolton(self,e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_bolton)
    
    self.btn_menu_toggle_pont = ToolTopButton("Pont",'icons/teeth-open-solid-top.png',True)
    self.btn_menu_toggle_pont.clicked.connect(lambda e: toggle_btn_menu_pont(self,e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_pont)
    
    self.btn_menu_toggle_korkhaus = ToolTopButton("Korkhaus",'icons/teeth-open-solid-top.png',True)
    self.btn_menu_toggle_korkhaus.clicked.connect(lambda e: toggle_btn_menu_korkhaus(self,e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_korkhaus)
    
    self.container_toogle_arch_btn.setLayout(self.container_toogle_arch_btn_layout)
    section = ToolbarTopSection("Toggle",self.container_toogle_arch_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)

def toggle_btn_menu_bolton(self, e):
    icon = 'icons/teeth-open-solid-colored-top.png' if e else 'icons/teeth-open-solid-top.png'
    self.btn_menu_toggle_bolton.setIcon(QIcon(icon))
    
def toggle_btn_menu_pont(self, e):
    icon = 'icons/teeth-open-solid-colored-top.png' if e else 'icons/teeth-open-solid-top.png'
    self.btn_menu_toggle_pont.setIcon(QIcon(icon))
    
def toggle_btn_menu_korkhaus(self, e):
    icon = 'icons/teeth-open-solid-colored-top.png' if e else 'icons/teeth-open-solid-top.png'
    self.btn_menu_toggle_korkhaus.setIcon(QIcon(icon))