import Scripts

# An example of the framework for creating a cemented microstructure and extracting properties from it

blobiness   = 2.0
porosity    = 0.330
shape = [770, 770]
output_path = './data/cemented/2D/blob_images'
image       = f'{output_path}/blobiness_{blobiness:.1f}_porosity_{porosity:.2f}.png'
output_name = f'cemented_blobiness_{blobiness:.1f}_porosity_{porosity:.2f}'

# Create the blobbed microstructure, including the effective porosity in an image
Scripts.microstructures.Create_Blobs(porosity=porosity, blobiness=blobiness, output_path=output_path, shape=shape)
Scripts.microstructures.create_effective_por(image)

## Run simulations in between 
## Note! This won't work without a properly set up simulation file, and the correct path to it. You can use the Navier-Stokes_FCP_2D_image.i file as a template, but you will need to edit it to fit your needs.
moose_executable = '/path/to/moose/executable' # Change this to the path of your MOOSE executable
Scripts.handeling_moose.run_simulation_image(image, output_name)

# Extract properties from the image
M0, M1, M3, tau = Scripts.postprocessing.Obtaining_properties(image, axis=0)