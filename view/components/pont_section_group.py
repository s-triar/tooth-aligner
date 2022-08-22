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

class PontArchSection(QWidget):
    def __init__(self, anterior_total_tooth_material, p1_distance, m1_distance, *args, **kwargs) -> None:
        super(PontArchSection, self).__init__(*args, **kwargs)
        layout = QGridLayout()
        
        # anterior
        label_anterior = QLabel('Anterior Width')
        w_anterior = QLabel('{0:.3f}'.format(anterior_total_tooth_material))
        # p1
        label_p1 = QLabel('Premolar 1')
        d_p1 = QLabel('{0:.3f}'.format(p1_distance))
        # m1
        label_m1 = QLabel('Molar 1')
        d_m1 = QLabel('{0:.3f}'.format(m1_distance))
        titik_dua = QLabel(':')
        layout.addWidget(label_anterior,0,0)
        layout.addWidget(titik_dua,0,1)
        layout.addWidget(w_anterior,0,2)
        titik_dua = QLabel(':')
        layout.addWidget(label_p1,1,0)
        layout.addWidget(titik_dua,1,1)
        layout.addWidget(d_p1,1,2)
        titik_dua = QLabel(':')
        layout.addWidget(label_m1,2,0)
        layout.addWidget(titik_dua,2,1)
        layout.addWidget(d_m1,2,2)
        
        self.setLayout(layout)