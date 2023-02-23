from pathlib import Path

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QAction,
    QSizePolicy,
    QVBoxLayout,
    QFileDialog
)

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from constant.enums import ArchType, PanelMode
from controller.bite_contact_controller import reset_bite_contact
from controller.import_data_controller import load_opt_model
from controller.landmarking_controller import save_landmark, load_landmark
from controller.segmentation_controller import save_segmentation, set_selected_arch, set_selected_label
from controller.step_controller import change_step
from controller.summary_controller import calculate_studi_model
from utility.app_tool import get_saved_path

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton
import pandas as pd

def create_save_load_project_menu(self, parent_layout):
    self.container_tool_btn = QWidget()
    self.container_tool_btn_layout = QHBoxLayout()
    self.container_tool_btn.setLayout(self.container_tool_btn_layout)
    
    self.btn_save_project = ToolTopButton("Save Project",'icons/teeth-segmentation.png','icons/teeth-segmentation-colors.png',True)
    self.btn_save_project.clicked.connect(lambda e: click_btn_save_project(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_save_project)
    
    container_load_landmark_widget = QWidget()
    container_load_landmark_layout = QVBoxLayout()
    
    container_load_landmark_widget.setLayout(container_load_landmark_layout)
    
    
    
    self.btn_load_max_landmark = QPushButton('Load Landmark Max')
    self.btn_load_max_landmark.setIcon(QIcon('icons/teeth-open-solid-top.png'))
    self.btn_load_max_landmark.clicked.connect(lambda e: click_btn_load_landmark(self, ArchType.UPPER.value))
    
    container_load_landmark_layout.addWidget(self.btn_load_max_landmark)
    
    self.btn_load_man_landmark = QPushButton('Load Landmark Man')
    self.btn_load_man_landmark.setIcon(QIcon('icons/teeth-open-solid-bottom.png'))
    self.btn_load_man_landmark.clicked.connect(lambda e: click_btn_load_landmark(self, ArchType.LOWER.value))
    container_load_landmark_layout.addWidget(self.btn_load_man_landmark)
    
    self.container_tool_btn_layout.addWidget(container_load_landmark_widget)
    
    self.btn_load_project = ToolTopButton("Load Project",'icons/teeth-segmentation.png','icons/teeth-segmentation-colors.png',True)
    self.btn_load_project.clicked.connect(lambda e: click_btn_load_project(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_load_project)
    
    section = ToolbarTopSection("Save & Load Project",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)


def click_btn_save_project(self, e):
    n_step = self.slider_step_aligner.maximum()+1
    for i in range(n_step):
        change_step(self,i)
        save_segmentation(self) # save model
        save_landmark(self)
    path_model = self.model_paths[0]
    pathsave = get_saved_path(path_model,".json",isProject=True)
    filepath = Path(pathsave)  
    filepath.parent.mkdir(parents=True, exist_ok=True) 
    df = pd.DataFrame()
    df.to_json(filepath) 
    self.btn_save_project.setChecked(False)
    
    
def click_btn_load_landmark(self, type_arch):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilters(["*.csv"])
    filenames = []
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        print(filenames)
    load_landmark(self, type_arch, filenames[0])
    calculate_studi_model(self)
    
    
def click_btn_load_project(self, e):
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog().AnyFile)
    dlg.setNameFilters(["*.json"])
    filenames = []
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        print(filenames)
        load_opt_model(self, filenames[0])
    
    self.btn_load_project.setChecked(False)
    