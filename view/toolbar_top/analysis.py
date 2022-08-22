from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QToolButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize,Qt
from PyQt5 import QtWidgets
from controller.vedo_plotter_controller import remove_not_arch

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton
from view.toolbar_right.panel_bolton import create_total_tooth_material_widget
from view.toolbar_right.panel_korkhaus import create_pane_korkhaus, draw_korkhaus_lines
from view.toolbar_right.panel_pont import create_pane_pont, draw_pont_lines


def create_analysis_menu(self, parent_layout):
    self.container_toogle_arch_btn = QWidget()
    self.container_toogle_arch_btn_layout = QHBoxLayout()
    
    self.btn_menu_toggle_bolton = ToolTopButton("Bolton",'icons/bolton.png','icons/bolton-colors.png',True)
    self.btn_menu_toggle_bolton.toggled.connect(lambda e: toggle_btn_menu_bolton(self,e))
    self.btn_menu_toggle_bolton.clicked.connect(lambda e: click_btn_menu_bolton(self,e))
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_bolton)
    
    self.btn_menu_toggle_pont = ToolTopButton("Pont",'icons/pont.png','icons/pont-colors.png',True)
    self.btn_menu_toggle_pont.toggled.connect(lambda e: toggle_btn_menu_pont(self,e))
    self.btn_menu_toggle_pont.clicked.connect(lambda e: click_btn_menu_pont(self,e))
    
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_pont)
    
    self.btn_menu_toggle_korkhaus = ToolTopButton("Korkhaus",'icons/korkhaus_new.png','icons/korkhaus_new-colors.png',True)
    self.btn_menu_toggle_korkhaus.toggled.connect(lambda e: toggle_btn_menu_korkhaus(self,e))
    self.btn_menu_toggle_korkhaus.clicked.connect(lambda e: click_btn_menu_korkhaus(self,e))
    
    self.container_toogle_arch_btn_layout.addWidget(self.btn_menu_toggle_korkhaus)
    
    self.container_toogle_arch_btn.setLayout(self.container_toogle_arch_btn_layout)
    section = ToolbarTopSection("Analysis",self.container_toogle_arch_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)
    
def reset_toggle_analysis(self, b):
    btns = self.container_toogle_arch_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
            
    # tool
    btns = self.container_tool_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    

def toggle_btn_menu_bolton(self, e):
    if e:
        self.bolton_panel_widget_container.show()
        create_total_tooth_material_widget(self)
    else:
        self.bolton_panel_widget_container.hide()

def click_btn_menu_bolton(self, e):
    reset_toggle_analysis(self, self.btn_menu_toggle_bolton)
    
    
def toggle_btn_menu_pont(self, e):
    if e:
        self.pont_panel_widget_container.show()
        create_pane_pont(self)
        draw_pont_lines(self)
    else:
        self.pont_panel_widget_container.hide()
        remove_not_arch(self)


def click_btn_menu_pont(self, e):
    reset_toggle_analysis(self, self.btn_menu_toggle_pont)
    
def toggle_btn_menu_korkhaus(self, e):
    if e:
        self.korkhaus_panel_widget_container.show()
        create_pane_korkhaus(self)
        draw_korkhaus_lines(self)
    else:
        self.korkhaus_panel_widget_container.hide()
        remove_not_arch(self)


def click_btn_menu_korkhaus(self, e):
    reset_toggle_analysis(self, self.btn_menu_toggle_korkhaus)
    



