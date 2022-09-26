# from vedo import *

# c1 = Cube()
# c2 = c1.clone().c('violet').alpha(0.5) # copy of c1
# v = vector(0.2,1,0)
# p = vector(1,0,0)  # axis passes through this point
# c2.rotate(90, axis=v, point=p)

# T = c2.getTransform()
# print(T)

# show(c1.wireframe().lw(3), c2, axes=1) # press a during interaction then q

# T = c2.getTransform()
# print(T)

# interactive()

from vedo import *

c1 = Box((0.2,0,0.1),2,1,2,alpha=0.6)
c2 = Box((0.2,0,0.1),2,1,2,alpha=0.6)
c1= Mesh([c1.points(),c1.faces()],c='blue',alpha=0.6)
c2=Mesh([c2.points(),c2.faces()])
v = vector(0.2,1,0)
p = vector(1,0,0)  # axis passes through this point
pts = c2.points()
# pts[0]=[0.2,0.3,0]
c2.points(pts)
ctr=c2.centerOfMass()
c2.rotateZ(20, False, ctr)
t1 = c1.getTransform()

t2 = c2.getTransform()

# c1.applyTransform(t2)



show(c1,c2, axes=1) # press a during interaction then q
