


from PyQt5.QtWidgets import (
    QPushButton,
    QStyleOption,
    QStyle,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon
from PyQt5.QtCore import Qt, QSize


class ButtonRotation(QtWidgets.QPushButton):
    def __init__(self, icon, icon_active, *args, **kwargs) -> None:
        super(ButtonRotation, self).__init__(*args, **kwargs)
        self.icon_path = icon
        self.icon_path_active = icon_active
        self.setIconSize(QSize(40,40))
        self.setIcon(QIcon(self.icon_path))
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
    
    def paintEvent(self, e) -> None:
        if(self.isDown()):
            self.setIcon(QIcon(self.icon_path_active))
        else:
            self.setIcon(QIcon(self.icon_path))
        return super().paintEvent(e)
    


class RotationButtonGroup(QtWidgets.QWidget):
    def __init__(self, title, *args, **kwargs) -> None:
        super(RotationButtonGroup, self).__init__(*args, **kwargs)
        icon_increase='icons/circle-plus-solid.png'
        icon_decrease='icons/circle-minus-solid.png'
        icon_increase_active='icons/circle-plus-solid-colors.png'
        icon_decrease_active='icons/circle-minus-solid-colors.png'
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        layout_main = QVBoxLayout()
        self.setLayout(layout_main)
        
        f = QFont()
        f.setBold(True)
        title = QLabel(title)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(f)
        title.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        title.setStyleSheet("color:rgb(29, 155, 240);font-size:12pt;")
        layout_main.addWidget(title)
        
        group_btns = QWidget()
        layout_btns = QHBoxLayout()
        self.btn_increase = ButtonRotation(icon_increase,icon_increase_active)
        self.btn_decrease = ButtonRotation(icon_decrease,icon_decrease_active)
        layout_btns.addWidget(self.btn_decrease)
        layout_btns.addWidget(self.btn_increase)
        group_btns.setLayout(layout_btns)
        layout_main.addWidget(group_btns)
        self.setProperty('class','rotation_group_btn')
        # self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # self.setText(title)
    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
            
    # def paintEvent(self, e) -> None:
    #     if(self.isCheckable()):
    #         if self.isChecked():
    #             self.setIcon(QIcon(self.icon_active_path))
    #         else:
    #             self.setIcon(QIcon(self.icon_path))
            
    #     return super().paintEvent(e)