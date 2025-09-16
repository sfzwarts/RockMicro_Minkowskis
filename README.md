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
├── data/                                      # Main dataset
│   ├── cemented/                              # Cemented configurations 
│       ├── 2D/                                # In two dimensions
│           ├── blob_images/                   # Data to (re)create the blobbed images
│           ├── simulation_results/            # The results of the simulations of the hydraulic properties
│   └── random_packings/                       # Random particle packings (all shapes, packing fractions)
│       ├── 2D/                                # In two dimensions
│           ├── heterogeneous_diameter/        # Varying diameter over the structure
│               ├── Circle_data/               # Data of the coordinates and radius of a random grid]
│               ├── simulation_results/        
│           ├── homogeneous_diameter/          # Constant diameter over the structure
│               ├── Circle_data/
│               ├── circle_data_structured/    # Data of the coordinates and radius of the structured grid
│               ├── simulation_results/        
│       ├── 3D/                                # In three dimensions
│               ├── simulation_results/        
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
- [PoreSpy](https://porespy.org/) – microstructure generation and analysis  
- [Gmsh](https://gmsh.info/) – meshing of generated geometries  
- [OpenMC](https://openmc.org/) – (used for geometry sampling / utilities)  
- [NumPy](https://numpy.org/) and [pandas](https://pandas.pydata.org/) – data handling  

For flow simulations, we use the [MOOSE framework](https://mooseframework.inl.gov/) to solve the incompressible Stokes equations on the generated meshes.  

## Contributing
Currently, the main contributors are:

- [S. Zwarts]([https://scholar.google.com/citations?hl=en&user=tFDIX40AAAAJ](https://scholar.google.com/citations?hl=en&user=tFDIX40AAAAJ))
- [W. Lindqwister](https://scholar.google.com/citations?view_op=search_authors&mauthors=winston+lindqwister&hl=en&oi=ao)
- [M. Lesueur](https://scholar.google.com/citations?hl=en&user=Rt6zNgkAAAAJ)
