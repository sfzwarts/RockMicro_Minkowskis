# RockMicro_Minkowskis

## Description
RockMicro_Minkowskis is an open-source database of generated rock microstructures with computed Minkowski functionals and corresponding Stokes flow simulation results.
The dataset is designed to explore the relationship between microstructural features and macroscopic transport properties, with controlled variation in particle shape (circles, rectangles, ellipses, triangles) and packing fraction.
Additionally, cemented configurations with reduced connectivity are included to extend the diversity of microstructural characteristics.

## Software requirements
The Python scripts rely on certain packages: GMSH, PoreSpy, OpenMC, and their dependencies.
The Stokes flow simulations are performed within the MOOSE framework

## Repository structure
RockMicro_Minkowskis/
│
├── data/                
│   ├── random_packings/ 
│       ├── 2D/
│             ├── homogeneous_diameter/ 
│             ├── heterogeneous_diameter/ 
│       ├── 3D/
│   ├── cemented_microstructures/         
│
├── scripts/             
│   ├── meshing/ 
│   ├── postprocessing/ 
│
├── docs/                # Documentation, figures, and examples
│
└── README.md            # This file

## Contributing
Currently, the main contributors are W. Linqwister, M. Lesueur and S. Zwarts. 
