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
from controller.attachment_controller import init_var_attachment
from controller.grid_controller import init_var_grid
from controller.landmarking_controller import init_var_landmarking
from controller.rotation_controller import init_var_rotation
from controller.segmentation_controller import init_var_segmentation
from controller.step_controller import init_var_step


vtkmodules.qt.QVTKRWIBase = "QGLWidget"

from view.setup_ui import setup_ui
from controller.vedo_plotter_controller import init_var_vedo_model
from controller.bolton_controller import init_var_bolton
from controller.pont_controller import init_var_pont
from controller.korkhaus_controller import init_var_korkhaus

class Window(QFrame):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.main_layout = QGridLayout()
        init_var_vedo_model(self)
        
        init_var_bolton(self)
        init_var_korkhaus(self)
        init_var_pont(self)
        init_var_step(self)
        init_var_attachment(self)
        init_var_grid(self)
        # self.click_plot_mode = None
        # self.tooth_selected={
        #     "label": None,
        #     "mode" : None, # mesial, distal, out (buccal or labial), in (lingual or palatal), cusp, pit
        #     "index": None
        # }
        # self.mesh_selected = {
        #     'arch_type': '',
        #     'arch': None
        # }
        setup_ui(self)
        init_var_rotation(self)
        init_var_segmentation(self)
        init_var_landmarking(self)
        
        
        
        


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowState(Qt.WindowMaximized)

        self.mVtkWindow = Window()
        self.setCentralWidget(self.mVtkWindow)
        
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QFile, QIODevice
import glob





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # apply_stylesheet(app, theme='light_blue.xml')
    for j in glob.glob('icons/*.png'):
    
        p = QPixmap()
        p.load(j)

        file = QFile(j)
        file.open(QIODevice.WriteOnly)
        p.save(file,'PNG')
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
