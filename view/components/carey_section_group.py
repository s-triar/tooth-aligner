from PyQt5.QtWidgets import (
    QPushButton,
    QStyleOption,
    QStyle,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon, QPen,QPainter,QColor
from PyQt5.QtCore import Qt, QSize, QRect
from constant.enums import ArchType, LandmarkDefinition
from utility.colors import convert_label_to_color, convert_landmark_to_color
from utility.names import convert_landmark_val_to_name, convert_tooth_val_to_name, convert_arch_val_to_name

from view.components.circle_indicator_label import CircleIndicatorLabel

class CareyArchSection(QWidget):
    def __init__(self, total_tooth_material_length, brasswire_length, descrepancy, *args, **kwargs) -> None:
        super(CareyArchSection, self).__init__(*args, **kwargs)
        layout = QGridLayout()
        

        label_ttm= QLabel('TTM')
        w_ttm = QLabel('{0:.3f}'.format(total_tooth_material_length))

        label_brasswire = QLabel('Brasswire Length')
        w_brasswire = QLabel('{0:.3f}'.format(brasswire_length))
        
        label_des = QLabel('Descrepancy')
        w_des = QLabel('{0:.3f}'.format(descrepancy))
        

        
        titik_dua = QLabel(':')
        layout.addWidget(label_ttm,0,0)
        layout.addWidget(titik_dua,0,1)
        layout.addWidget(w_ttm,0,2)
        titik_dua = QLabel(':')
        layout.addWidget(label_brasswire,1,0)
        layout.addWidget(titik_dua,1,1)
        layout.addWidget(w_brasswire,1,2)
        titik_dua = QLabel(':')
        layout.addWidget(label_des,2,0)
        layout.addWidget(titik_dua,2,1)
        layout.addWidget(w_des,2,2)

        
        self.setLayout(layout)