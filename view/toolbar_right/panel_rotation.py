
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
from controller.rotation_controller import pitch, roll, yaw

from view.components.rotation_btn_group import RotationButtonGroup

def create_panel_rotation(self, parent_layout):
    self.panel_rotation_widget = QWidget()
    self.panel_rotation_layout = QVBoxLayout()
    self.panel_rotation_widget.setLayout(self.panel_rotation_layout)
    
    slider_widget=QWidget()
    slider_widget_layout = QVBoxLayout()
    slider_widget.setLayout(slider_widget_layout)
    label_slider = QLabel('Pivot')
    self.slider_pivot_root = QSlider(Qt.Horizontal)
    self.slider_pivot_root.setFocusPolicy(Qt.StrongFocus)
    self.slider_pivot_root.setTickPosition(QSlider.TicksBothSides)
    self.slider_pivot_root.setTickInterval(1)
    self.slider_pivot_root.setSingleStep(0.1)
    slider_widget_layout.addWidget(label_slider)
    slider_widget_layout.addWidget(self.slider_pivot_root)
    
    
    
    self.btn_pitch = RotationButtonGroup("Pitch")
    self.btn_roll = RotationButtonGroup("Roll")
    self.btn_yaw = RotationButtonGroup("Yaw")
    
    self.btn_pitch.btn_increase.clicked.connect(lambda e: do_pitch(self, '+'))
    self.btn_pitch.btn_decrease.clicked.connect(lambda e: do_pitch(self, '-'))
    
    self.btn_roll.btn_increase.clicked.connect(lambda e: do_roll(self, '+'))
    self.btn_roll.btn_decrease.clicked.connect(lambda e: do_roll(self, '-'))
    
    self.btn_yaw.btn_increase.clicked.connect(lambda e: do_yaw(self, '+'))
    self.btn_yaw.btn_decrease.clicked.connect(lambda e: do_yaw(self, '-'))
    
    self.panel_rotation_layout.addWidget(slider_widget)
    self.panel_rotation_layout.addWidget(self.btn_pitch)
    self.panel_rotation_layout.addWidget(self.btn_roll)
    self.panel_rotation_layout.addWidget(self.btn_yaw)
    self.panel_rotation_layout.addStretch()
    self.panel_rotation_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    parent_layout.addWidget(self.panel_rotation_widget,1, 11, 20, 1)
    self.panel_rotation_widget.hide()
    # self.panel_rotation_widget.setObjectName('panel_tool_right')
    

def do_pitch(self, rotate_type):
    pitch(self, rotate_type, self.slider_pivot_root.value())
    
def do_roll(self, rotate_type):
    roll(self, rotate_type, self.slider_pivot_root.value())

def do_yaw(self, rotate_type):
    yaw(self, rotate_type, self.slider_pivot_root.value())
    
    
    

    
    
    