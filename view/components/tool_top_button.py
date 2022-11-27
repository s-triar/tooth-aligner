from PyQt5.QtWidgets import (
    QToolButton,
    QStyleOption,
    QStyle
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon
from PyQt5.QtCore import Qt, QSize

class ToolTopButton(QToolButton):
    def __init__(self, title, icon_path, icon_active_path, is_checkable, icon_size=[80,40], *args, **kwargs) -> None:
        super(ToolTopButton, self).__init__(*args, **kwargs)
        self.icon_path = icon_path
        self.icon_active_path = icon_active_path
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(icon_size[0],icon_size[1]))
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setText(title)
        
        if is_checkable==True:
            self.setCheckable(True)
            
    def paintEvent(self, e) -> None:
        if(self.isCheckable()):
            if self.isChecked():
                self.setIcon(QIcon(self.icon_active_path))
            else:
                self.setIcon(QIcon(self.icon_path))
            
        return super().paintEvent(e)