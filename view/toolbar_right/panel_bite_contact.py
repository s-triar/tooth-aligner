from controller.bite_contact_controller import get_bite_contact


def draw_bite_contact(self):
    cap_bite_up_low, cap_bite_low_up = get_bite_contact(self)
    self.model_plot.add(cap_bite_up_low)
    self.model_plot.add(cap_bite_low_up)
    self.model_plot.render()