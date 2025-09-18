import Scripts

# An example of the framework for creating a cemented microstructure and extracting properties from it

blobiness   = 2.0
porosity    = 0.330
output_path = './data/cemented/2D/blob_images'
image       = f'{output_path}/blobiness_{blobiness:.1f}_porosity_{porosity:.2f}.png'
output_name = f'cemented_blobiness_{blobiness:.1f}_porosity_{porosity:.2f}'

# Create the blobbed microstructure, inlcuding the effective porosity
Scripts.microstructures.Create_Blobs(porosity=0.3, blobiness=2, output_path='.', shape=[770,770])
Scripts.microstructures.create_effective_por(image)

## Run simulations in between
Scripts.handeling_moose.run_simulation(image, output_name)

# Extract properties from the image
M0, M1, M3, tau = Scripts.postprocessing.Obtaining_properties(image, axis=0)
# These you can either add to the CSV file, or use them for further processing