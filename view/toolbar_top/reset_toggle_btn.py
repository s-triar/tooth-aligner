from controller.vedo_plotter_controller import set_plot_click_mode
from view.components.tool_top_button import ToolTopButton

def reset_toggle_tooltop_btn(self, b):
    btns = self.container_tool_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    # analysis
    btns = self.container_toogle_arch_btn.findChildren(ToolTopButton)
    for btn in btns:
        if btn.isChecked() and btn != b:
            btn.setChecked(False)
    # b.setChecked(True)
    btns = self.container_utility_btn.findChildren(ToolTopButton)
    for btn in btns:
        if(btn.isCheckable() and btn.isChecked() and btn != b):
            btn.setChecked(False)
    # set_plot_click_mode(self, None)
    