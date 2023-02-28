import numpy as np
import yt
import loadBuffer

path = "C:/Users/sabas/Documents/NJIT/CSTR/flarecs-id.0035.vtk"
lb = loadBuffer.loadBuffer()
ds = yt.load(path)

# ds1 = lb.dsl(ds, 1)
# slc1 = yt.SlicePlot(ds1, "z", ("gas", "density"))
# slc1.save("yt_ss1")

ds2 = lb.dsl(ds, 2)
slc2 = yt.SlicePlot(ds2, "z", ("gas", "density"))
slc2.save("yt_ss2")

ds3 = lb.dsl(ds, 3)
slc3 = yt.SlicePlot(ds3, "z", ("gas", "density"))
slc3.save("yt_ss3")


