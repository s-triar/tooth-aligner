from vedo import load,  Plotter
from optimization.de_optimization5 import de_rotation_and_moving
from utility.arch import Arch
from constant.enums import ArchType

u = load('C:\\Users\\intel\\Downloads\\awal-DATA-GIGI-CLEAN - labelled\\12. KEC\\12. KEC\\KEC_UPPER.vtp')
l = load('C:\\Users\\intel\\Downloads\\awal-DATA-GIGI-CLEAN - labelled\\12. KEC\\12. KEC\\KEC_LOWER.vtp')

m_u = Arch(arch_type=ArchType.UPPER.value, mesh=u)
m_l = Arch(arch_type=ArchType.LOWER.value, mesh=l)

chromosomes=[]
for i in range(10):
    temp = [1.5,1.5,1.5,0,0,0]*14*2
    chromosomes.append(temp)
models = [m_u,m_l]
for chromosome in chromosomes:
    for i in range(len(models)):
        models[i] = de_rotation_and_moving(models[i], chromosome[(i * (14 * 6)):(i + 1) * (14 * 6)])  # 6 chromosome per tooth

plt = Plotter()
plt.add(models[0].mesh, models[1].mesh)
plt.show()
