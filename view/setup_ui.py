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

from view.toolbar_bottom.index import create_bottom_panel

vtkmodules.qt.QVTKRWIBase = "QGLWidget"

from view.arch_plot.vedo_plot import create_vtk_view_with_vedo
from view.toolbar_top.index import create_top_toolbar
from view.toolbar_right.index import create_right_panel
def setup_ui(self):
    create_vtk_view_with_vedo(self, self.main_layout)
    create_top_toolbar(self, self.main_layout)
    create_right_panel(self, self.main_layout)
    create_bottom_panel(self, self.main_layout)
    self.setLayout(self.main_layout)