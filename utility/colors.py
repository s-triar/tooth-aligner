import math
import numpy as np
from constant.enums import LandmarkType, ToothType
def map_label_color(label):
    label = math.floor(label)
    if(label==ToothType.DELETED.value):
        return [20,20,20]
    elif(label==ToothType.GINGIVA.value):
        return [255,162,143]
    elif(label==ToothType.MOLAR_UR7_LL7.value):
        return [150,117,148]
    elif(label==ToothType.MOLAR_UR6_LL6.value):
        return [170,255,255]
    elif(label==ToothType.PREMOLAR_UR5_LL5.value):
        return [255,  0,127]
    elif(label==ToothType.PREMOLAR_UR4_LL4.value):
        return [170,255,127]
    elif(label==ToothType.CANINE_UR3_LL3.value):
        return [  0,  0,127]
    elif(label==ToothType.INCISOR_UR2_LL2.value):
        return [255,255,127]
    elif(label==ToothType.INCISOR_UR1_LL1.value):
        return [255,170,255]
    elif(label==ToothType.INCISOR_UL1_LR1.value):
        return [255,255,255]
    elif(label==ToothType.INCISOR_UL2_LR2.value):
        return [ 77, 99, 82]
    elif(label==ToothType.CANINE_UL3_LR3.value):
        return [255,  0,255]
    elif(label==ToothType.PREMOLAR_UL4_LR4.value):
        return [255,255,  0]
    elif(label==ToothType.PREMOLAR_UL5_LR5.value):
        return [  0,  0,255]
    elif(label==ToothType.MOLAR_UL6_LR6.value):
        return [  0,255,  0]
    elif(label==ToothType.MOLAR_UL7_LR7.value):
        return [255,  0,  0]
    
def map_landmark_color(ld):
    if(ld==LandmarkType.MESIAL.value):
        return [255,0,0]
    elif(ld==LandmarkType.DISTAL.value):
        return [0,0,255]
    elif(ld==LandmarkType.BUCCAL_OR_LABIAL.value):
        return [200,200,200]
    elif(ld==LandmarkType.LINGUAL_OR_PALATAL.value):
        return [75,75,75]
    elif(ld==LandmarkType.PIT.value):
        return [255,255,255]
    elif(ld==LandmarkType.CUSP.value):
        return [150,155,255]
    
    elif(ld==LandmarkType.CUSP_IN.value):
        return [255,90,180]
    elif(ld==LandmarkType.CUSP_IN_MESIAL.value):
        return [255,150,30]
    elif(ld==LandmarkType.CUSP_IN_DISTAL.value):
        return [255,240,0]
    
    elif(ld==LandmarkType.CUSP_OUT.value):
        return [50,255,240]
    elif(ld==LandmarkType.CUSP_OUT_MESIAL.value):
        return [40,255,180]
    elif(ld==LandmarkType.CUSP_OUT_MIDDLE.value):
        return [90,160,90]
    elif(ld==LandmarkType.CUSP_OUT_DISTAL.value):
        return [20,255,0]
    

def convert_labels_to_colors(labels):
    new_colors =np.zeros((len(labels), 3),dtype=np.uint8)
    for i in range(len(labels)):
        new_colors[i] = map_label_color(labels[i])
    return new_colors

def convert_label_to_color(label):
    return map_label_color(label)

def convert_landmark_to_color(ld):
    return map_landmark_color(ld)