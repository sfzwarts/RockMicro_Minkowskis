# Standard library
import os
import sys

# Scientific stack
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

# Image processing
from skimage import io, color, measure
from skimage.draw import polygon
from skimage.measure import euler_number
from PIL import Image
import mpimg

# Domain-specific libraries
import openmc
import meshio
import porespy as ps

def Volume(outer_radius = 0.005):
        min_x = openmc.XPlane(x0=0-outer_radius, boundary_type='reflective')
        max_x = openmc.XPlane(x0=1+outer_radius, boundary_type='reflective')
        min_y = openmc.YPlane(y0=0-outer_radius, boundary_type='reflective')
        max_y = openmc.YPlane(y0=1+outer_radius, boundary_type='reflective')
        min_z = openmc.ZPlane(z0=-outer_radius*5, boundary_type='reflective')
        max_z = openmc.ZPlane(z0=outer_radius*5, boundary_type='reflective')
        region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
        return region

#Create a Random Circle Packing (RCP)
def Random_Closed_Packing(path, name, region, seed, outer_radius = 0.005, pf = 0.62):
        centers = openmc.model.pack_spheres(radius = outer_radius, region = region, pf = pf, seed=seed)
        with open('%s/Circle_data/%s_centers.txt' % (path, name), 'w') as output:
            np.savetxt(output, centers)

#Create a 2D slice from the RCP
def Slice_RCP(path, name, outer_radius = 0.005):
    centers = np.genfromtxt("%s/Circle_data/%s_centers.txt" % (path, name))
    with open("%s/Circle_data/%s_centers.txt" % (path, name), 'w') as f_out:
        for i in range(len(centers)):
            x=centers[i][0]
            y=centers[i][1]
            z=centers[i][2]
            if abs(z)>outer_radius*0.999:
                continue
            new_radius = ((outer_radius)**2 - (z)**2) ** 0.5
            f_out.write('{0} {1} {2} {3}\n'.format(x,y,0,new_radius))

def ThreeD_Volume(outer_radius = 0.005):
        min_x = openmc.XPlane(x0=0-outer_radius, boundary_type='reflective')
        max_x = openmc.XPlane(x0=1+outer_radius, boundary_type='reflective')
        min_y = openmc.YPlane(y0=0-outer_radius, boundary_type='reflective')
        max_y = openmc.YPlane(y0=1+outer_radius, boundary_type='reflective')
        min_z = openmc.ZPlane(z0=0-outer_radius, boundary_type='reflective')
        max_z = openmc.ZPlane(z0=1+outer_radius, boundary_type='reflective')
        region = +min_x & -max_x & +min_y & -max_y & +min_z & -max_z
        return region
    
#Create a Random Sphere Packing (RCP)
def Random_Closed_Packing(path, name, region, seed, outer_radius = 0.005, pf = 0.62):
        centers = openmc.model.pack_spheres(radius = outer_radius, region = region, pf = pf, seed=seed)
        with open('%s/Sphere_data/%s_centers.txt' % (path, name), 'w') as output:
            np.savetxt(output, centers)

