from matplotlib import axis
from pyparsing import col
from vedo import Line, Points
import numpy as np
import vedo
from scipy.interpolate import splprep, splev
from scipy.optimize import fmin
class SplineKu(Line):
    """
    Find the B-Spline curve through a set of points. This curve does not necessarly
    pass exactly through all the input points. Needs to import `scipy`.

    Return an ``Mesh`` object.

    :param float smooth: smoothing factor.

        - 0 = interpolate points exactly [default].
        - 1 = average point positions.

    :param int degree: degree of the spline (1<degree<5)
    :param str easing: control sensity of points along the spline.

        Available options are
        [InSine, OutSine, Sine, InQuad, OutQuad, InCubic, OutCubic,
        InQuart, OutQuart, InCirc, OutCirc].
        Can be used to create animations (move objects at varying speed).
        See e.g.: https://easings.net

    :param int res: number of points on the spline

    See also: ``CSpline`` and ``KSpline``.
    """
    def __init__(self, points,
                 smooth=0,
                 degree=2,
                 closed=False,
                 s=None,
                 res=None,
                 easing="",
                 ):

        # temp = np.array(points)
        if isinstance(points, Points):
            points = points.points()

        if len(points[0]) == 2: # make it 3d
            points = np.c_[np.array(points), np.zeros(len(points))]

        per = 0
        if closed:
            points = np.append(points, [points[0]], axis=0)
            per = 1

        if res is None:
            res = len(points)*10
            
        self.res_spline = res
        points = np.array(points)

        minx, miny, minz = np.min(points, axis=0)
        maxx, maxy, maxz = np.max(points, axis=0)
        maxb = max(maxx - minx, maxy - miny, maxz - minz)
        smooth *= maxb / 2  # must be in absolute units

        x = np.linspace(0, 1, res)
        if easing:
            if easing=="InSine":
                x = 1 - np.cos((x * np.pi) / 2)
            elif easing=="OutSine":
                x = np.sin((x * np.pi) / 2)
            elif easing=="Sine":
                x = -(np.cos(np.pi * x) - 1) / 2
            elif easing=="InQuad":
                x = x*x
            elif easing=="OutQuad":
                x = 1 - (1 - x) * (1 - x)
            elif easing=="InCubic":
                x = x*x
            elif easing=="OutCubic":
                x = 1 - np.power(1 - x, 3)
            elif easing=="InQuart":
                x = x * x * x * x
            elif easing=="OutQuart":
                x = 1 - np.power(1 - x, 4)
            elif easing=="InCirc":
                x = 1 - np.sqrt(1 - np.power(x, 2))
            elif easing=="OutCirc":
                x = np.sqrt(1 - np.power(x - 1, 2))
            else:
                vedo.logger.error(f"unkown ease mode {easing}")

        # find the knots
        self.tckp, self.uu = splprep(points.T, task=0, s=smooth if s==None else s, k=degree, per=per)
        # (self.tckp, self.uu) = splprep(np.transpose(temp), s=0, k=3)
        
        # evaluate spLine, including interpolated points:
        xnew, ynew, znew = splev(x, self.tckp)

        Line.__init__(self, np.c_[xnew, ynew, znew], res=res, lw=2)
        self.lighting('off')
        self.name = "SplineKu"
    
    def calculateToPoint_(self, u):
        s = np.array(splev(u, self.tckp))
        # print(s)
        self.temp_distance_to_point = s-self.point_target
        # print("u",u, self.point_target, self.temp_distance_to_point, s)
        return (self.temp_distance_to_point**2).sum()
    
    def closestPoint(self,point, return_u=False):
        self.temp_distance_to_point=0
        self.point_target=np.array(point).reshape(3,1)
        # self.point_target=point
        closestu = fmin(self.calculateToPoint_, np.mean(point), disp=False)
        # print(closestu,"closestu")
        closest = np.array(splev(closestu, self.tckp)).reshape(3)
        
        if return_u==True:
            return closest, closestu
        return closest
    
    def getDistanceHalfway(self, u = 0, v = 1):
        spline = np.array(splev(np.linspace(u, v, self.res_spline), self.tckp))
        lengths = np.sqrt(np.sum(np.diff(spline.T, axis=0)**2, axis=1))
        return np.sum(lengths)
    
    def getHalwayPoint(self):
        spline = np.array(splev(np.linspace(0, 1, self.res_spline), self.tckp))
        return np.array([spline[0, self.res_spline//2],spline[1, self.res_spline//2],spline[2, self.res_spline//2]])
    
    # def getPoints(self, pts):
    #     collection=[]
    #     for pt in pts:
    #         # p = np.array(p).reshape(3,1)
    #         # self.point_target = p
    #         closest, closestu = self.closestPoint(pt, return_u=True)
    #         if(closestu[0]<0.5):
    #             print(closestu)
    #             collection.append(closest)
    #     return collection