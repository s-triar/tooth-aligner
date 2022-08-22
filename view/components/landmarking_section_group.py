from PyQt5.QtWidgets import (
    QPushButton,
    QStyleOption,
    QStyle,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QGroupBox
)
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPainter, QIcon, QPen,QPainter,QColor
from PyQt5.QtCore import Qt, QSize, QRect
from constant.enums import ArchType, LandmarkDefinition
from utility.colors import convert_label_to_color, convert_landmark_to_color
from utility.names import convert_landmark_val_to_name, convert_tooth_val_to_name, convert_arch_val_to_name

from controller.landmarking_controller import set_selected_face_label, set_selected_q_label_landmarking, reset_selected_q_label_landmarking, show_landmark

class LandmarkCircle(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(LandmarkCircle,self).__init__(*args, **kwargs)
        self.color = color
        self.setFixedSize(50, 50)
        
    def paintEvent(self, event):
        center = self.rect().center()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.drawRoundedRect(QRect(-12, -12, 2*7, 2*7), 30, 30)
        painter.setBrush(QColor(self.color[0],self.color[1],self.color[2]))

        pen = QPen(QColor(self.color[0],self.color[1],self.color[2]))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(QRect(-12, -12, 2*7, 2*7), 30, 30)

class LandmarkGroupLabel(QWidget):
    def __init__(self,main_win, arch_id, tooth_id, ld_val, *args, **kwargs) -> None:
        super(LandmarkGroupLabel, self).__init__(*args, **kwargs)
        # self.main_win=main_win
        layout= QHBoxLayout()
        ld_name=convert_landmark_val_to_name(ld_val)
        label = QLabel(ld_name)
        layout.addWidget(label)
        color_landmark= convert_landmark_to_color(ld_val)
        indicator=LandmarkCircle(color_landmark)
        layout.addWidget(indicator)
        coordinate=QLabel("")
        coordinate.setObjectName('coordinate_ld_'+str(arch_id)+'_'+str(tooth_id)+'_'+str(ld_val))
        layout.addWidget(coordinate)
        btn_change_landmark=QPushButton('Change')
        btn_change_landmark.setObjectName('btn_change_ld_'+str(arch_id)+'_'+str(tooth_id)+'_'+str(ld_val))
        btn_change_landmark.clicked.connect(lambda e: click_btn_edit_landmark(main_win,btn_change_landmark.objectName(),btn_change_landmark))
        btn_change_landmark.setCheckable(True)
        btn_change_landmark.setChecked(False)
        btn_change_landmark.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        layout.addWidget(btn_change_landmark)
        self.setLayout(layout)

def click_btn_edit_landmark(main_win,obj_name,obj):
    btns = obj.parent().parent().parent().parent().findChildren(QPushButton)
    for btn in btns:
        if obj.isChecked() and btn != obj and 'btn_change_ld_' in btn.objectName():
            btn.setDisabled(True)
        elif (not obj.isChecked()) and (not btn.isEnabled()) and btn != obj and 'btn_change_ld_' in btn.objectName():
            btn.setEnabled(True)
    obj_labels = obj.parent().findChildren(QLabel)
    obj_label=None
    for o in obj_labels:
        if('coordinate_ld_' in o.objectName()):
            obj_label = o
    if(obj.isChecked()):
        set_selected_q_label_landmarking(main_win, obj_label)
        obj_names = obj_label.objectName().split('_')
        arch_id = int(obj_names[2])
        tooth_label = int(obj_names[3])
        landmark = int(obj_names[4])
        set_selected_face_label(main_win, landmark, tooth_label, arch_id)
    else:
        reset_selected_q_label_landmarking(main_win)
        # show_landmark(main_win)
        

class LandmarksSection(QWidget):
    def __init__(self, main_win, arch_id, tooth_id,landmarks, *args, **kwargs) -> None:
        super(LandmarksSection, self).__init__(*args, **kwargs)
        layout=QVBoxLayout()
        for ld_id in landmarks:
            ld_group = LandmarkGroupLabel(main_win,arch_id, tooth_id, ld_id)
            layout.addWidget(ld_group)
        self.setLayout(layout)
        
class LandmarkToothSection(QWidget):
    def __init__(self, main_win, arch_id, tooth_id,landmarks, *args, **kwargs) -> None:
        super(LandmarkToothSection, self).__init__(*args, **kwargs)
        layout = QVBoxLayout()
        color_tooth = convert_label_to_color(tooth_id)
        label_tooth_group = QWidget()
        label_tooth_group_layout = QHBoxLayout()
        tooth_name = convert_tooth_val_to_name(tooth_id)
        label = QLabel("("+str(tooth_id)+") "+tooth_name)
        label_tooth_group_layout.addWidget(label)
        btn_toggle_landmark = QPushButton("Open")
        
        # btn_toggle_landmark.clicked.connect(lambda e: )
        # btn_toggle_landmark.toggled.connect(lambda e: )
        btn_toggle_landmark.setCheckable(True)
        btn_toggle_landmark.setChecked(False)
        btn_toggle_landmark.setObjectName('btn_toggle_ld_'+str(arch_id)+'_'+str(tooth_id))
        btn_toggle_landmark.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        label_tooth_group_layout.addWidget(btn_toggle_landmark)
        label_tooth_group.setLayout(label_tooth_group_layout)
        layout.addWidget(label_tooth_group)
        section_ld = LandmarksSection(main_win, arch_id, tooth_id,landmarks)
        section_ld.setObjectName('ld_section_'+str(arch_id)+'_'+str(tooth_id))
        layout.addWidget(section_ld)
        # section_ld.hide()
        self.setLayout(layout)



class LandmarkArchGroup(QGroupBox):
    def __init__(self, main_win, arch_id, *args, **kwargs) -> None:
        super(LandmarkArchGroup, self).__init__(*args, **kwargs)
        arch_name = convert_arch_val_to_name(arch_id)
        self.setTitle(arch_name)
        layout = QVBoxLayout()
        for tooth_key in LandmarkDefinition.archs[arch_id]:
            ld_tooth_section = LandmarkToothSection(main_win, arch_id, tooth_key, LandmarkDefinition.archs[arch_id][tooth_key])
            layout.addWidget(ld_tooth_section)
        self.setLayout(layout)
        
    def paintEvent(self, a0) -> None:
        return super().paintEvent(a0)