def Create_Blobs(porosity, blobiness, output_path, shape=[770, 770]):
    im = ps.generators.blobs(shape=shape, porosity=porosity, blobiness=blobiness)

    fig, ax = plt.subplots(1, 1, figsize=[4, 4])
    ax.imshow(im, origin='lower', interpolation='none', cmap='gray')  # Add grayscale colormap
    ax.axis('off')  # Turn off axis

    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Save the image
    filename = f"blobiness_{blobiness:.1f}_porosity_{porosity:.2f}.png"
    filepath = os.path.join(output_path, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight', pad_inches=0.0)
    plt.close()

    print(f"Saved {filepath}")
    
def create_effective_por(image_path):
    existing_image = mpimg.imread(image_path)
    height, width = existing_image.shape
    
    base_name = os.path.basename(image_path)
    name_without_ext = os.path.splitext(base_name)[0]

    plt.figure(figsize=[7.2, 7.2])
    plt.axis('off')
    plt.imshow(existing_image, cmap='gray')
    plt.clf()
    
    inlets = np.zeros_like(existing_image)
    inlets[0, :] = True
    outlets = np.zeros_like(existing_image)
    outlets[-1, :] = True

    # Trim non-percolating paths
    x = ps.filters.trim_nonpercolating_paths(im=existing_image, inlets=inlets, outlets=outlets)

    # Construct output path: same as input but with _effective_porosity.png
    output_name = f"{name_without_ext}_effective_porosity.png"
    output_path = os.path.join(os.path.dirname(image_path), output_name)
       
    # Convert to uint8 if needed (assuming x is boolean or float)
    if x.dtype == bool:
        x_uint8 = (x * 255).astype(np.uint8)
    elif x.dtype == float:
        x_uint8 = (x * 255).astype(np.uint8)
    else:
        x_uint8 = x.astype(np.uint8)
        
    # Save as grayscale
    Image.fromarray(x_uint8, mode='L').save(output_path)
                
def mesh_to_png(mesh_path, output_path, image_shape=(1000, 1000)):
    # Load mesh with meshio
    mesh = meshio.read(mesh_path)
    
    # Get node coordinates and elements (triangles or quadrilaterals)
    points = mesh.points[:, :2]  # Only X, Y for 2D mesh
    cells = mesh.cells_dict['triangle'] if 'triangle' in mesh.cells_dict else mesh.cells_dict['quad']
    
    # Create an empty binary image
    binary_image = np.zeros(image_shape, dtype=np.uint8)
    
    # Scale points to fit within the image dimensions
    min_x, min_y = points.min(axis=0)
    max_x, max_y = points.max(axis=0)
    scale_x = (image_shape[1] - 1) / (max_x - min_x)
    scale_y = (image_shape[0] - 1) / (max_y - min_y)
    
    for cell in cells:
        # Get the polygon vertices
        polygon_points = points[cell]
        
        # Scale and shift vertices to image grid
        polygon_points[:, 0] = (polygon_points[:, 0] - min_x) * scale_x
        polygon_points[:, 1] = (polygon_points[:, 1] - min_y) * scale_y
        
        # Use skimage.draw.polygon to fill the triangles/quads
        rr, cc = polygon(polygon_points[:, 1], polygon_points[:, 0], shape=image_shape)
        binary_image[rr, cc] = 1  # Mark as foreground
    
    # Save the binary image as a PNG
    plt.imsave(f"{output_path}.png", binary_image, cmap="gray", dpi=1200)
    plt.clf()
    print(f'Saved {output_path}')
        
def crop_image(output_path):
    image_path = f"{output_path}.png"
    with Image.open(image_path) as image:
        width, height = image.size
        cropped_image = image.crop((1, 1, width - 1, height - 1))
        cropped_image.save(image_path)
        cropped_image.close()  # Not strictly needed with context manager, but safe
    print(f"Cropped: {output_path}.png")

def dat_to_bw_png(input_file, output_file):

    with open(input_file, 'r') as f:
        lines = f.readlines()
    
    bool_lines = []
    for line in lines:
        if 'True' in line or 'False' in line:
            bool_lines.append(line.strip())
    
    data = []
    for line in bool_lines:
        row = [1 if word == 'True' else 0 for word in line.split()]
        data.append(row)
    
    data = np.array(data, dtype=np.uint8)
    img_data = data * 255
    img = Image.fromarray(img_data, mode='L')
    img.save(output_file)

def binarize_image(image_path, threshold=0.5):
    image = io.imread(image_path, as_gray=True)
    binary = (image > threshold).astype(np.uint8) * 255 
    io.imsave(image_path, binary.astype(np.uint8), check_contrast=False)
    print(f"Binarized and saved: {image_path}")
    
def create_RP_porespy(path, seed, packing_fraction, radius, edges='extended', shape=[1000, 1000]):

    spheres = ps.generators.random_spheres(shape=shape, r=radius, phi=packing_fraction, edges=edges, seed=seed)
    spheres = spheres.astype(np.uint8)

    labeled_spheres, num_features = scipy.ndimage.label(spheres)
    props = ps.metrics.regionprops_3D(labeled_spheres)
    coords = [(float(prop['centroid'][0]), float(prop['centroid'][1]), float(prop['centroid'][2]), radius) for prop in props]

    name_txt = f'{path}/Model_{seed}_pf_{packing_fraction:1.3f}'
    with open('%s.txt' %(name_txt), 'w') as f:
        for coord in coords:
            f.write(f"{float(coord[0])/shape[0]} {float(coord[1])/shape[0]} 0 0.005\n")
        
    print('Created  %s' %(name_txt))