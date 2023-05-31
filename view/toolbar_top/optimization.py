import math

import numpy as np
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
    QAction,
    QSizePolicy
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets
from constant.enums import PanelMode
from controller.bite_contact_controller import reset_bite_contact
from controller.segmentation_controller import set_selected_arch, set_selected_label
from controller.step_controller import update_transform_arch
from controller.summary_controller import (calculate_studi_model, get_Bs_pts, get_line_centers_pts, get_studi_model_summary_pts, get_summary_flat_pts, get_As_pts, get_destination_tooth)
from optimization.de_optimization5 import start_de
from utility.app_tool import get_saved_optimization_step_value

from view.components.toolbar_top_section import ToolbarTopSection
from view.components.tool_top_button import ToolTopButton
import copy
import csv
from pathlib import Path
def create_optimization_menu(self, parent_layout):
    self.container_tool_btn = QWidget()
    self.container_tool_btn_layout = QHBoxLayout()
    self.container_tool_btn.setLayout(self.container_tool_btn_layout)
    
    self.btn_de_optimization = ToolTopButton("DE Optimization",'icons/teeth-segmentation.png','icons/teeth-segmentation-colors.png',True)
    
    # self.btn_de_optimization.setObjectName('btn_toolbar_tool_segmentation')
    self.btn_de_optimization.clicked.connect(lambda e: click_btn_de_optimization(self,e))
    # self.btn_de_optimization.toggled.connect(lambda e: toggle_btn_de_optimization(self,e))
    self.container_tool_btn_layout.addWidget(self.btn_de_optimization)
    
    
    section = ToolbarTopSection("Optimization",self.container_tool_btn)
    section.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
    parent_layout.addWidget(section)


def check_decrement_teeth_error(last_three_errors):
    res = []
    if len(last_three_errors) < 3:
        return True
    for i in range(len(last_three_errors[0])):
        check_decrease = math.floor(last_three_errors[0][i]) - math.floor(last_three_errors[2][i]) # harus > 1 untuk lanjut
        if check_decrease <= 1:
            res.append(True)
        else:
            res.append(False)
    return res

def is_tooth_need_continue(states):
    return not np.array(states).all()

def click_btn_de_optimization(self, e):
    path_model = self.model_paths[0]
    filepathsave = get_saved_optimization_step_value(path_model)
    filepath = Path(filepathsave)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    last_three_errors = []
    n_tooth = 14

    teeth_errors = [120000] * (2 * n_tooth)
    # error_opt = [1200000, 1200000] #uppper, lower
    is_arch_finish = [False, False] #upper, lower
    is_tooth_finish = [False] * (2 * n_tooth)
    step_i = 1
    gen = []
    new_models=self.models
    flats = copy.deepcopy(get_summary_flat_pts(self))
    summary = copy.deepcopy(get_studi_model_summary_pts(self))
    Bs = copy.deepcopy(get_Bs_pts(self))
    As = copy.deepcopy(get_As_pts(self))
    destination_tooth = copy.deepcopy(get_destination_tooth(self))
    line_centers = copy.deepcopy(get_line_centers_pts(self))
    # error_upper = 10
    # error_lower = 10
    # while(step_i<16):
    while(is_tooth_need_continue(is_tooth_finish) and step_i <= 100):
        self.btn_addmin_step_aligner.btn_increase.click()
        print("step_i",step_i)
        step_i+=1
        # new_models, gen, error_opt = start_de(self.models, get_summary_flat_pts(self), get_studi_model_summary_pts(self), gen)
        # print("eror", error_opt)
        # while(error_opt>5000):
        new_models, gen, error_opt,teeth_errors, is_arch_finish, is_tooth_finish,timede = start_de(new_models, flats, summary, line_centers, Bs, gen, As, destination_tooth, is_arch_finish, is_tooth_finish, teeth_errors)

        if len(last_three_errors) < 3:
            last_three_errors.append(teeth_errors)
        else:
            last_three_errors.append(teeth_errors)
            last_three_errors = last_three_errors[1:]

        is_tooth_finish = check_decrement_teeth_error(last_three_errors)


        # if error_opt[0] < error_upper:
        #     is_arch_finish[0] = True
        # if error_opt[1] < error_lower:
        #     is_arch_finish[1] = True

        print("eror in while", error_opt)
        print(gen)
        #     save optimization process
        f = open(filepathsave, 'a+', encoding='utf-8', newline='')
        writer = csv.writer(f)
        teeth_err = '|'.join(['%.4f'.format(c) for c in teeth_errors])
        chromo = '|'.join([str(c) for c in gen])
        t_chromo = '|'.join(["T" if c == True else "F" for c in is_tooth_finish])
        writer.writerow([step_i, error_opt, timede, t_chromo, teeth_err, chromo])
        f.close()

        for i in range(len(self.models)):
            self.models[i].mesh = new_models[i].mesh.clone()
            self.models[i].right_left_vec = new_models[i].right_left_vec
            self.models[i].forward_backward_vec = new_models[i].forward_backward_vec
            self.models[i].upward_downward_vec = new_models[i].upward_downward_vec
            self.models[i].gingiva=new_models[i].gingiva
            self.models[i].teeth=new_models[i].teeth
            update_transform_arch(self,self.step_model.get_current_step())
            # calculate_studi_model(self)
        # self.btn_addmin_step_aligner.btn_increase.click()
    self.btn_de_optimization.setChecked(False)
    # self.model_plot.add(new_models[0].mesh)
    # self.model_plot.add(new_models[1].mesh)
    # self.model_plot.render()
    