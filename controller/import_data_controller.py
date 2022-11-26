from vedo import load
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

def calculate_studi_model(self):
    if(Arch._is_complete()):
        for m in self.models:
            m.extract_tooth()
        self.bolton_studi_model.calc_anterior_overall(self.models)
        # print("get_anterior_overall",self.bolton_studi_model.get_anterior_overall())
        # print("overjet",self.bolton_studi_model.get_overjet())
        self.korkhaus_studi_model.calculate_khorkaus(self.models)
        self.pont_studi_model.calculate_pont(self.models)
        self.carey_studi_model.calculate_carey(self.models)

def reset_model(self):
    self.model_plot.clear()
    Arch._clear()
    self.models = []
    self.model_paths = []
    self.model_plot.render()

def check_archs_loaded(self):
    return Arch._is_complete()