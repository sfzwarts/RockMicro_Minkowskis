"""Microstructure generation and image-conversion utilities."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import meshio
import numpy as np
import porespy as ps
import scipy.ndimage
from PIL import Image
from skimage import io, measure
from skimage.draw import polygon


def _require_openmc():
    """Import OpenMC only for workflows that actually need it."""
    try:
        import openmc
    except ImportError as exc:  # pragma: no cover - depends on external software
        raise ImportError(
            "OpenMC is required for heterogeneous sphere packings. "
            "Install the full Conda environment from environment.yml."
        ) from exc
    return openmc


def Volume(outer_radius: float = 0.005):
    """Return the thin OpenMC region used to create a heterogeneous 2D slice."""
    openmc = _require_openmc()
    min_x = openmc.XPlane(x0=-outer_radius, boundary_type="reflective")
    max_x = openmc.XPlane(x0=1 + outer_radius, boundary_type="reflective")
    min_y = openmc.YPlane(y0=-outer_radius, boundary_type="reflective")
    max_y = openmc.YPlane(y0=1 + outer_radius, boundary_type="reflective")
    min_z = openmc.ZPlane(z0=-outer_radius * 5, boundary_type="reflective")
    max_z = openmc.ZPlane(z0=outer_radius * 5, boundary_type="reflective")
    return +min_x & -max_x & +min_y & -max_y & +min_z & -max_z


def ThreeD_Volume(outer_radius: float = 0.005):
    """Return the unit-cube OpenMC region used for a 3D sphere packing."""
    openmc = _require_openmc()
    min_x = openmc.XPlane(x0=-outer_radius, boundary_type="reflective")
    max_x = openmc.XPlane(x0=1 + outer_radius, boundary_type="reflective")
    min_y = openmc.YPlane(y0=-outer_radius, boundary_type="reflective")
    max_y = openmc.YPlane(y0=1 + outer_radius, boundary_type="reflective")
    min_z = openmc.ZPlane(z0=-outer_radius, boundary_type="reflective")
    max_z = openmc.ZPlane(z0=1 + outer_radius, boundary_type="reflective")
    return +min_x & -max_x & +min_y & -max_y & +min_z & -max_z


def Random_Closed_Packing(
    output_dir: str | Path,
    name: str,
    region,
    seed: int,
    outer_radius: float = 0.005,
    pf: float = 0.62,
) -> Path:
    """Generate an OpenMC sphere packing and save its centre coordinates."""
    openmc = _require_openmc()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    centers = openmc.model.pack_spheres(
        radius=outer_radius, region=region, pf=pf, seed=seed
    )
    output_file = output_dir / f"{name}_centers.txt"
    np.savetxt(output_file, centers)
    return output_file


def Slice_RCP(
    circle_data_dir: str | Path, name: str, outer_radius: float = 0.005
) -> Path:
    """Replace 3D sphere centres with their radii in the central 2D slice."""
    output_file = Path(circle_data_dir) / f"{name}_centers.txt"
    centers = np.atleast_2d(np.genfromtxt(output_file))

    sliced = []
    for x, y, z, *_ in centers:
        if abs(z) <= outer_radius * 0.999:
            sliced.append((x, y, 0, (outer_radius**2 - z**2) ** 0.5))
    np.savetxt(output_file, sliced)
    return output_file


def create_blobs(
    porosity: float,
    blobiness: float,
    output_dir: str | Path,
    shape: Sequence[int] = (770, 770),
    seed: int | None = None,
) -> Path:
    """Generate a binary cemented microstructure and return its PNG path."""
    if not 0 < porosity < 1:
        raise ValueError("porosity must be between 0 and 1")

    image = ps.generators.blobs(
        shape=tuple(shape), porosity=porosity, blobiness=blobiness, seed=seed
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / (
        f"blobiness_{blobiness:.1f}_porosity_{porosity:.2f}.png"
    )
    Image.fromarray(image.astype(np.uint8) * 255, mode="L").save(output_file)
    return output_file


def Create_Blobs(
    porosity: float,
    blobiness: float,
    output_path: str | Path,
    shape: Sequence[int] = (770, 770),
) -> Path:
    """Backward-compatible alias for :func:`create_blobs`."""
    return create_blobs(porosity, blobiness, output_path, shape)


def create_effective_porosity(image_path: str | Path) -> Path:
    """Save only pore paths that connect the first and last image rows."""
    image_path = Path(image_path)
    pore_space = io.imread(image_path, as_gray=True) > 0.5
    inlets = np.zeros_like(pore_space, dtype=bool)
    outlets = np.zeros_like(pore_space, dtype=bool)
    inlets[0, :] = True
    outlets[-1, :] = True

    connected = ps.filters.trim_nonpercolating_paths(
        im=pore_space, inlets=inlets, outlets=outlets
    )
    output_file = image_path.with_name(f"{image_path.stem}_effective_porosity.png")
    Image.fromarray(connected.astype(np.uint8) * 255, mode="L").save(output_file)
    return output_file


def create_effective_por(image_path: str | Path) -> Path:
    """Backward-compatible alias for :func:`create_effective_porosity`."""
    return create_effective_porosity(image_path)


def mesh_to_png(
    mesh_path: str | Path,
    output_path: str | Path,
    image_shape: tuple[int, int] = (1000, 1000),
) -> Path:
    """Rasterize a 2D triangle or quadrilateral mesh as a binary PNG."""
    mesh = meshio.read(mesh_path)
    points = mesh.points[:, :2]
    if "triangle" in mesh.cells_dict:
        cells = mesh.cells_dict["triangle"]
    elif "quad" in mesh.cells_dict:
        cells = mesh.cells_dict["quad"]
    else:
        raise ValueError("mesh contains neither triangle nor quad cells")

    binary_image = np.zeros(image_shape, dtype=np.uint8)
    minimum = points.min(axis=0)
    maximum = points.max(axis=0)
    scale = (np.asarray(image_shape[::-1]) - 1) / (maximum - minimum)

    for cell in cells:
        vertices = (points[cell] - minimum) * scale
        rows, columns = polygon(vertices[:, 1], vertices[:, 0], shape=image_shape)
        binary_image[rows, columns] = 1

    output_file = Path(output_path).with_suffix(".png")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(binary_image * 255, mode="L").save(output_file)
    return output_file


def crop_image(output_path: str | Path) -> Path:
    """Remove a one-pixel border from a PNG."""
    image_path = Path(output_path).with_suffix(".png")
    with Image.open(image_path) as image:
        width, height = image.size
        image.crop((1, 1, width - 1, height - 1)).save(image_path)
    return image_path


def dat_to_bw_png(input_file: str | Path, output_file: str | Path) -> Path:
    """Convert rows containing ``True``/``False`` tokens to a binary PNG."""
    rows = []
    with Path(input_file).open() as stream:
        for line in stream:
            if "True" in line or "False" in line:
                rows.append([word == "True" for word in line.split()])
    image = np.asarray(rows, dtype=np.uint8) * 255
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image, mode="L").save(output_file)
    return output_file


def binarize_image(image_path: str | Path, threshold: float = 0.5) -> Path:
    """Threshold an image in place."""
    image_path = Path(image_path)
    binary = io.imread(image_path, as_gray=True) > threshold
    io.imsave(image_path, binary.astype(np.uint8) * 255, check_contrast=False)
    return image_path


def create_random_packing_porespy(
    output_dir: str | Path,
    seed: int,
    packing_fraction: float,
    radius_pixels: int = 5,
    edges: str = "extended",
    shape: Sequence[int] = (1000, 1000),
    physical_radius: float = 0.005,
) -> Path:
    """Generate an equal-radius 2D packing and save normalized coordinates."""
    try:
        spheres = ps.generators.random_spheres(
            tuple(shape),
            r=radius_pixels,
            volume_fraction=packing_fraction,
            edges=edges,
            seed=seed,
        )
    except TypeError:  # PoreSpy 2.3 used the older keyword names
        spheres = ps.generators.random_spheres(
            shape=tuple(shape),
            r=radius_pixels,
            phi=packing_fraction,
            edges=edges,
            seed=seed,
        )
    spheres = spheres.astype(np.uint8)
    labels, _ = scipy.ndimage.label(spheres)
    properties = measure.regionprops(labels)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"Model_{seed}_pf_{packing_fraction:.3f}.txt"
    height, width = shape[:2]
    with output_file.open("w") as stream:
        for prop in properties:
            row, column = prop.centroid[:2]
            stream.write(
                f"{column / width:.12g} {row / height:.12g} 0 "
                f"{physical_radius:.12g}\n"
            )
    return output_file


def create_RP_porespy(
    path: str | Path,
    seed: int,
    packing_fraction: float,
    radius: int,
    edges: str = "extended",
    shape: Sequence[int] = (1000, 1000),
) -> Path:
    """Backward-compatible wrapper around :func:`create_random_packing_porespy`."""
    return create_random_packing_porespy(
        path,
        seed,
        packing_fraction,
        radius_pixels=int(radius),
        edges=edges,
        shape=shape,
    )
