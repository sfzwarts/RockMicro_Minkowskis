import porespy as ps
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import scipy.ndimage
import os


def generate_microstructures(shape, r, pf, model, mode, path):
    """
    Generate a 3D microstructure of randomly packed spheres and save the
    coordinates to a TXT file.
    """
    spheres = ps.generators.random_spheres(
        shape=shape,
        r=r,
        phi=pf,
        edges=mode,
        seed=int(model)
    ).astype(np.uint8)

    labeled_spheres, num_features = scipy.ndimage.label(spheres)
    props = ps.metrics.regionprops_3D(labeled_spheres)

    coords = [
        (float(prop["centroid"][0]),
         float(prop["centroid"][1]),
         float(prop["centroid"][2]),
         r)
        for prop in props
    ]

    os.makedirs(path, exist_ok=True)
    name_txt = f"{path}/Model_{int(model)}_pf_{pf:1.3f}.txt"

    with open(name_txt, "w") as f:
        for idx, c in enumerate(coords, start=1):
            f.write(f"{idx} {c[0]} {c[1]} {c[2]} {c[3]}\n")

    return coords



def save_slice_png(coords_slice, Nx, Ny, filename, dpi):
    """
    coords_slice: list of (x, y, r_intersect)  → index removed
    Nx, Ny: physical domain size
    filename: PNG output
    dpi: controls pixel resolution
    """

    fig, ax = plt.subplots(figsize=(Nx / 100, Ny / 100))

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.set_xlim(0, Nx)
    ax.set_ylim(0, Ny)
    ax.set_aspect('equal')
    ax.axis('off')

    for (x, y, r) in coords_slice:
        circ = Circle((x, y), r, color='white')
        ax.add_patch(circ)

    fig.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    

def slice_microstructure(coords, shape, model, pf, path,
                         scan_res_high=0.05, scan_res_low=0.25):
    """
    Slice the 3D microstructure into 2D slices at different resolutions
    coords: list of (idx, x, y, z, R)
    shape: 3D shape of the microstructure
    model: model number
    pf: packing fraction
    scan_res_high: high resolution (voxel size)
    scan_res_low: low resolution (voxel size)
    """

    Nx, Ny, Nz = shape

    num_slices = int(Nz / scan_res_high)
    slice_spacing = Nz / num_slices

    slice_high_dir = f"{path}/Slices_Model_{model}_pf_{pf:1.3f}_high_{scan_res_high:1.3f}"
    slice_low_dir  = f"{path}/Slices_Model_{model}_pf_{pf:1.3f}_low_{scan_res_low:1.3f}"
    os.makedirs(slice_high_dir, exist_ok=True)
    os.makedirs(slice_low_dir, exist_ok=True)

    high_dpi = 1 / scan_res_high * 100
    low_dpi  = 1 / scan_res_low  * 100

    print(f"Creating {num_slices} slices (spacing={slice_spacing:.3f} voxels)…")

    for k in range(num_slices):
        z_slice = k * slice_spacing
        slice_coords = []
        for (idx, x, y, z0, R) in coords:
            dz = z0 - z_slice
            if abs(dz) <= R:
                r_intersect = (R**2 - dz**2)**0.5
                slice_coords.append((idx, x, y, r_intersect))

        for folder in [slice_high_dir, slice_low_dir]:
            txt_name = f"{folder}/slice_{k:04d}.txt"
            with open(txt_name, "w") as f:
                for (idx, x, y, r_intersect) in slice_coords:
                    f.write(f"{idx} {x} {y} {r_intersect}\n")

        png_circle_data = [(x, y, r) for (_, x, y, r) in slice_coords]

        save_slice_png(
            png_circle_data, Nx, Ny,
            filename=f"{slice_high_dir}/slice_{k:04d}.png",
            dpi=high_dpi
        )

        save_slice_png(
            png_circle_data, Nx, Ny,
            filename=f"{slice_low_dir}/slice_{k:04d}.png",
            dpi=low_dpi
        )

        print(f"  Slice {k+1}/{num_slices} saved.")

    print("All slices completed!")


if __name__ == "__main__":
    print("Starting Creating Microstructures + Analytic Slicing")

    r = 2
    shape = np.array([100, 100, 250])
    mode = 'extended'
    path = os.getcwd()

    pfs = [0.60]
    models = np.arange(1, 2)

    scan_res_high = 0.05
    scan_res_low  = 0.50

    for model in models:
        for pf in pfs:
            coords = generate_microstructures(shape, r, pf, model, mode, path)
            slice_microstructure(coords, shape, model, pf, path,
                                 scan_res_high, scan_res_low)