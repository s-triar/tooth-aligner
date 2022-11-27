from vedo import load
from controller.summary_controller import calculate_studi_model
from utility.arch import Arch

def load_model(self, path, id):
    model_vedo = load(path)
    model = Arch(id, model_vedo)
    self.models.append(model)
    self.model_paths.append(path)
    self.model_plot.add(self.models[-1].get_mesh())
    self.model_plot.addGlobalAxes(axtype=8)
    self.model_plot.resetCamera()
    calculate_studi_model(self)
    print(path) #D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segement_refine_manual/Gerry Sihaj LowerJawScan Cleaned 10000_d_predicted_refined a.vtp



def reset_model(self):
    self.model_plot.clear()
    Arch._clear()
    self.models = []
    self.model_paths = []
    self.model_plot.render()

def check_archs_loaded(self):
    return Arch._is_complete()