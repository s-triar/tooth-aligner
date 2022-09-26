
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
    QComboBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor

from constant.enums import ArchType, ToothType
from utility.colors import convert_label_to_color

from controller.segmentation_controller import apply_change_segmantation, reset_change_segmentation, set_selected_arch, set_selected_label, undo_change_segmentation

def create_panel_segmentation(self, parent_layout):
    self.panel_segmentation_widget = QWidget()
    self.panel_segmentation_layout = QVBoxLayout()
    self.panel_segmentation_widget.setLayout(self.panel_segmentation_layout)

    self.combo_box_arch_segmentation = QComboBox()
    model_arch = self.combo_box_arch_segmentation.model()
    for data in ArchType:
        self.combo_box_arch_segmentation.addItem(data.name, data.value)
        # model_arch.setData(model_arch.index(data.value, 0))
    self.combo_box_arch_segmentation.currentIndexChanged.connect(lambda e: change_arch_combo_box(self, e))

    self.combo_box_label_segmentation = QComboBox()

    model = self.combo_box_label_segmentation.model()
    for data in ToothType:
        self.combo_box_label_segmentation.addItem(data.name, data.value)
        color = convert_label_to_color(data.value)
        model.setData(model.index(data.value, 0), QColor(color[0],color[1],color[2]), Qt.BackgroundRole)
        if(data.value == ToothType.DELETED.value):
            model.setData(model.index(data.value, 0), QColor(255,255,255), Qt.ItemDataRole.ForegroundRole)

    self.combo_box_label_segmentation.currentIndexChanged.connect(lambda e: change_label_combo_box(self, e))

    # self.combo_box_label_segmentation.activated.connect(self.accept)

    self.btn_apply_segmentation = QPushButton("Apply")
    self.btn_reset_segmentation = QPushButton("Reset")
    self.btn_undo_segmentation = QPushButton("Undo")
    self.btn_apply_segmentation.clicked.connect(lambda e: apply_changed_segmentation(self))
    self.btn_reset_segmentation.clicked.connect(lambda e: reset_changed_segmentation(self))
    self.btn_undo_segmentation.clicked.connect(lambda e: undo_changed_segmentation(self))
    self.btn_undo_segmentation.setEnabled(False)
    self.btn_apply_segmentation.setEnabled(False)
    self.btn_reset_segmentation.setEnabled(False)
    lh_w=QWidget()
    lh= QHBoxLayout()
    lh_w.setLayout(lh)
    lh.addWidget(self.btn_reset_segmentation)
    lh.addWidget(self.btn_undo_segmentation)
    self.panel_segmentation_layout.addWidget(self.combo_box_arch_segmentation)
    self.panel_segmentation_layout.addWidget(self.combo_box_label_segmentation)
    self.panel_segmentation_layout.addWidget(lh_w)
    self.panel_segmentation_layout.addWidget(self.btn_apply_segmentation)
    
    self.panel_segmentation_layout.addStretch()
    # self.panel_segmentation_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
    parent_layout.addWidget(self.panel_segmentation_widget,1, 11, 20, 1)
    self.panel_segmentation_widget.hide()
    
    # self.panel_segmentation_widget.setObjectName('panel_tool_right')

def change_arch_combo_box(self, i):
    id_us = self.combo_box_arch_segmentation.itemData(self.combo_box_arch_segmentation.currentIndex()) # .toPyObject()
    # print('VAL arch',id_us, i)
    set_selected_arch(self, id_us)

def change_label_combo_box(self, i):
    id_us = self.combo_box_label_segmentation.itemData(self.combo_box_label_segmentation.currentIndex()) # .toPyObject()
    # print('VAL tooth',id_us,i)
    set_selected_label(self, id_us)

def reset_changed_segmentation(self):
    reset_change_segmentation(self)
    
def apply_changed_segmentation(self):
    apply_change_segmantation(self)

def undo_changed_segmentation(self):
    undo_change_segmentation(self)
# def color(self):
#         return self.combo_box_label_segmentation.currentData(Qt.BackgroundRole)

# def colorName(self):
#     return self.combo_box_label_segmentation.currentText()