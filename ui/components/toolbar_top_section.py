from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QBoxLayout,
    QStyleOption,
    QStyle
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtCore import Qt, QSize

class ToolbarTopSection(QtWidgets.QWidget):
    def __init__(self, title, content, *args, **kwargs) -> None:
        super(ToolbarTopSection, self).__init__(*args, **kwargs)
        # self.this_layout = QBoxLayout(QBoxLayout.Direction.TopToBottom,self)
        # self.setStyleSheet("padding-bottom:4px;")
        self.setObjectName('toolbar_section')
        # self.setStyleSheet('''
        #     .toolbar_section {
        #         border: 1px solid rgb(255,255,255); 
        #         padding-bottom:4px;                  
        #     }
        # ''')
        
        self.setProperty("class","toolbar_section")
        # self.container = QWidget()
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(0,0,0,0)
        self.container_layout.addWidget(content)
        f = QFont()
        f.setBold(True)
        title = QLabel(title)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(f)
        title.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        title.setStyleSheet("color:rgb(29, 155, 240);font-size:12pt;")
        self.container_layout.addWidget(title)
        # self.container.setLayout(self.container_layout)
        # self.this_layout.addWidget(self.container)
        self.setLayout(self.container_layout)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)