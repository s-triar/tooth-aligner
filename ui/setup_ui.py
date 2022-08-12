from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
    QFormLayout
)
import vtk
import vtkmodules.qt
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vedo import Plotter

vtkmodules.qt.QVTKRWIBase = "QGLWidget"

from ui.arch_plot.vedo_plot import create_vtk_view_with_vedo
from ui.toolbar_top.index import create_top_toolbar

def setup_ui(self):
    create_vtk_view_with_vedo(self)
    create_top_toolbar(self, self.main_layout)
    self.setLayout(self.main_layout)