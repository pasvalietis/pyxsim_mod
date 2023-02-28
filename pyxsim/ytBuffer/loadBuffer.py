import numpy as np
import yt


class LoadBuffer:

    def __init__(self):
        return

    def dss(self, obj, field, n):
        """
        "Down-sample Select"
        Selects a single field from full yt object generated from simulation and down-samples it by every nth element
        *CURRENTLY ONLY WORKING FOR GAS FIELD*

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