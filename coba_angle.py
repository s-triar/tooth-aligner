import numpy as np
import math

def get_angle_from_2_2d_lines(lineA, lineB, is_return_degree=False):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    print(vA,vB)
    # Get dot prod
    dot_prod = np.dot(vA, vB)
    print(dot_prod)
    # Get magnitudes
    magA = np.dot(vA, vA)**0.5
    magB = np.dot(vB, vB)**0.5
    print(magA,magB)
    # Get cosine value
    cos_ = dot_prod/magA/magB
    print(cos_)
    # Get angle in radians and then convert to degrees
    angle = math.acos(cos_)
    if(is_return_degree==True):
        return math.degrees(angle) #0-180
    else:
        return angle
    
def get_angle_from_2_2d_lines2(lineA, lineB, is_return_degree=False):
    dimension = len(lineA[0])
    vA = [lineA[1][i] - lineA[0][i] for i in range(dimension)]
    vB = [lineB[1][i] - lineB[0][i] for i in range(dimension)]
    print(vA,vB)
    
    dot_prod = sum([vA[i]*vB[i] for i in range(dimension)])
    print(dot_prod)
    
    magA = math.sqrt(sum([vA[i]**2 for i in range(dimension)]))
    magB = math.sqrt(sum([vB[i]**2 for i in range(dimension)]))
    print(magA,magB)
    
    cos_ = dot_prod/(magA*magB)
    print(cos_)
    angle = math.acos(cos_)
    if( is_return_degree):
        return math.degrees(angle)   
    return angle
    
def get_angle_from_2_2d_lines3(lineA, lineB, is_return_degree=False):
    dimension = len(lineA[0])
    vA = [lineA[1][i] - lineA[0][i] for i in range(dimension)]
    vB = [lineB[1][i] - lineB[0][i] for i in range(dimension)]
    print(vA,vB)
    mm1 = (lineA[1][0]-lineA[0][0])
    mm2 = (lineB[1][0]-lineB[0][0])
    m1 = (lineA[1][1]-lineA[0][1]) / (mm1 if mm1 != 0 else 0.000000001)
    m2 = (lineB[1][1]-lineB[0][1]) / (mm2 if mm2 != 0 else 0.000000001)
    print(m1,m2)
    tantheta = (m2-m1)/(1+(m2*m1))
    print(tantheta)
    angle = math.atan(tantheta)
    if( is_return_degree):
        return abs(math.degrees(angle))
    return abs(angle)

line1 = [
    [-5,3],
    [4,-1]
]

line2 = [
    [ 1,1],
    [1,4],
    
   
    
]

r = get_angle_from_2_2d_lines(line1,line2,True)

r2 = get_angle_from_2_2d_lines2(line1,line2,True)

r3 = get_angle_from_2_2d_lines3(line1,line2,True)

print(r,r2,r3)


g = [47,9,5,6,21,9]
t = np.argmin(g)
print(t)