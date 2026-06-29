"""Generate and characterize a small cemented microstructure.

Run from the repository root after installing the project:

    python examples/cemented.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from rockmicro import microstructures, postprocessing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--porosity", type=float, default=0.50)
    parser.add_argument("--blobiness", type=float, default=2.0)
    parser.add_argument("--shape", type=int, nargs=2, default=(256, 256))
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/cemented")
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image = microstructures.create_blobs(
        porosity=args.porosity,
        blobiness=args.blobiness,
        output_dir=args.output_dir,
        shape=args.shape,
        seed=args.seed,
    )
    effective_image = microstructures.create_effective_porosity(image)
    m0, m1, m3, tau = postprocessing.compute_properties(image)

    print(f"Image: {image}")
    print(f"Connected pore space: {effective_image}")
    print(f"M0={m0:.6g}, M1={m1:.6g}, M3={m3}, tau={tau:.6g}")


if __name__ == "__main__":
    main()
