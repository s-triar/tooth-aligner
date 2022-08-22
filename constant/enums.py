import enum

class PanelMode(enum.Enum):
    ROTATION=1
    BOLTON=2
    PONT=3
    KORKHAUS=4
    LANDMARK=5
    SEGMENTATION=6

class LandmarkType(enum.Enum):
    MESIAL=1
    DISTAL=2
    BUCCAL_OR_LABIAL=3
    LINGUAL_OR_PALATAL=4
    PIT=5
    CUSP=6
    CUSP_OUT=7
    CUSP_IN=8
    CUSP_OUT_MESIAL=9
    CUSP_OUT_MIDDLE=10
    CUSP_OUT_DISTAL=11
    CUSP_IN_MESIAL=12
    CUSP_IN_DISTAL=13

class ArchType(enum.Enum):
    UPPER=1
    LOWER=2
    
class ToothType(enum.Enum):
    
    GINGIVA=0
    MOLAR_UR7_LL7=1
    MOLAR_UR6_LL6=2
    PREMOLAR_UR5_LL5=3
    PREMOLAR_UR4_LL4=4
    CANINE_UR3_LL3=5
    INCISOR_UR2_LL2=6
    INCISOR_UR1_LL1=7

    INCISOR_UL1_LR1=8
    INCISOR_UL2_LR2=9
    CANINE_UL3_LR3=10
    PREMOLAR_UL4_LR4=11
    PREMOLAR_UL5_LR5=12
    MOLAR_UL6_LR6=13
    MOLAR_UL7_LR7=14
    
    DELETED=15
    
class LandmarkDefinition:
    archs={}
    archs[ArchType.LOWER.value]={}
    #7
    archs[ArchType.LOWER.value][ToothType.INCISOR_UR1_LL1.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #8
    archs[ArchType.LOWER.value][ToothType.INCISOR_UL1_LR1.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #6
    archs[ArchType.LOWER.value][ToothType.INCISOR_UR2_LL2.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #6
    archs[ArchType.LOWER.value][ToothType.INCISOR_UL2_LR2.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #5
    archs[ArchType.LOWER.value][ToothType.CANINE_UR3_LL3.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #10
    archs[ArchType.LOWER.value][ToothType.CANINE_UL3_LR3.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    
    #4
    archs[ArchType.LOWER.value][ToothType.PREMOLAR_UR4_LL4.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
     #11
    archs[ArchType.LOWER.value][ToothType.PREMOLAR_UL4_LR4.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
    
    #3
    archs[ArchType.LOWER.value][ToothType.PREMOLAR_UR5_LL5.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        # LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
    
    #12
    archs[ArchType.LOWER.value][ToothType.PREMOLAR_UL5_LR5.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        # LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
    
    #2
    archs[ArchType.LOWER.value][ToothType.MOLAR_UR6_LL6.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    #13
    archs[ArchType.LOWER.value][ToothType.MOLAR_UL6_LR6.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    #1
    archs[ArchType.LOWER.value][ToothType.MOLAR_UR7_LL7.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        ]
    #14
    archs[ArchType.LOWER.value][ToothType.MOLAR_UL7_LR7.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        ]
    
    
    archs[ArchType.UPPER.value]={}
    #7
    archs[ArchType.UPPER.value][ToothType.INCISOR_UR1_LL1.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #8
    archs[ArchType.UPPER.value][ToothType.INCISOR_UL1_LR1.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #6
    archs[ArchType.UPPER.value][ToothType.INCISOR_UR2_LL2.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #6
    archs[ArchType.UPPER.value][ToothType.INCISOR_UL2_LR2.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #5
    archs[ArchType.UPPER.value][ToothType.CANINE_UR3_LL3.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    #10
    archs[ArchType.UPPER.value][ToothType.CANINE_UL3_LR3.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.CUSP.value,
        ]
    
    #4
    archs[ArchType.UPPER.value][ToothType.PREMOLAR_UR4_LL4.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
     #11
    archs[ArchType.UPPER.value][ToothType.PREMOLAR_UL4_LR4.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        ]
    
    #3
    archs[ArchType.UPPER.value][ToothType.PREMOLAR_UR5_LL5.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        # LandmarkType.CUSP_IN_MESIAL.value,
        # LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        # LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    
    #12
    archs[ArchType.UPPER.value][ToothType.PREMOLAR_UL5_LR5.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        # LandmarkType.CUSP_IN_MESIAL.value,
        # LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_IN.value,
        LandmarkType.CUSP_OUT.value
        # LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    
    #2
    archs[ArchType.UPPER.value][ToothType.MOLAR_UR6_LL6.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        # LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    #13
    archs[ArchType.UPPER.value][ToothType.MOLAR_UL6_LR6.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        # LandmarkType.CUSP_OUT_MIDDLE.value,
        ]
    #1
    archs[ArchType.UPPER.value][ToothType.MOLAR_UR7_LL7.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        ]
    #14
    archs[ArchType.UPPER.value][ToothType.MOLAR_UL7_LR7.value]=[
        LandmarkType.MESIAL.value,
        LandmarkType.DISTAL.value,
        LandmarkType.BUCCAL_OR_LABIAL.value,
        LandmarkType.LINGUAL_OR_PALATAL.value,
        LandmarkType.PIT.value,
        LandmarkType.CUSP_IN_MESIAL.value,
        LandmarkType.CUSP_IN_DISTAL.value,
        LandmarkType.CUSP_OUT_MESIAL.value,
        LandmarkType.CUSP_OUT_DISTAL.value,
        ]
    

    