from constant.enums import LandmarkType, ArchType, ToothType
import pandas as pd
landmark_definition = {}

landmark_def_path = "ld_saved_de.txt"

def import_landmark_def():
    df = pd.read_csv(landmark_def_path, encoding='utf-8', header=None)
    for index, row in df.iterrows():
        idx_arch = 1
        idx_tooth = 3
        idx_landmark = 5
        idx_coord = 7
        arch = int(row[idx_arch])
        tooth = int(row[idx_tooth])
        landmark = int(row[idx_landmark])
        coordinate=str(row[idx_coord])
        coors = []
        coord = coordinate.split("|")
        for c in coord:
            coors.append(float(c))

        if arch in landmark_definition:
            if tooth in landmark_definition[arch]:
                if landmark in landmark_definition[arch][tooth]:
                    landmark_definition[arch][tooth][landmark] = coors
                else:
                    landmark_definition[arch][tooth][landmark] = {}
                    landmark_definition[arch][tooth][landmark] = coors
            else:
                landmark_definition[arch][tooth] = {}
                landmark_definition[arch][tooth][landmark] = coors
        else:
            landmark_definition[arch] = {}
            landmark_definition[arch][tooth] = {}
            landmark_definition[arch][tooth][landmark] = coors
def get_landmark_definition():
    if landmark_definition != {}:
        return landmark_definition
    else:
        import_landmark_def()
        return landmark_definition

if __name__ == '__main__':
    a = get_landmark_definition()
    print(a)