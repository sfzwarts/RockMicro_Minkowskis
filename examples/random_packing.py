"""Generate and optionally mesh a homogeneous two-dimensional packing.

Run from the repository root after installing the project:

    python examples/random_packing.py
    python examples/random_packing.py --mesh
"""

from __future__ import annotations

import argparse
from pathlib import Path

from rockmicro import microstructures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--packing-fraction", type=float, default=0.35)
    parser.add_argument("--radius-pixels", type=int, default=5)
    parser.add_argument("--shape", type=int, nargs=2, default=(256, 256))
    parser.add_argument("--mesh", action="store_true")
    parser.add_argument("--mesh-resolution", type=float, default=0.005)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/random_packing")
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coordinate_dir = args.output_dir / "circle_data"
    coordinates = microstructures.create_random_packing_porespy(
        output_dir=coordinate_dir,
        seed=args.seed,
        packing_fraction=args.packing_fraction,
        radius_pixels=args.radius_pixels,
        shape=args.shape,
    )
    print(f"Coordinates: {coordinates}")

    if args.mesh:
        from rockmicro import meshing

        mesh = meshing.Model_gmsh(
            path=args.output_dir,
            path_data=coordinate_dir,
            name=coordinates.stem,
            resolution=args.mesh_resolution,
            shape="circle",
        )
        print(f"Mesh: {mesh}")


if __name__ == "__main__":
    main()
