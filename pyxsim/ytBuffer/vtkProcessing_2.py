import numpy as np
import yt

ds = yt.load("flarecs-id.0035.vtk")  # loads full vtk file
ddims = ds.domain_dimensions

# print(ddim)
# print(ds.field_list)
# print(ds.derived_field_list)

ad = ds.all_data()          # Get all data
gd = ad["gas", "density"]   # Get density data
na = np.array([gd])         # Turn data into np array
na = np.reshape(na, ddims)   # Shape np array to proper dimensions

ss2 = na[::2, ::2, ::2]  # Subsampling each dimension by 2
ss2_dims = ss2.shape
ss3 = na[::3, ::3, ::3]  # Subsampling each dimension by 3

# Creating yt object for ss2
ss2_dat = {"density": (ss2, "g/cm**3")}  # Open dictionary
bbox = np.array(                         # Bounding box of the domain in code units
    [[-0.5, 0.5], [0, 1], [-0.25, 0.25]]
)
L = "cm"                                 # Length units
ds2 = yt.load_uniform_grid(ss2_dat, ss2_dims, L, bbox=bbox, sim_time=3.500282)

slc2 = yt.SlicePlot(ds2, "z", "density")
slc2.save("Downsample2_slice")


def down_sample_select(obj, field, n):
    """
    Selects a single field from full yt object generated from simulation and down-samples it by every nth element

    :param obj: Full yt object
    :param field: Field of the intended data
    :param n: Down-sampling factor
    :return: Down-sampled yt object
    """

    ad = obj.all_data()  # Get all data
    gd = ad["gas", "density"]  # Get selected field data
    na = np.array([gd])  # Turn data into np array
    na = np.reshape(na, obj.domain_dimensions)  # Shape np array to proper dimensions

    ss = na[::n, ::n, ::n]
    ss_dims = ss.shape

    ss_dat = {"density": (ss, "g/cm**3")}  # Open dictionary
    bbox = np.array(  # Bounding box of the domain in code units
        [[-0.5, 0.5], [0, 1], [-0.25, 0.25]]
    )
    L = "cm"  # Length units

    ds = yt.load_uniform_grid(ss_dat, ss_dims, L, bbox=bbox, sim_time=obj.parameters["Time"])

    return ds


ds3 = down_sample_select(ds, "density", 3)

slc3 = yt.SlicePlot(ds3, "z", "density")
slc3.save("Downsample3_slice")

