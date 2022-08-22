import math
from constant.enums import LandmarkType, ToothType, ArchType

def map_tooth_val_to_name(val):
    # val = math.floor(val)
    if(val == ToothType.GINGIVA.value):
        return 'Gingiva'
    elif(val == ToothType.MOLAR_UR7_LL7.value):
        return 'Molar Second'
    elif(val == ToothType.MOLAR_UR6_LL6.value):
        return 'Molar First'
    elif(val == ToothType.PREMOLAR_UR5_LL5.value):
        return 'Premolar Second'
    elif(val == ToothType.PREMOLAR_UR4_LL4.value):
        return 'Premolar First'
    elif(val == ToothType.CANINE_UR3_LL3.value):
        return 'Canine'
    elif(val == ToothType.INCISOR_UR2_LL2.value):
        return 'Incisor Second'
    elif(val == ToothType.INCISOR_UR1_LL1.value):
        return 'Incisor First'

    elif(val == ToothType.INCISOR_UL1_LR1.value):
        return 'Incisor First'
    elif(val == ToothType.INCISOR_UL2_LR2.value):
        return 'Incisor Second'
    elif(val == ToothType.CANINE_UL3_LR3.value):
        return 'Canine'
    elif(val == ToothType.PREMOLAR_UL4_LR4.value):
        return 'Premolar First'
    elif(val == ToothType.PREMOLAR_UL5_LR5.value):
        return 'Premolar Second'
    elif(val == ToothType.MOLAR_UL6_LR6.value):
        return 'Molar First'
    elif(val == ToothType.MOLAR_UL7_LR7.value):
        return 'Molar Second'
    
    elif(val == ToothType.DELETED.value):
        return 'Delete'
        
    

def map_landmark_val_to_name(val):
    # val = math.floor(val)
    if(val == LandmarkType.MESIAL.value):
        return "Mesial"
    elif (val == LandmarkType.DISTAL.value):
        return "Distal"
    elif (val == LandmarkType.BUCCAL_OR_LABIAL.value):
        return "Buccal/Labial"
    elif (val == LandmarkType.LINGUAL_OR_PALATAL.value):
        return "Lingual/Palatal"
    elif (val == LandmarkType.PIT.value):
        return "Pit"
    elif (val == LandmarkType.CUSP.value):
        return "Cusp"
    elif (val == LandmarkType.CUSP_OUT.value):
        return "Cusp Buccal/Labial"
    elif (val == LandmarkType.CUSP_IN.value):
        return "Cusp Lingual/Palatal"
    elif (val == LandmarkType.CUSP_OUT_MESIAL.value):
        return "Cusp Buccal/Labial Mesial"
    elif (val == LandmarkType.CUSP_OUT_MIDDLE.value):
        return "Cusp Buccal/Labial Middle"
    elif (val == LandmarkType.CUSP_OUT_DISTAL.value):
        return "Cusp Buccal/Labial Distal"
    elif (val == LandmarkType.CUSP_IN_MESIAL.value):
        return "Cusp Lingual/Palatal Mesial"
    elif (val == LandmarkType.CUSP_IN_DISTAL.value):
        return "Cusp Lingual/Palatal Distal"

def map_arch_val_to_name(val):
    if(val == ArchType.LOWER.value):
        return "Mandibular"    
    else:
        return "Maximillar"

def convert_landmark_val_to_name(val):
    return map_landmark_val_to_name(val)

def convert_tooth_val_to_name(val):
    return map_tooth_val_to_name(val)

def convert_arch_val_to_name(val):
    return map_arch_val_to_name(val)
