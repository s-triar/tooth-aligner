from constant.enums import ArchType

class Attachment():
    def __init__(self, mesh, name, label) -> None:
        self.mesh=mesh
        self.name = name
        self.label=label

class AttachmentModel():
    
    def __init__(self) -> None:
        self.arch={}
        self.arch[ArchType.LOWER.value]={}
        self.arch[ArchType.UPPER.value]={}
    # arch
        # lower/upper
            # step aligner
                # tooth label
    
    def add_attachment(self,arch_type,step, mesh, name, label):
        temp = Attachment(mesh,name, label)
        if step in self.arch[arch_type]:
            self.arch[arch_type][step].append(temp)
        else:
            self.arch[arch_type][step]=[temp]
    
    def copy_attachment(self, fromstep, tostep):
        for arch_type in ArchType:
            if fromstep in self.arch[arch_type.value]:
                self.arch[arch_type.value][tostep]=self.arch[arch_type.value][fromstep].copy()
            
    
    def get_attachment_on_step(self, step):
        # print('get_attachment_on_step',step, self.arch)
        res={}
        for a in self.arch:
            res[a]=None
            if step in self.arch[a]:
                res[a]=self.arch[a][step]
        return res
    
    def delete_attachment(self, arch, step, name):
        index=None
        for idx, item in enumerate(self.arch[arch][step]):
            if item.name == name:
                index = idx
                break
        if(index!=None):
            self.arch[arch][step].pop(index)
    
    def update_attachment_with_new_mesh(self, arch, step, index, mesh):
        self.arch[arch][step][index].mesh = mesh
    
    def get_arch_and_step_from_name(self, name):
        arch=None
        step=None
        for a in self.arch:
            for s in self.arch[a]:
                for att in self.arch[a][s]:
                    if(att.name ==name):
                        arch=a
                        step=s
                        break
        return arch, step
    
    def get_attachment_from_name(self, name):
        attach=None
        arch=None
        step=None
        for a in self.arch:
            for s in self.arch[a]:
                for att in self.arch[a][s]:
                    if(att.name ==name):
                        attach=att
                        arch = a
                        step=s
                        break
        return attach, arch, step
    
    def get_attachment_from_label(self, label):
        attachs=[]
        archs=[]
        steps=[]
        index_k=[]
        i=0
        j=0
        k=0
        for a in self.arch:
            for s in self.arch[a]:
                for att in self.arch[a][s]:
                    if(att.label==label):
                        attachs.append(att)
                        archs.append(a)
                        steps.append(s)
                        index_k.append(k)
                    k+=1
                j+=1
            i+=1
        return attachs, archs, steps, index_k
        