
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
from controller.step_controller import add_transform_arch, apply_transform_arch, change_step, remove_transform_arch
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
    self.slider_step_aligner.setMaximum(0)
    
    self.slider_step_aligner.valueChanged.connect(lambda e: on_value_change(self, e))
    
    slider_group_layout.addWidget(self.label_slider_step_aligner)
    slider_group_layout.addWidget(self.slider_step_aligner)
    
    self.btn_addmin_step_aligner = RotationButtonGroup('Delete/Add')
    self.btn_addmin_step_aligner.btn_increase.clicked.connect(lambda e: add_step(self, e))
    self.btn_addmin_step_aligner.btn_decrease.clicked.connect(lambda e: delete_step(self, e))
    
    
    self.panel_step_aligner_layout.addWidget(slider_group)
    self.panel_step_aligner_layout.addWidget(self.btn_addmin_step_aligner)
    
    self.panel_step_aligner_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
    parent_layout.addWidget(self.panel_step_aligner_widget,20, 0, 1, 11)
    
    
def on_value_change(self, e):
    print('value change', e)
    te='Aligner {0}/{1}'.format(str(self.slider_step_aligner.value()), str(self.slider_step_aligner.maximum()))
    self.label_slider_step_aligner.setText(te)
    # apply_transform_arch(self, e)
    change_step(self,e)

def add_step(self,event):
    max = self.slider_step_aligner.maximum()
    self.slider_step_aligner.setMaximum(max+1)
    val = self.slider_step_aligner.value()
    if(val==max):
        print("add_transform arch",self.slider_step_aligner.value())
        add_transform_arch(self,self.slider_step_aligner.value())
        self.slider_step_aligner.setValue(self.slider_step_aligner.maximum())
    print('add step',self.slider_step_aligner.value())
    # apply_transform_arch(self, self.slider_step_aligner.value())
    change_step(self,self.slider_step_aligner.value())
    
    
def delete_step(self, event):
    max = self.slider_step_aligner.maximum()
    if(max>0):
        self.slider_step_aligner.setMaximum(max-1)
        val = self.slider_step_aligner.value()
        if(val==max):
            self.slider_step_aligner.setValue(self.slider_step_aligner.maximum())
        remove_transform_arch(self,val)   
    print('delete step')
    # apply_transform_arch(self, self.slider_step_aligner.value())
    change_step(self,self.slider_step_aligner.value())
    