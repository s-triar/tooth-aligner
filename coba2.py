from vedo import Plotter, load
from utility.colors import convert_label_to_color, convert_labels_to_colors
paths_upper=[
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_UPPER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._UPPER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_UPPER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_UPPER.vtp",
]
paths_ld_upper = [
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_UPPER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._UPPER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_UPPER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_UPPER.csv",
]
paths_lower = [
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_LOWER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._LOWER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_LOWER.vtp",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_LOWER.vtp",
]
paths_ld_lower = [
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\1 MNF\\MNF_LOWER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\4. SN\\SN._LOWER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\7. GSF\\GSF_LOWER.csv",
    "D:\\NyeMan\\KULIAH S2\\Thesis\\3Shape new-20220223T024758Z-001\\fix\\8. UR\\UR_LOWER.csv",
]

plt = Plotter(N=4)
for i in range(len(paths_upper)):
    mesh = load(paths_upper[i])
    colors = convert_labels_to_colors(mesh.celldata['Label'])
    mesh.celldata['Color'] = colors
    mesh.celldata.select('Color')
    plt.add(mesh, at=i)
plt.show()
plt.interactive()