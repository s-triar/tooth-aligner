
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


def create_panel_step_aligner(self, parent_layout):
    self.panel_step_aligner_widget = QWidget()
    self.panel_step_aligner_layout = QHBoxLayout()
    self.panel_step_aligner_widget.setLayout(self.panel_step_aligner_layout)
    
    slider_group = QWidget()
    slider_group_layout = QVBoxLayout()
    slider_group.setLayout(slider_group_layout)
    self.label_slider_step_aligner = QLabel('Aligner 0/0')
    self.label_slider_step_aligner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.label_slider_step_aligner.setAlignment(Qt.AlignCenter)
    self.slider_step_aligner = QSlider(Qt.Horizontal)
    self.slider_step_aligner.setFocusPolicy(Qt.StrongFocus)
    self.slider_step_aligner.setTickPosition(QSlider.TicksBothSides)
    self.slider_step_aligner.setTickInterval(1)
    self.slider_step_aligner.setSingleStep(1)
    slider_group_layout.addWidget(self.label_slider_step_aligner)
    slider_group_layout.addWidget(self.slider_step_aligner)
    
    self.btn_addmin_step_aligner = RotationButtonGroup('Delete/Add')
    
    self.panel_step_aligner_layout.addWidget(slider_group)
    self.panel_step_aligner_layout.addWidget(self.btn_addmin_step_aligner)
    
    self.panel_step_aligner_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
    parent_layout.addWidget(self.panel_step_aligner_widget,20, 0, 1, 11)
    
    