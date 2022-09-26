
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
    QFormLayout,
    QFrame, 
    QScrollArea,
    QSizePolicy,
    QSlider
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from controller.attachment_controller import prep_delete_attachment, prep_new_attachment, prep_reset_attachment_state


def create_panel_attatchment(self, parent_layout):
    self.panel_attachment_widget = QWidget()
    self.panel_attachment_layout = QVBoxLayout()
    self.panel_attachment_widget.setLayout(self.panel_attachment_layout)
    
    
    self.btn_attachment_rectangular_3 = QPushButton("Rectangular 3 mm")
    self.btn_attachment_rectangular_3.setIcon(QIcon('icons/square-solid.png'))
    self.btn_attachment_rectangular_3.setCheckable(True)
    self.btn_attachment_rectangular_3.setChecked(False)
    
    self.btn_attachment_rectangular_3.clicked.connect(lambda e: on_btn_attachment_rectangular_3_clicked(self, e))
    self.btn_attachment_rectangular_3.toggled.connect(lambda e: on_btn_attachment_rectangular_3_toggled(self, e))
    self.panel_attachment_layout.addWidget(self.btn_attachment_rectangular_3)
    
    self.btn_attachment_rectangular_4 = QPushButton("Rectangular 4 mm")
    self.btn_attachment_rectangular_4.setIcon(QIcon('icons/square-solid.png'))
    self.btn_attachment_rectangular_4.setCheckable(True)
    self.btn_attachment_rectangular_4.setChecked(False)
    
    self.btn_attachment_rectangular_4.clicked.connect(lambda e: on_btn_attachment_rectangular_4_clicked(self, e))
    self.btn_attachment_rectangular_4.toggled.connect(lambda e: on_btn_attachment_rectangular_4_toggled(self, e))
    self.panel_attachment_layout.addWidget(self.btn_attachment_rectangular_4)
    
    self.btn_attachment_rectangular_5 = QPushButton("Rectangular 5 mm")
    self.btn_attachment_rectangular_5.setIcon(QIcon('icons/square-solid.png'))
    self.btn_attachment_rectangular_5.setCheckable(True)
    self.btn_attachment_rectangular_5.setChecked(False)
    
    self.btn_attachment_rectangular_5.clicked.connect(lambda e: on_btn_attachment_rectangular_5_clicked(self, e))
    self.btn_attachment_rectangular_5.toggled.connect(lambda e: on_btn_attachment_rectangular_5_toggled(self, e))
    self.panel_attachment_layout.addWidget(self.btn_attachment_rectangular_5)
    
    
    self.btn_delete_attachment = QPushButton("Delete")
    self.btn_delete_attachment.setIcon(QIcon('icons/trash-solid.png'))
    self.btn_delete_attachment.setCheckable(True)
    self.btn_delete_attachment.setChecked(False)
    
    self.btn_delete_attachment.clicked.connect(lambda e: on_btn_delete_attachment_clicked(self, e))
    self.btn_delete_attachment.toggled.connect(lambda e: on_btn_delete_attachment_toggled(self, e))
    
    self.panel_attachment_layout.addWidget(self.btn_delete_attachment)
    
    self.panel_attachment_layout.addStretch()
    self.panel_attachment_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    parent_layout.addWidget(self.panel_attachment_widget,1, 11, 20, 1)
    self.panel_attachment_widget.hide()
    # self.panel_attachment_widget.setObjectName('panel_tool_right')
    
def reset_toggle_btn_attachment(self, b):
    btns = self.panel_attachment_widget.findChildren(QPushButton)
    for btn in btns:
        if(btn.isCheckable() and btn.isChecked() and btn != b):
            btn.setChecked(False)

def on_btn_delete_attachment_clicked(self, event):
    reset_toggle_btn_attachment(self, self.btn_delete_attachment)

def on_btn_delete_attachment_toggled(self, event):
    if event:
        self.btn_delete_attachment.setIcon(QIcon('icons/trash-solid-colored.png'))
        prep_delete_attachment(self)
    else:
        self.btn_delete_attachment.setIcon(QIcon('icons/trash-solid.png'))
        prep_reset_attachment_state(self)

def on_btn_attachment_rectangular_3_clicked(self, event):
    reset_toggle_btn_attachment(self, self.btn_attachment_rectangular_3)

def on_btn_attachment_rectangular_3_toggled(self, event):
    if event:
        self.btn_attachment_rectangular_3.setIcon(QIcon('icons/square-solid-colored.png'))
        prep_new_attachment(self,3)
    else:
        self.btn_attachment_rectangular_3.setIcon(QIcon('icons/square-solid.png'))
        prep_reset_attachment_state(self)
        
def on_btn_attachment_rectangular_4_clicked(self, event):
    reset_toggle_btn_attachment(self, self.btn_attachment_rectangular_4)

def on_btn_attachment_rectangular_4_toggled(self, event):
    if event:
        self.btn_attachment_rectangular_4.setIcon(QIcon('icons/square-solid-colored.png'))
        prep_new_attachment(self,4)
    else:
        self.btn_attachment_rectangular_4.setIcon(QIcon('icons/square-solid.png'))
        prep_reset_attachment_state(self)
        
def on_btn_attachment_rectangular_5_clicked(self, event):
    reset_toggle_btn_attachment(self, self.btn_attachment_rectangular_5)

def on_btn_attachment_rectangular_5_toggled(self, event):
    if event:
        self.btn_attachment_rectangular_5.setIcon(QIcon('icons/square-solid-colored.png'))
        prep_new_attachment(self,5)
    else:
        self.btn_attachment_rectangular_5.setIcon(QIcon('icons/square-solid.png'))
        prep_reset_attachment_state(self)

    
    
    