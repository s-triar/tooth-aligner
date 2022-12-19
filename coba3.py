# from vedo import *


# def rotate(event):
#     print(plt.actors)
#     for actor in plt.actors:
#         actor.rotateX(2.5, False, (0,0,0))

# c1 = Cube()
# c2 = c1.clone().c('violet').alpha(0.5) # copy of c1
# v = vector(0.2,1,0)
# p = vector(1,0,0)  # axis passes through this point
# c2.rotate(90, axis=v, point=p)

# T = c2.getTransform()
# print(T)
# plt = Plotter(axes=1)
# plt.addCallback( "RightButtonPressEvent", rotate)
# plt.show(c1.wireframe().lw(3), c2, axes=1) # press a during interaction then q
# plt.interactor.AddObserver("LeftButtonPressEvent", self._mouseleft)

# from vedo import *

# c1 = Box((0.2,0,0.1),2,1,2,alpha=0.6)
# c2 = Box((0.2,0,0.1),2,1,2,alpha=0.6)
# c1= Mesh([c1.points(),c1.faces()],c='blue',alpha=0.6)
# c2=Mesh([c2.points(),c2.faces()])
# v = vector(0.2,1,0)
# p = vector(1,0,0)  # axis passes through this point
# pts = c2.points()
# # pts[0]=[0.2,0.3,0]
# c2.points(pts)
# ctr=c2.centerOfMass()
# c2.rotateZ(20, False, ctr)
# t1 = c1.getTransform()

# t2 = c2.getTransform()

# # c1.applyTransform(t2)



# show(c1,c2, axes=1) # press a during interaction then q


# from vedo import *

# cone = Cone() #.x(100) #Cone(r=0.5, res=50)

# print(cone.points(transformed=True)[:10])
# print(cone.points(transformed=False)[:10])
# print(cone.getTransform())

# show(cone, axes=1)


# from vedo import dataurl, Plotter, Mesh, Sphere

# msh1 = Mesh(dataurl+'motor.byu')
# cutmesh = Sphere().y(-0.4).scale(0.4).alpha(0.4)

# msh2 = msh1.clone().cutWithMesh(cutmesh)
# redcap = msh2.cap(returnCap=False).color("r4")


# plt = Plotter(N=2, axes=1)
# plt.at(0).show(msh1, cutmesh)
# plt.at(1).show(msh2, redcap, viewup="z")
# plt.interactive().close()


r={}
r[1]=