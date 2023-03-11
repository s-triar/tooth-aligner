from constant.enums import ToothType

def get_tooth_labels():
    tooth_labels={
        "anterior":[
            ToothType.INCISOR_UL1_LR1.value,
            ToothType.INCISOR_UL2_LR2.value,
            ToothType.INCISOR_UR1_LL1.value,
            ToothType.INCISOR_UR2_LL2.value,
        ],
        "canine":[
            ToothType.CANINE_UL3_LR3.value,
            ToothType.CANINE_UR3_LL3.value,
        ],
        "posterior":[
            ToothType.MOLAR_UL7_LR7.value,
            ToothType.MOLAR_UL6_LR6.value,
            ToothType.PREMOLAR_UL5_LR5.value,
            ToothType.PREMOLAR_UL4_LR4.value,
            ToothType.PREMOLAR_UR4_LL4.value,
            ToothType.PREMOLAR_UR5_LL5.value,
            ToothType.MOLAR_UR6_LL6.value,
            ToothType.MOLAR_UR7_LL7.value
        ]
    }
    return tooth_labels

def get_tooth_label_flat():
    return [
        ToothType.INCISOR_UL1_LR1.value,
        ToothType.INCISOR_UL2_LR2.value,
        ToothType.INCISOR_UR1_LL1.value,
        ToothType.INCISOR_UR2_LL2.value,
        ToothType.CANINE_UL3_LR3.value,
        ToothType.CANINE_UR3_LL3.value,
        ToothType.MOLAR_UL7_LR7.value,
        ToothType.MOLAR_UL6_LR6.value,
        ToothType.PREMOLAR_UL5_LR5.value,
        ToothType.PREMOLAR_UL4_LR4.value,
        ToothType.PREMOLAR_UR4_LL4.value,
        ToothType.PREMOLAR_UR5_LL5.value,
        ToothType.MOLAR_UR6_LL6.value,
        ToothType.MOLAR_UR7_LL7.value
    ]