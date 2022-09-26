from constant.enums import ArchType
from utility.arch import Arch


# msh2 = msh1.clone().cutWithMesh(cutmesh)
# redcap = msh2.cap(returnCap=True).color("green")

def reset_bite_contact(self):
    up_model = self.models[Arch._get_index_arch_type(ArchType.UPPER.value)]
    low_model = self.models[Arch._get_index_arch_type(ArchType.LOWER.value)]
    
    up_model.mesh.alpha(1)
    low_model.mesh.alpha(1)

def get_bite_contact(self):
    up_model = self.models[Arch._get_index_arch_type(ArchType.UPPER.value)]
    low_model = self.models[Arch._get_index_arch_type(ArchType.LOWER.value)]
    
    bite_up_low = up_model.mesh.clone().cutWithMesh(low_model.mesh.clone())
    bite_low_up = low_model.mesh.clone().cutWithMesh(up_model.mesh.clone())
    
    cap_bite_up_low = bite_up_low.cap(returnCap=True).color("r4")
    cap_bite_low_up = bite_low_up.cap(returnCap=True).color("r4")
    
    up_model.mesh.alpha(0.5)
    low_model.mesh.alpha(0.5)
    
    return cap_bite_up_low, cap_bite_low_up
    
    