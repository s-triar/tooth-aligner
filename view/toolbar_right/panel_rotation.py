
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
from controller.rotation_controller import change_pivot_point, do_moving, pitch, roll, yaw

from view.components.rotation_btn_group import RotationButtonGroup

def create_panel_rotation(self, parent_layout):
    self.panel_rotation_widget = QWidget()
    self.panel_rotation_layout = QVBoxLayout()
    self.panel_rotation_widget.setLayout(self.panel_rotation_layout)
    
    slider_widget=QWidget()
    slider_widget_layout = QVBoxLayout()
    slider_widget.setLayout(slider_widget_layout)
    
    slider_widget_layout.addWidget(QLabel('Rotasi'))
    label_slider = QLabel('Pivot')
    
    slider_widget_label_widget = QWidget()
    slider_widget_label_widget_layout = QHBoxLayout()
    slider_widget_label_widget.setLayout(slider_widget_label_widget_layout)
    self.slider_pivot_value = QLabel('0/0')
    slider_widget_label_widget_layout.addWidget(label_slider)
    slider_widget_label_widget_layout.addWidget(self.slider_pivot_value)
    
    self.slider_pivot_root = QSlider(Qt.Horizontal)
    self.slider_pivot_root.setFocusPolicy(Qt.StrongFocus)
    self.slider_pivot_root.setTickPosition(QSlider.TicksBothSides)
    self.slider_pivot_root.setTickInterval(1)
    self.slider_pivot_root.setSingleStep(0.1)
    slider_widget_layout.addWidget(slider_widget_label_widget)
    slider_widget_layout.addWidget(self.slider_pivot_root)
    self.slider_pivot_root.valueChanged.connect(lambda e: on_slider_pivot_change(self, e))
    
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
    
    slider_widget_layout.addWidget(QLabel('Movement'))
    
    self.btn_movement_x = RotationButtonGroup("Sumbu X")
    self.btn_movement_y = RotationButtonGroup("Sumbu Y")
    self.btn_movement_z = RotationButtonGroup("Sumbu Z")
    
    self.btn_movement_x.btn_increase.clicked.connect(lambda e: do_move(self, '+', 'x'))
    self.btn_movement_x.btn_decrease.clicked.connect(lambda e: do_move(self, '-', 'x'))
    self.btn_movement_y.btn_increase.clicked.connect(lambda e: do_move(self, '+', 'y'))
    self.btn_movement_y.btn_decrease.clicked.connect(lambda e: do_move(self, '-', 'y'))
    self.btn_movement_z.btn_increase.clicked.connect(lambda e: do_move(self, '+', 'z'))
    self.btn_movement_z.btn_decrease.clicked.connect(lambda e: do_move(self, '-', 'z'))
    
    self.panel_rotation_layout.addWidget(self.btn_movement_x)
    self.panel_rotation_layout.addWidget(self.btn_movement_y)
    self.panel_rotation_layout.addWidget(self.btn_movement_z)
    
    self.panel_rotation_layout.addStretch()
    self.panel_rotation_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    parent_layout.addWidget(self.panel_rotation_widget,1, 11, 20, 1)
    self.panel_rotation_widget.hide()
    # self.panel_rotation_widget.setObjectName('panel_tool_right')
    

def do_pitch(self, rotate_type):
    pitch(self, rotate_type)
    
def do_roll(self, rotate_type):
    roll(self, rotate_type)

def do_yaw(self, rotate_type):
    yaw(self, rotate_type)

def on_slider_pivot_change(self, e):
    te='{0}/{1}'.format(str(self.slider_pivot_root.value()), str(self.slider_pivot_root.maximum()))
    self.slider_pivot_value.setText(te)
    change_pivot_point(self, self.slider_pivot_root.value())

def do_move(self, move_type, move_direction):
    val=[0,0,0]
    if(move_type=='+' and move_direction=='x'):
        val=[0.1,0,0]
    elif(move_type=='+' and move_direction=='y'):
        val=[0,0.1,0]
    elif(move_type=='+' and move_direction=='z'):
        val=[0,0,0.1]
    if(move_type=='-' and move_direction=='x'):
        val=[-0.1,0,0]
    elif(move_type=='-' and move_direction=='y'):
        val=[0,-0.1,0]
    elif(move_type=='-' and move_direction=='z'):
        val=[0,0,-0.1]
    do_moving(self, val)

    
    
    