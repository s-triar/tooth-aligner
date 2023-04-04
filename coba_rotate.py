from vedo import *
c1 = Cube().alpha(0.5)

t1 = Point(c1.points()[0]).c('green')

c2 = c1.clone().c('violet').alpha(0.5) # copy of c1
v = vector(0.2,1,0)
p = vector(1,0,0)  # axis passes through this point
p = c1.centerOfMass()
c2.rotate(90, axis=v, point=p)
t2 = Point(c2.points()[0]).c('pink')

c3 = c2.clone().c('blue4').alpha(0.5)
v2 = vector(0.2,0.4,0.8)
c3.rotate(90,axis=v2,point=p)
t3 = Point(c3.points()[0]).c('blue')

l = Line(-v+p, v+p).lw(3).c('red')
l2 = Line(-v2+p, v2+p).lw(3).c('blue')
show(c1, l, c2,l2, c3,t1,t2,t3, axes=1).close()