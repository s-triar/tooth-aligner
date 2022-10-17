
from view.toolbar_right.panel_carey import create_panel_carey
from view.toolbar_right.panel_grid import create_panel_grid
from view.toolbar_right.panel_rotation import create_panel_rotation
from view.toolbar_right.panel_segmentation import create_panel_segmentation
from view.toolbar_right.panel_landmarking import create_panel_landmarking
from view.toolbar_right.panel_bolton import create_panel_bolton
from view.toolbar_right.panel_pont import create_panel_pont
from view.toolbar_right.panel_korkhaus import create_panel_korkhaus
from view.toolbar_right.panel_attachment import create_panel_attatchment
from view.toolbar_right.panel_summary import create_panel_summary

def create_right_panel(self, parent_layout):
    create_panel_rotation(self, parent_layout)
    create_panel_segmentation(self, parent_layout)
    create_panel_landmarking(self, parent_layout)
    create_panel_bolton(self, parent_layout)
    create_panel_pont(self, parent_layout)
    create_panel_korkhaus(self, parent_layout)
    create_panel_attatchment(self, parent_layout)
    create_panel_summary(self, parent_layout)
    create_panel_grid(self, parent_layout)
    create_panel_carey(self, parent_layout)