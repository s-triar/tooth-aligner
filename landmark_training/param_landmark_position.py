from constant.enums import LandmarkType, ArchType, ToothType

landmark_definition = {
    ArchType.UPPER.value: {
        ToothType.INCISOR_UR1_LL1.value: {
            LandmarkType.MESIAL.value: [0,0,0,0,0,0],
            LandmarkType.DISTAL.value: [0,0,0,0,0,0]
        }
    }
}

