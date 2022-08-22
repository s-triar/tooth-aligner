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

class ToothMaterialGroupLabel():
    def __init__(self,tooth_label, width, parent_layout_grid, row) -> None:
        label = QLabel('('+str(tooth_label)+') '+convert_tooth_val_to_name(tooth_label))
        indicator = CircleIndicatorLabel(convert_label_to_color(tooth_label))
        width_label = QLabel('{0:.3f}'.format(width))
        parent_layout_grid.addWidget(indicator,row,0)
        parent_layout_grid.addWidget(label,row,1)
        parent_layout_grid.addWidget(width_label,row,2)
        
class BoltonArchSection(QWidget):
    def __init__(self, data_tooth_width, *args, **kwargs) -> None:
        super(BoltonArchSection, self).__init__(*args, **kwargs)
        layout = QGridLayout()
        row = 0
        for k in data_tooth_width:
            label = QLabel('('+str(k)+') '+convert_tooth_val_to_name(k))
            indicator = CircleIndicatorLabel(convert_label_to_color(k))
            width_label = QLabel("{0:.3f}".format(data_tooth_width[k]))
            layout.addWidget(indicator,row,0)
            layout.addWidget(label,row,1)
            layout.addWidget(width_label,row,2)
            row+=1
        self.setLayout(layout)


            
        
        
        
        
