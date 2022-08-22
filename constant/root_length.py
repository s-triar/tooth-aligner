from constant.enums import ToothType, ArchType

class RootLength:
    archs={
        ArchType.LOWER.value:{
            ToothType.INCISOR_UL1_LR1.value:12.5,
            ToothType.INCISOR_UR1_LL1.value:12.5,
            ToothType.INCISOR_UL2_LR2.value:14,
            ToothType.INCISOR_UR2_LL2.value:14,
            ToothType.CANINE_UL3_LR3.value:16,
            ToothType.CANINE_UR3_LL3.value:16,
            ToothType.PREMOLAR_UL4_LR4.value:14,
            ToothType.PREMOLAR_UR4_LL4.value:14,
            ToothType.PREMOLAR_UL5_LR5.value:14.5,
            ToothType.PREMOLAR_UR5_LL5.value:14.5,
            ToothType.MOLAR_UL6_LR6.value:14,
            ToothType.MOLAR_UR6_LL6.value:14,
            ToothType.MOLAR_UL7_LR7.value:13,
            ToothType.MOLAR_UR7_LL7.value:13,
        },
        ArchType.UPPER.value:{
            ToothType.INCISOR_UL1_LR1.value:13,
            ToothType.INCISOR_UR1_LL1.value:13,
            ToothType.INCISOR_UL2_LR2.value:13,
            ToothType.INCISOR_UR2_LL2.value:13,
            ToothType.CANINE_UL3_LR3.value:17,
            ToothType.CANINE_UR3_LL3.value:17,
            ToothType.PREMOLAR_UL4_LR4.value:14,
            ToothType.PREMOLAR_UR4_LL4.value:14,
            ToothType.PREMOLAR_UL5_LR5.value:14,
            ToothType.PREMOLAR_UR5_LL5.value:14,
            ToothType.MOLAR_UL6_LR6.value:12.9,
            ToothType.MOLAR_UR6_LL6.value:12.9,
            ToothType.MOLAR_UL7_LR7.value:11,
            ToothType.MOLAR_UR7_LL7.value:11,
        }
    }
    