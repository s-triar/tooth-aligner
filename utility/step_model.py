class StepModel():
    def __init__(self) -> None:
        self.step_models=[]
        self.step_teeth=[]
        self.current_step=0
    
    def get_current_step(self):
        return self.current_step
    
    def change_current_step(self, s):
        self.current_step = s
    
    def add_step_model(self, models, teeth):
        self.step_models.append(models.copy())
        self.step_teeth.append(teeth.copy())
        
    def remove_step_model(self, index):
        # self.step_models.pop(index)
        self.step_models = [element for (i,element) in enumerate(self.step_models) if i != index]
    
    def get_step_model(self, index):
        return self.step_models[index], self.step_teeth[index]
    
    def update_step_model(self, index, models, teeth):
        mdls = self.step_models[0:index]
        mdls.append(models.copy())
        self.step_models = mdls
        
        steps = self.step_teeth[0:index]
        steps.append(teeth.copy())
        self.step_models = steps