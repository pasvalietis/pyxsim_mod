import numpy as np

import yt

odim = [580, 577, 289]  # x,y,z dimensions of original vtk file
ds = yt.load("flarecs-id.0035.vtk")  # loads full vtk file

# ds = yt.load("flarecs-id.0035.vtk", nprocs=8)
# ds = yt.load("C:/Users/sabas/Documents/Paraview Extracts/subsampling_3.vtk")

# for i in sorted(ds.field_list):
#   print(i)

dd = ds.all_data()  # data structure containing all raw data (flattened)
gas_density = dd["gas", "density"]  # data structure containing flattened density data
# ath_density = dd["athena", "density"]

print()
print("Gas Density Data:")
print(gas_density)
# print(ath_density)

print()
densData = np.array(gas_density)  # loading the flattened density data into a numpy array
print("Shape of numpy array:")
print(densData.shape)
cells = odim[0] * odim[1] * odim[2]
print("Number of predicted cells:")
print(cells)

print()
ss2 = densData[0::2]  # subsampling the flattened density data by 2
print("Shape of sub-sampled numpy array:")
print(ss2.shape)

# ss2_struct = np.reshape(ss2, (odim[0]/2, odim[1]/2, odim[2]/2))
# print(ss2_struct)

