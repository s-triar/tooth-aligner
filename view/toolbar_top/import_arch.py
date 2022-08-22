from PyQt5.QtWidgets import (
    QHBoxLayout,
    QWidget,
    QToolButton,
    QFileDialog
    
)
from utility.arch import Arch

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton
from view.toolbar_top.toggle_arch import check_btn_toggle_arch
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon
from PyQt5.QtCore import Qt, QSize
from controller.import_data_controller import check_archs_loaded, load_model, reset_model
from constant.enums import ArchType

def create_import_menu(self, parent_layout):
    self.container_import_btn = QWidget()
    self.container_import_btn_layout = QHBoxLayout()
    
    self.btn_import_max = ToolTopButton("Max","icons/file-import-solid.png",None, False)
    self.btn_import_man = ToolTopButton("Man","icons/file-import-solid.png",None, False)
    self.btn_import_reset = ToolTopButton("Reset","icons/file-circle-xmark-solid.png",None,False)
    self.btn_import_reset.setDisabled(True)
    self.btn_import_max.clicked.connect(lambda e: import_arch(self, ArchType.UPPER.value, self.btn_import_max))
    self.btn_import_man.clicked.connect(lambda e: import_arch(self, ArchType.LOWER.value, self.btn_import_man))
    self.btn_import_reset.clicked.connect(lambda e: reset_arch(self))
    self.container_import_btn_layout.addWidget(self.btn_import_max)
    self.container_import_btn_layout.addWidget(self.btn_import_man)
    self.container_import_btn_layout.addWidget(self.btn_import_reset)
    self.container_import_btn.setLayout(self.container_import_btn_layout)
    section = ToolbarTopSection('Import', self.container_import_btn)
    # parent_layout.addWidget(section, 0, 0)
    parent_layout.addWidget(section)
    
def check_loaded(self):
    if(check_archs_loaded(self)):
        self.btn_import_reset.setEnabled(True)
    else:
        self.btn_import_reset.setDisabled(True)


def import_arch(self, arch_type, btn):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilters(["*.vtp *.stl"])
    filenames = []
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        load_model(self, filenames[0], arch_type)
        btn.setDisabled(True)
        check_btn_toggle_arch(self, arch_type, True)
    check_loaded(self)
    
def reset_arch(self):
    reset_model(self)
    check_btn_toggle_arch(self, ArchType.LOWER.value, False)
    self.btn_import_man.setEnabled(True)
    check_btn_toggle_arch(self, ArchType.UPPER.value, False)
    self.btn_import_max.setEnabled(True)
    check_loaded(self)
    

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
    
