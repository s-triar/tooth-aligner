from controller.landmarking_controller import draw_eigen_vec
from utility.calculation import get_eigen_flat
import numpy as np

if __name__ == '__main__':
    max =np.array([
        [ 26.475197 , -12.104838 ,  -9.891745 ],
        [ -7.1870623,  -3.1671603,  30.865192 ],
        [-14.864996 ,  -2.701504 ,  29.148333 ],
        [-37.09614  ,  -7.4188924, -19.791348 ],
        ])
    
    man=np.array([
        [-34.02611 ,    -8.755888  , -18.94108   ],
        [-10.483309,    -0.04435403,  22.715569  ],
        [ -5.191966,    -0.7876815 ,  24.438826  ],
        [ 27.147053,   -12.0584755 ,  -8.790311  ],
        ])

    mean = np.mean(man)
    print("mean", mean)
    man = man/mean
    
    outp = np.array([26.475197 , -12.104838 ,  -9.891745])
    # outp = np.array([-34.02611 ,    -8.755888  , -18.94108])
    # max[:,[2,0]] = max[:,[0,2]]
    
    
    from vedo import Mesh, Plotter, Point
    
    a = Mesh([man,[[0,1,2,3]]])
    eigen_val, eigen_vec = get_eigen_flat(man)
    print(eigen_val)
    print(eigen_vec)
    eigen_draw = draw_eigen_vec(eigen_vec, a.centerOfMass())
    
    outp_tr = np.transpose(outp)
    
    outp_tr = np.matmul([[0,0,0],[0,0,0],eigen_vec[2]], outp_tr)
    # outp_tr = np.matmul(eigen_vec, outp_tr)
    outp_tr = np.transpose(outp_tr)
    
    outp_p = Point(outp)
    outp_ptr = Point(outp_tr, c='k3')
    
    plt = Plotter(axes=1)
    plt.show(a, eigen_draw, outp_p,outp_ptr)