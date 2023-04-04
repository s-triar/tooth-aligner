from vedo import *
c1 = Cube().alpha(0.5)
t1 = Point(c1.points()[0]).c('green')
c2 = c1.clone().c('violet').alpha(0.5) # copy of c1
v = vector(0.5,0,0)
p = vector(1,0,0)  # axis passes through this point
p = c1.centerOfMass()
c2.rotate(90, axis=v, point=p)
t2 = Point(c2.points()[0]).c('pink')
c3 = c2.clone().c('blue4').alpha(0.5)
v2 = vector(0,1,0.2)
c3.rotate(90,axis=v2,point=p)
t3 = Point(c3.points()[0]).c('blue')
l = Line(-v+p, v+p).lw(3).c('red')
l2 = Line(-v2+p, v2+p).lw(3).c('blue')

cq1 = Cube().alpha(0.5)
tq1 = Point(cq1.points()[0]).c('green')
cq2 = cq1.clone().c('violet').alpha(0.5) # copy of c1
vq = vector(0,1,0.2)
pq = vector(1,0,0)  # axis passes through this point
pq = cq1.centerOfMass()
cq2.rotate(90, axis=v, point=p)
tq2 = Point(cq2.points()[0]).c('pink')
cq3 = cq2.clone().c('blue4').alpha(0.5)
vq2 = vector(0.5,0,0)
cq3.rotate(90,axis=vq2,point=pq)
tq3 = Point(cq3.points()[0]).c('blue')
lq = Line(-vq+pq, vq+pq).lw(3).c('red')
lq2 = Line(-vq2+pq, vq2+pq).lw(3).c('blue')
plt = Plotter(N=2)
show(c1, l, c2,l2, c3,t1,t2,t3, axes=1,at=0)
show(cq1, lq, cq2,lq2, cq3,tq1,tq2,tq3, axes=1,at=1)
plt.interactive()