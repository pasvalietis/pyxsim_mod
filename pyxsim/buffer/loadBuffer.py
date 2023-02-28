import numpy as np
import yt


class loadBuffer:

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

    def dsa(self, obj, n):
        """
        "Down-sample All"
        Selects all fields from full yt object generated from simulation and down-samples them by every nth element
        *CURRENTLY LENGTH UNITS ONLY CM*

        :param obj: Full yt object
        :param n: Down-sampling factor
        :return: Down-sampled yt object
        """

        ad = obj.all_data()  # Get all data

        ss_dat = {}
        ss_dims = [0, 0, 0]

        for field in obj.field_list:
            name = field[0]
            property = field[1]

            gd = ad[name, property]         # Get selected field data
            unit = gd[1]                    # Get field units

            na = np.array([gd])                         # Turn data into np array
            na = np.reshape(na, obj.domain_dimensions)  # Shape np array to proper dimensions

            ss = na[::n, ::n, ::n]  # Subsample the field every n dimensions
            ss_dims = ss.shape      # Store the shape of the sub-sampled array

            ss_dat[property] = (ss, unit)

        dle = obj.domain_left_edge
        dre = obj.domain_right_edge

        bbox = np.array(  # Bounding box of the domain in code units
            [[dle[0], dre[0]], [dle[1], dre[1]], [dle[2], dre[2]]]
        )
        L = "cm"  # Length units

        ds = yt.load_uniform_grid(ss_dat, ss_dims, L, bbox=bbox, sim_time=obj.parameters["Time"])

        return ds

    def dsl(self, obj, n):
        """
        "Downsample Load"
        Uses built-in yt fixed resolution function to load a yt object from the target path
        at a particular subsampling rate

        :param obj: Path containing full dataset
        :param n: Down-sampling factor
        :return: Down-sampled yt object
        """

        nDim = obj.domain_dimensions / n
        nx = complex(0, nDim[0])
        ny = complex(0, nDim[1])
        nz = complex(0, nDim[2])

        rds = obj.r[::nx, ::ny, ::nz]

        newName = obj.basename.rsplit(".", 1)[0] + "_ss" + str(n)
        save = rds.save_as_dataset(filename=newName, fields=obj.field_list)

        nds = yt.load(save)

        return nds



