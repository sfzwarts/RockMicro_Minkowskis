# RockMicro_Minkowskis

## Description
RockMicro_Minkowskis is an open-source database of generated rock microstructures with computed Minkowski functionals and corresponding Stokes flow simulation results.

The dataset is designed to explore the relationship between microstructural features and macroscopic transport properties, with controlled variation in:
- Particle shape: circles, rectangles, ellipses, triangles
- Packing fraction: systematically varied to capture pore-scale transitions
- Connectivity: cemented configurations are included to study reduced connectivity

<figure>
  <p float="left">
    <img src="Data/random_packings/2D/homogenous_diameter/Circle_data/Model_1_pf_0.380_circle_extra_1_beta_0.png" width="350" />
    <img src="Data/cemented/2D/blob_images/blobiness_1.0_porosity_0.50.png" width="350" /> 
  </p>
  <figcaption align="center">
    Example microstructures: (left) random packing of circular particles, (right) cemented configuration with reduced connectivity.
  </figcaption>
</figure>

This repository contains both the data and the scripts used for generation and analysis.

## Dataset structure
```bash
RockMicro_Minkowskis/
│
├── data/                                      # Main dataset (CSV files with Minkowski + flow results)
│   ├── cemented/                              # Cemented configurations (reduced connectivity)
│       ├── 2D/                                # In two dimensions
│           ├── blob_images/                   # Varying diameter over the structure
│           ├── simulation_results/            # Varying diameter over the structure
│   └── random_packings/                       # Random particle packings (all shapes, packing fractions)
│       ├── 2D/                                # In two dimensions
│           ├── heterogeneous_diameter/        # Varying diameter over the structure
│               ├── Circle_data/               # Data of the coordinates and radius of a random grid
│               ├── Circle_data_structured/    # Data of the coordinates and radius of the structured grid
│               ├── simulation_results/        # Data of the hydraulic properties related to the circle data
│           ├── homogeneous_diameter/          # Constant diameter over the structure
│               ├── Circle_data/               # Data of the coordinates and radius of a random grid
│               ├── simulation_results/        # Data of the hydraulic properties related to the circle data
│       ├── 3D/                                # In three dimensions
│               ├── simulation_results/        # Data of the hydraulic properties related to the circle data
│               ├── simulation_results/        # Data of the hydraulic properties related to the circle data
│               ├── Sphere_data/               # Data of the hydraulic properties related to the circle data
│
├── scripts/                   # Python scripts for geometry generation and analysis
│   ├── meshing.py
│   ├── microstructures.py
│   └── postprocessing.py
│
├── Simulation_files/          # Example input files for Stokes flow simulations in MOOSE
│   ├── stokes_input.i
│   └── mesh_example.e
│
└── README.md                  # This file
```
## Software requirements
The Python scripts rely on the following packages and dependencies:
- PoreSpy       – microstructure generation and analysis
- Gmsh          – meshing of generated geometries
- OpenMC        – (used for geometry sampling / utilities)
- NumPy, pandas – data handling

For flow simulations, we use the MOOSE framework to solve the incompressible Stokes equations on the generated meshes

## Contributing
Currently, the main contributors are W. Lindqwister, M. Lesueur and S. Zwarts. 
