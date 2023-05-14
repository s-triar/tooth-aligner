from constant.enums import LandmarkType, ArchType, ToothType

landmark_definition = {
    ArchType.UPPER.value: {
        ToothType.INCISOR_UR1_LL1.value: {
            LandmarkType.MESIAL.value: [0,0,0,0,0,0],
            LandmarkType.DISTAL.value: [0,0,0,0,0,0]
        }
    }
}

import numpy as np

# Example dictionary with conditions
conditions = {
    'condition1': 5,
    'condition2': 6,
    'condition3': 3
}

# Example array
array = np.array([1, 6, 12, 3, 8, 5])
arra1 = np.array([5,5,2,5,7,3])

def getty(arr,v):
    if(v > 5):
        return  arr[0]
    return arr[1]

arrt = [array, arra1]

# Create a dynamic condition based on the dictionary
condition = np.logical_and.reduce([
        np.logical_and(True, np.where(value < 6, True, getty(arrt, value) > value + 1))
        for value in conditions.values()
    ]
)

# Apply the condition to the array
result = array[condition]
print(result)