from pathlib import Path  
from dotenv import load_dotenv
import os
import enum

# from constant.enums import ArchType

class ArchType(enum.Enum):
    UPPER=1
    LOWER=2



def get_saved_path(path_model, extendsion,cur_step=None, isProject=False):
    load_dotenv()
    save_path = os.getenv("SAVE")
    c=path_model.split(os.altsep)
    file = c[-1]
    sign_jaw = os.getenv(ArchType.LOWER.name)
    if(os.getenv(ArchType.UPPER.name) in file.lower()):
        sign_jaw = os.getenv(ArchType.UPPER.name)
    file_chunk = file.split(' ')
    person = ''
    for f in file_chunk:
        if(sign_jaw in f.lower()):
            break
        if(person!=''):
            person+=" "
        person+=f
    if(isProject==False):
        return os.path.join(save_path,person,"step_"+str(cur_step),person+"_step_"+str(cur_step)+extendsion)
    else:
        return os.path.join(save_path,person,person+extendsion)
    


    
if __name__ == '__main__':
    print(ArchType.LOWER.name)
    a=r'D:/NyeMan/KULIAH S2/Thesis/MeshSegNet-master/MeshSegNet-master/down_segement_refine_manual/Gerry Sihaj LowerJawScan Cleaned 10000_d_predicted_refined a.vtp'
    g = get_saved_path(a,".csv",4,isProject=False)
    print(g)
    filepath = Path(g)  
    filepath.parent.mkdir(parents=True, exist_ok=True) 
    for i in range(1):
        print(i)