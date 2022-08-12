from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QToolButton
)

from ui.components.toolbar_top_section import ToolbarTopSection
from ui.components.tool_top_button import ToolTopButton
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon
from PyQt5.QtCore import Qt, QSize

def create_import_menu(self, parent_layout):
    self.container_import_btn = QWidget()
    self.container_import_btn_layout = QHBoxLayout()
    
    self.btn_import_max = ToolTopButton("Max","icons/file-import-solid.png", False)
    self.btn_import_man = ToolTopButton("Man","icons/file-import-solid.png", False)
    self.btn_import_reset = ToolTopButton("Reset","icons/file-circle-xmark-solid.png",False)
    self.container_import_btn_layout.addWidget(self.btn_import_max)
    self.container_import_btn_layout.addWidget(self.btn_import_man)
    self.container_import_btn_layout.addWidget(self.btn_import_reset)
    self.container_import_btn.setLayout(self.container_import_btn_layout)
    section = ToolbarTopSection('Import', self.container_import_btn)
    # parent_layout.addWidget(section, 0, 0)
    parent_layout.addWidget(section)
    

# def create_import_menu_old2(self, parent_layout):
#     self.container_import_menu = QWidget()
#     self.container_import_menu.setStyleSheet("background-color:rgba(250,240,215,1)")
#     self.container_import_menu_layout = QVBoxLayout()
    
#     self.container_import_btn = QWidget()
    
#     self.container_import_btn_layout = QVBoxLayout()
    
#     self.container_import_max_man_btn = QWidget()
#     self.container_import_max_man_btn_layout = QHBoxLayout()
#     self.btn_import_max = QPushButton("Max")
#     self.btn_import_man = QPushButton("Man")
#     self.container_import_max_man_btn_layout.addWidget(self.btn_import_max)
#     self.container_import_max_man_btn_layout.addWidget(self.btn_import_man)
#     self.container_import_max_man_btn.setLayout(self.container_import_max_man_btn_layout)
    
#     self.btn_import_reset = QPushButton("Reset")
    
#     # self.container_import_btn_layout.addWidget(self.btn_import_max)
#     # self.container_import_btn_layout.addWidget(self.btn_import_man)
#     self.container_import_btn_layout.addWidget(self.container_import_max_man_btn)
#     self.container_import_btn_layout.addWidget(self.btn_import_reset)
    
#     self.container_import_btn.setLayout(self.container_import_btn_layout)
#     self.container_import_menu_layout.addWidget(self.container_import_btn)
    
#     f = QFont()
#     f.setBold(True)
#     title = QLabel('Import')
#     title.setAlignment(Qt.AlignCenter)
#     title.setFont(f)
#     title.setStyleSheet("color:rgba(29, 155, 240,1)")
    
#     self.container_import_menu_layout.addWidget(title)
#     self.container_import_menu.setLayout(self.container_import_menu_layout)
#     # self.group_import_btn.setLayout(self.layout_import_btn)
#     parent_layout.addWidget(self.container_import_menu, 0, 0)
    
