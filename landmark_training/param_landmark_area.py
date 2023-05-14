from constant.enums import LandmarkType, ArchType, ToothType

candidate_definition = {
    ArchType.UPPER.value: {
        ToothType.INCISOR_UR1_LL1.value: {
            LandmarkType.MESIAL.value: {
                'u': [0.73, 4],
                'd': [0.12, 6],
                'r': [0.12, 8],
                'l': [0.12, True],
                'f': [0.12, 5],
                'b': [0.12, True],
            },
            LandmarkType.DISTAL.value: {
                'u': [0.73, 4],
                'd': [0.12, 6],
                'r': [0.12, 8],
                'l': [0.12, True],
                'f': [0.12, 5],
                'b': [0.12, True],
            }
        }
    }
}
