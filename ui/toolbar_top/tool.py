from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets

from ui.components.toolbar_top_section import ToolbarTopSection
from ui.components.tool_top_button import ToolTopButton

def create_tool(self, parent_layout):
    self.container_tool_btn = QWidget()
    self.container_tool_btn_layout = QHBoxLayout()
    self.container_tool_btn.setLayout(self.container_tool_btn_layout)
    
    self.btn_segmentation = ToolTopButton("Segmentation",'icons/teeth-segmentation.png',True)
    self.btn_segmentation.clicked.connect(lambda e: toggle_btn_segmentation(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_segmentation)
    
    self.btn_landmark = ToolTopButton("Landmark",'icons/tooth-landmark-solid.png',True)
    self.btn_landmark.clicked.connect(lambda e: toggle_btn_landmark(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_landmark)

    self.btn_rotate = ToolTopButton('Rotate','icons/tooth-rotate.png',True)
    self.btn_rotate.clicked.connect(lambda e: toggle_btn_rotate(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_rotate)
    
    section = ToolbarTopSection("Tool",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)

def toggle_btn_segmentation(self, e):
    icon = 'icons/teeth-segmentation-colors.png' if e else 'icons/teeth-segmentation.png'
    self.btn_segmentation.setIcon(QIcon(icon))
def toggle_btn_landmark(self, e):
    icon = 'icons/tooth-landmark-solid-colors.png' if e else 'icons/tooth-landmark-solid.png'
    self.btn_landmark.setIcon(QIcon(icon))
def toggle_btn_rotate(self, e):
    icon = 'icons/tooth-rotate-colors.png' if e else 'icons/tooth-rotate.png'
    self.btn_rotate.setIcon(QIcon(icon))