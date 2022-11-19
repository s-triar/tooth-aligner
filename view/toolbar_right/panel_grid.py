# pitch
# roll
# yaw

# pivot

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
    QLabel,
    QFormLayout,
    QFrame, 
    QScrollArea,
    QSizePolicy
)
from vedo import Line, Point, Grid
from PyQt5.QtCore import Qt, QSize
from constant.enums import ArchType
from controller.vedo_plotter_controller import remove_not_arch
import numpy as np

def create_panel_grid(self, parent_layout):
    self.grid_panel_widget_container = QWidget()
    self.grid_panel_layout_container = QVBoxLayout()
    
    self.grid_panel_widget = QWidget()
    self.grid_panel_layout = QVBoxLayout()
    
    self.grid_panel_widget_area = QScrollArea()
    self.grid_panel_widget_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.grid_panel_widget_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.grid_panel_widget_area.setWidgetResizable(True)
    self.grid_panel_widget_area.setWidget(self.grid_panel_widget)
    
    self.grid_panel_widget.setLayout(self.grid_panel_layout)
    self.grid_panel_layout_container.addWidget(self.grid_panel_widget_area)
    self.grid_panel_widget_container.setLayout(self.grid_panel_layout_container)
    self.grid_panel_widget_container.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
    self.grid_panel_widget_container.setFixedWidth(600)
    
    self.pane_arch_grid=QWidget()
    self.grid_panel_layout.addWidget(self.pane_arch_grid)
    
    self.grid_summary_label=QLabel()
    self.grid_panel_layout.addWidget(self.grid_summary_label)
    self.grid_panel_layout.addStretch()
    
        
    parent_layout.addWidget(self.grid_panel_widget_container, 1, 11, 20, 1)

    self.grid_panel_widget_container.hide()
    
def draw_grid_lines(self):
    remove_not_arch(self, excepts_name_like='attachment')
    x2 = np.linspace(-30,30,120,endpoint=False, retstep=True)
    y2 = np.linspace(-30,30,120,endpoint=False, retstep=True)

    # print(x2[1])

    
    gr2 = Grid(sx=x2[0], sy=y2[0]).wireframe(True).lc((200,100,200))
    gr2.name = "Grid Board"
    self.model_plot.add(gr2)
    self.model_plot.render()
    
def draw_grid_lines_overlay(self):
    position = (0, 0, 0)
    gridSize = 500
    fineGrid = Grid(pos=position, s=(gridSize, gridSize), res=(gridSize, gridSize), c='k4')
    fineGrid.name = "Grid Board Fine"
    largeGrid = Grid(pos=position, s=(gridSize, gridSize), res=((int)(gridSize / 10), (int)(gridSize / 10)), lw=2, c='k2')
    largeGrid.name = "Grid Board Large"
    
    fineGrid.followCamera(self.model_plot.camera)
    largeGrid.followCamera(self.model_plot.camera)
    self.model_plot.parallelProjection(True)
    self.model_plot.add(fineGrid)
    self.model_plot.add(largeGrid)
    self.model_plot.render()

        
        