# Description of database

The folder structere is as follows in the database:

```bash
│
├── data/                                      # Main dataset
│   ├── cemented/                              # Cemented configurations 
│       └── 2D/                                # In two dimensions
│           ├── blob_images/                   # Data to (re)create the blobbed images
│           └── simulation_results/            # The results of the simulations of the hydraulic properties
│
│   └── random_packings/                       # Random particle packings (all shapes, packing fractions)
│       ├── 2D/                                # In two dimensions
│           ├── heterogeneous_diameter/        # Varying diameter over the structure
│               ├── Circle_data/               # Data of the coordinates and radius of a random grid]
│               └── simulation_results/        
│
│           └── homogeneous_diameter/          # Constant diameter over the structure
│               ├── Circle_data/
│               ├── circle_data_structured/    # Data of the coordinates and radius of the structured grid
│               └── simulation_results/        
│
│       └── 3D/                                # In three dimensions
│               ├── simulation_results/        
│               └── Sphere_data/               # Data of the hydraulic properties related to the circle data
│
```

In the database, the filenames of the random packings will have the following set up:
- In 2D: `Summary_{shape}_{packing_fraction}_extra_{shape_parameter}_beta_{beta_1}`  
- In 3D: `Summary_{shape}_{packing_fraction}_extra1_{shape_parameter_1}_extra2_{shape_parameter_2}_beta1_{beta_1}_beta2_{beta_2}`

Which includes the following variables:
- shape: different types of shapes in the circles
- packing fraction: the amount of packing which is within the predetermined volume
- shape_parameter: The extra parameter relates to the shape of the inscription. For circles, it will always be one. For ellipses and rectangles, it is the height/length ratio (and extra_2 height/width ratio in the 3D case). For the triangles, it is the angle of the triangle (in xz and xy direction), which gives way for different skewnesses of triangle or pyramid fittings.
- beta: the angle of rotation of each particle in radians

e.g.: Filename example
- Summary_circle_0.310_extra_1.0_beta_r.csv


<figure>
  <p float="left">
    <img src="../README_images/Fitting_shapes.png" width="700" />
  </p>
  <figcaption align="center">
    Visualisation of different grain shapes inscribed in the circle, at a certain rotation, here shown as beta_1 = 0, alligned with the flow direction
  </figcaption>
</figure>

