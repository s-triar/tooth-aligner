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

class KorkhausArchSection(QWidget):
    def __init__(self, l_distance, *args, **kwargs) -> None:
        super(KorkhausArchSection, self).__init__(*args, **kwargs)
        layout = QGridLayout()
        titik_dua = QLabel(':')
        # l
        l = QLabel('Panjang Garis Korkhaus')
        d_l = QLabel('{0:.3f}'.format(l_distance))
        
        layout.addWidget(l,0,0)
        layout.addWidget(titik_dua,0,1)
        layout.addWidget(d_l,0,2)
        self.setLayout(layout)