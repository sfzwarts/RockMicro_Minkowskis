import Scripts

# General parameters
seed = 1
packing_fraction = 0.5
name = f'Model_{seed}_pf_{packing_fraction}'
resolution = 0.001
shape = 'circle'
extra = 1
beta = 'r'

# An example of creating a random packing of circles with varying diameter.
# Note, for this script you need OpenMC
path = 'Data/random_packings/2D/heterogeneous_diameter/'
Volume = Scripts.microstructures.Volume()
Scripts.microstructures.Random_Closed_Packing(f'{path}/circle_data', name, Volume, seed, pf=packing_fraction)
Scripts.microstructures.Slice_RCP(path, name)

## Another exmaple of creating a random packing of circles with a constant diameter.
# Note, for this script you need PoreSpy
path = 'Data/random_packings/2D/homogeneoous_diameter/'
Scripts.mnicrostructures.create_RP_porespy(f'{path}/circle_data', seed, packing_fraction, radius=0.005, edges='extended')

# Set the name of the text file containing the coordinates and mesh path
text_file = f'{path}{name}_centers.txt'
mesh_path = f'Data/random_packings/2D/heterogeneous_diameter/'

# Now we create the mesh with the text file containing the coordinates
Scripts.meshing.Model_gmsh(path, text_file, name, resolution, shape='circle')
mesh_file = f'{path}/Meshes/Meshes_porespy/{name}_{shape}_{str(extra)}_r_{beta}_res_{str(resolution)}_mesh_2d.msh'

# Running the moose Simulation based on the mesh
output_name = f'{path}/output_files/{name}_{shape}_{str(extra)}_r_{beta}_res_{str(resolution)}'
Scripts.handeling_moose.run_simulatio_mesh(mesh_file, output_name)