def toggle_model(self, id_show, arch_type):
    models = []
    for m in self.models:
        if (arch_type == m.arch_type):
            models.append(m.mesh)
    if (len(models) > 0):
        if (id_show == True):
            for m in models:
                self.model_plot.add(m)
        if (id_show == False):
            self.model_plot.clear(actors=models)
    self.model_plot.render()