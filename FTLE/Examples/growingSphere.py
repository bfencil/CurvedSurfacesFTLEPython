import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))) # For locating your directory

from FTLE.Curved.CurvedSurfaceMain import FTLE_mesh # The primary function used for FTLE mesh calculations
from FTLE.Curved.utilities import make_vector_field_video
import h5py # for .h5 files


def load_mesh_data_h5(h5_file_path):
    """
    Example function for loading the expected data format.
    Load staggered curved surface mesh data from an HDF5 file.
    Expects groups:
        /node_cons/{t}
        /position/{t}
        /velocity/{t}
        /time_steps
    Returns dict with lists of per-time-step arrays.
    """
    with h5py.File(h5_file_path, 'r') as f:
        time_steps = f["time_steps"][:]
        total_time = len(time_steps)

        # Convert string keys to sorted integers
        keys = sorted(f["position"].keys(), key=lambda k: int(k))

        position = [f["position"][k][:] for k in keys]
        velocity = [f["velocity"][k][:] for k in keys]
        TrianT = [f["TrianT"][k][:] for k in keys]

        # Sanity check
        assert len(position) == total_time, "Mismatch in position data and time_steps"
        assert len(velocity) == total_time
        assert len(TrianT) == total_time

    return {
        'TrianT': TrianT,             # list of (M_t, 3)
        'position': position,               # list of (N_t, 3)
        'velocity': velocity,               # list of (N_t, 3)
        'time_steps': time_steps,
        'node_number': [p.shape[0] for p in position],  # list of node counts per step
        'total_time': total_time
    }

file_path = os.path.join(os.path.dirname(__file__), 'growing_sphere.h5') # fetches the path to the example data contained within the Examples folder


"""
Data is stored as a .h5. The load_mesh_data_h5 file is provided for loading the data but primarily for viewing 
the expected way to store the mesh data in python for usage in coherent structure computations
"""
mesh_data = load_mesh_data_h5(file_path)

node_positions = mesh_data['position']
node_velocities = mesh_data['velocity']
time_steps_array = mesh_data['time_steps']
TrianT = mesh_data['TrianT']


"""
If the data is not a python list it must be made into a list. In this example the 'time_steps'
data is actually a numpy array.
"""

time_steps = time_steps_array.tolist()

initial_time = 0
final_time = 22
particle_positions = node_positions[initial_time]


## Running the simulation
ftle, trajectories, isotropy, back_ftle, back_trajectories, back_isotropy = FTLE_mesh(TrianT, node_positions, node_velocities, particle_positions, initial_time, final_time, time_steps, plot_ftle=True, save_path=None, neighborhood=10)


## Making a video of the vector field flow(will save to your working Python environment directory)
make_vector_field_video(TrianT, node_positions, node_velocities, initial_time, final_time, time_steps, save_path="SphereVectorField.mp4",  framerate=10, camera_setup=( (-2.5458, -6.1214, 0.8577), (-0.0008, 0.0008, 0.0006), 80.96 ))




