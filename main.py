from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QFrame,
    QWidget,
    QGridLayout
)
import sys
# from qt_material import apply_stylesheet

import vtkmodules.qt
import os


vtkmodules.qt.QVTKRWIBase = "QGLWidget"

from ui.setup_ui import setup_ui

class Window(QFrame):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.models = []
        self.main_layout = QGridLayout()
        self.click_plot_mode = None
        self.tooth_selected={
            "label": None,
            "mode" : None, # mesial, distal, out (buccal or labial), in (lingual or palatal), cusp, pit
            "index": None
        }
        self.mesh_selected = {
            'arch_type': '',
            'arch': None
        }
        setup_ui(self)
        
        


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowState(Qt.WindowMaximized)

        self.mVtkWindow = Window()
        self.setCentralWidget(self.mVtkWindow)
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='light_blue.xml')
    stylesheet = app.styleSheet()
    with open('custom-style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))
    screen = app.primaryScreen()
    size = screen.size()
    print('Screen: %s' % screen.name())
    print('Size: %d x %d' % (size.width(), size.height()))
    window = MainWindow()
    window.show()
    app.exec_()
