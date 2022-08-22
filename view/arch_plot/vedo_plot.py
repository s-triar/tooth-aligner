from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Plotter
from controller.vedo_plotter_controller import vedo_plot_mouse_click
def create_vtk_view_with_vedo(self, parent_layout):
    self.vtk_widget = QVTKRenderWindowInteractor()
    parent_layout.addWidget(self.vtk_widget, 1, 0, 19, 11)
    create_vedo_plot(self)
    

def create_vedo_plot(self):
    self.model_plot = None
    self.model_plot = Plotter(qtWidget=self.vtk_widget, pos=(0, 0), axes=7)
    self.model_plot.show()
    self.model_plot.addCallback("mouse click", lambda event: vedo_plot_mouse_click(self,event))
    