from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QScrollArea
)
from PyQt5 import QtWidgets
from view.toolbar_top.import_arch import create_import_menu
from view.toolbar_top.optimization import create_optimization_menu
from view.toolbar_top.save_load_project import create_save_load_project_menu
from view.toolbar_top.toggle_arch import create_toggle_arch_menu
from view.toolbar_top.tool import create_tool
from view.toolbar_top.analysis import create_analysis_menu
from view.toolbar_top.utility import create_utility
from PyQt5.QtCore import Qt, QSize


def create_top_toolbar(self, parent_layout):
    self.menubar_widget_container = QWidget()
    self.menubar_layout_container = QHBoxLayout()
    
    self.menubar_widget = QWidget()
    self.menubar_layout = QHBoxLayout()
    
    self.menubar_widget_area = QScrollArea()
    # self.menubar_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.menubar_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.menubar_widget_area.setWidgetResizable(True)
    self.menubar_widget_area.setWidget(self.menubar_widget)
    
    self.menubar_widget.setLayout(self.menubar_layout)
    self.menubar_layout_container.addWidget(self.menubar_widget_area)
    self.menubar_widget_container.setLayout(self.menubar_layout_container)
    self.menubar_widget_container.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
    # self.landmark_panel_widget_container.setFixedWidth(600)
    
    create_import_menu(self,self.menubar_layout)
    # self.menubar_layout.addWidget(self.group_import_btn, 0, 0)
    
    create_toggle_arch_menu(self,self.menubar_layout)
    # self.menubar_layout.addWidget(self.group_toogle_arch_btn, 0, 1)
    create_tool(self, self.menubar_layout)
    create_analysis_menu(self, self.menubar_layout)
    create_utility(self, self.menubar_layout)
    create_optimization_menu(self, self.menubar_layout)
    create_save_load_project_menu(self, self.menubar_layout)
    # self.menubar_layout.addWidget(self.group_analysis_btn, 0, 2)
    
    self.menubar_widget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)

    parent_layout.addWidget(self.menubar_widget_container, 0, 0, 1, 12)
