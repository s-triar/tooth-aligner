# import sys
# from PyQt5 import Qt
# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# from vedo import Plotter, Picture, Text2D, printc

# class MainWindow(Qt.QMainWindow):

#     def __init__(self, parent=None):

#         Qt.QMainWindow.__init__(self, parent)
#         self.frame = Qt.QFrame()
#         self.layout = Qt.QVBoxLayout()
#         self.vtkWidget = QVTKRenderWindowInteractor(self.frame)

#         # Create vedo renderer and add objects and callbacks
#         self.plt = Plotter(qtWidget=self.vtkWidget)
#         self.cbid = self.plt.addCallback("key press", self.onKeypress)
#         self.imgActor = Picture("https://icatcare.org/app/uploads/2018/07/Helping-your-new-cat-or-kitten-settle-in-1.png")
#         self.text2d = Text2D("Use slider to change contrast")

#         self.slider = Qt.QSlider(1)
#         self.slider.valueChanged.connect(self.onSlider)
#         self.layout.addWidget(self.vtkWidget)
#         self.layout.addWidget(self.slider)

#         self.frame.setLayout(self.layout)
#         self.setCentralWidget(self.frame)
#         self.plt.show(self.imgActor, self.text2d, mode='image') # build the vedo rendering
#         self.show()                                            # show the Qt Window


#     def onSlider(self, value):
#         self.imgActor.window(value*10) # change image contrast
#         self.text2d.text(f"window level is now: {value*10}")
#         self.plt.render()

#     def onKeypress(self, evt):
#         printc("You have pressed key:", evt.keyPressed, c='b')
#         if evt.keyPressed=='q':
#             self.plt.close()
#             self.vtkWidget.close()
#             exit()

#     def onClose(self):
#         self.vtkWidget.close()

# if __name__ == "__main__":
#     app = Qt.QApplication(sys.argv)
#     window = MainWindow()
#     app.aboutToQuit.connect(window.onClose)
#     app.exec_()

# import numpy as np

# a = [4,65,7,7,6,6,33,]
# print(a)
# import os
# from pathlib import Path
# import glob
# path = "D:/NyeMan/KULIAH S2/Thesis/tooth-aligner/saved_landmark_predict_manual/AE/AE.json"
# c=path.split(os.altsep)
# a=os.altsep.join(c[:-1])
# for step_folder in glob.glob(a+"/*"):
#     if(".json" not in step_folder):
#         index = step_folder.split("step_")[-1]
#         for model in glob.glob(step_folder+"/*.vtp"):
#             print(model)
#             # load model
#         for ld in glob.glob(step_folder+"/*.csv"):
#             print(ld)
#             # load landmark

"""Draw the shadows and trailing lines of 2 planes. Not really
a simulation.. just a way to illustrate how to move objects around!"""
"""Simulation of a block connected to a spring in a viscous medium"""
from vedo import *

pts = [[0,0,0],
       [0.5,0.6,0.8],
       [1,1,1]]
gpts = Points(pts, r=10).c('green',0.5)

# Create a spline where the final points are more dense (easing)
line = Spline(pts, easing="OutCubic", res=100)

vpts = line.clone().shift(0,0.1,0) # a dotted copy

# Calculate positions as a fraction of the length of the line,
# being x=0 the first point and x=1 the last point.
# This corresponds to an imaginary point that travels along the line
# at constant speed:
equi_pts = Points([line.eval(x) for x in np.arange(0,1, 0.1)]).c('blue')

redpt = Point(r=25).c('red')
plt = show(vpts, gpts, line, redpt, equi_pts, axes=1, interactive=0)
# Animation
for i in range(len(line.points())):
    x = line.points(i)
    redpt.pos(x) # assign the new position
    plt.render()
plt.interactive().close()