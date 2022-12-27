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


from vedo import Plotter, load, Point, Sphere, Circle, Line, Points
import os
import numpy as np
from utility.calculation import find_new_point_in_a_line_with_new_distance,find_distance_between_two_points,find_distance_between_a_point_and_a_line,closest_line_seg_line_seg
from utility.splineku import SplineKu
l = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo LowerJawScan _d_predicted_refined.vtp')
u = load('D:\\NyeMan\\KULIAH S2\\Thesis\\MeshSegNet-master\\MeshSegNet-master\\down_segement_refine_manual\\gak bisa karena gigi kurang\\Sulaiman Triarjo UpperJawScan _d_predicted_refined.vtp')

# a = np.array([3,6,4.2])
# b = np.array([8.4,7.1,9])
# dstp = find_distance_between_two_points(a,b)
# c = find_new_point_in_a_line_with_new_distance(b,a ,dstp+10)
# print(c)
# ap=Point(a).c('black')
# bp=Point(b).c('blue')
# cp = Point(np.array(c)).c('green')
# cr = Sphere((2,2,2),r=3)
# cr2 = Sphere((4,4,4),r=2.5).c('yellow')
# ll = Line(a,c,res=1000)
# lly = Line([0,8,2],[0,9,4],res=1000)
# gg = cr2.clone().intersectWith(cr)
# ff = gg.geodesic(a,c)
# # yy = lly.geodesic(a,c)
# pl1, pl2 = closest_line_seg_line_seg(np.array([[0,8,2],[0,9,4]]), np.array([a,c]))
# print(ff.points())
# tts = Points(ff.points(),r=10,c='orange')
# for tp in ff.points():
#     tg =find_distance_between_a_point_and_a_line(tp,[a,c])
#     print(tg)
# print('=========')

# yyp = Point(pl1,c='red')
# yyp2 = Point(pl2,c='violet')

# # hh = cr.collideWith(cr2)
plt = Plotter(axes=1)
plt.show(l,u)
# plt.show(ap,bp,cp,gg,ll,ff,tts, lly,yyp,yyp2)

# a = [0,0,0]
# b=[7,1,1]
# c=[3.3,5,9]

# spl = SplineKu([a,c,b],degree=2)
# plt = Plotter(axes=1)
# plt.show(spl)