from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QRect

class CircleIndicatorLabel(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(CircleIndicatorLabel,self).__init__(*args, **kwargs)
        self.color = color
        self.setFixedSize(50, 50)
        
    def paintEvent(self, event):
        center = self.rect().center()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.drawRoundedRect(QRect(-12, -12, 2*7, 2*7), 30, 30)
        painter.setBrush(QColor(self.color[0],self.color[1],self.color[2]))

        pen = QPen(QColor(self.color[0],self.color[1],self.color[2]))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(QRect(-12, -12, 2*7, 2*7), 30, 30)
