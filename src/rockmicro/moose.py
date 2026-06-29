"""Helpers for rendering and running the bundled MOOSE input templates."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_TEMPLATE_DIR = REPOSITORY_ROOT / "Simulation_files"
INSTALLED_TEMPLATE_DIR = Path(sys.prefix) / "Simulation_files"
DEFAULT_TEMPLATE_DIR = (
    REPOSITORY_TEMPLATE_DIR
    if REPOSITORY_TEMPLATE_DIR.is_dir()
    else INSTALLED_TEMPLATE_DIR
)
DEFAULT_INPUT_DIR = REPOSITORY_ROOT / "outputs" / "moose_inputs"


def _render_template(
    template_name: str,
    values: dict[str, str],
    output_name: str,
    template_dir: str | Path = DEFAULT_TEMPLATE_DIR,
    output_dir: str | Path = DEFAULT_INPUT_DIR,
) -> Path:
    template_path = Path(template_dir) / template_name
    if not template_path.is_file():
        raise FileNotFoundError(f"MOOSE template not found: {template_path}")

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    output_path = destination / output_name
    output_path.write_text(template_path.read_text().format(**values))
    return output_path


def parse_template_image(
    image: str | Path,
    output_name: str | Path,
    *,
    template_dir: str | Path = DEFAULT_TEMPLATE_DIR,
    output_dir: str | Path = DEFAULT_INPUT_DIR,
) -> Path:
    """Render the 2D image-based MOOSE input file."""
    return _render_template(
        "Navier-Stokes_FCP_2D_image_template.i",
        {"image": str(image), "output_name": str(output_name)},
        "Navier-Stokes_FCP_2D_image_input.i",
        template_dir,
        output_dir,
    )


def parse_template_mesh(
    mesh: str | Path,
    output_name: str | Path,
    *,
    template_dir: str | Path = DEFAULT_TEMPLATE_DIR,
    output_dir: str | Path = DEFAULT_INPUT_DIR,
) -> Path:
    """Render the 2D mesh-based MOOSE input file."""
    return _render_template(
        "Navier-Stokes_FCP_2D_mesh_template.i",
        {"mesh": str(mesh), "output_name": str(output_name)},
        "Navier-Stokes_FCP_2D_mesh_input.i",
        template_dir,
        output_dir,
    )


def call_moose(
    data_file: str | Path,
    moose_executable: str | Path,
    *,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run MOOSE for one input file and raise on simulation failure."""
    executable = Path(moose_executable).expanduser()
    if not executable.is_file():
        raise FileNotFoundError(f"MOOSE executable not found: {executable}")

    return subprocess.run(
        [str(executable), "-i", str(data_file)],
        check=True,
        text=True,
        capture_output=capture_output,
    )


def call_MOOSE(
    data_file_path: str | Path, moose_executable: str | Path | None = None
) -> subprocess.CompletedProcess[str]:
    """Backward-compatible alias for :func:`call_moose`."""
    if moose_executable is None:
        raise ValueError("provide moose_executable")
    return call_moose(data_file_path, moose_executable)


def run_simulation_image(
    image: str | Path,
    output_name: str | Path,
    moose_executable: str | Path,
) -> subprocess.CompletedProcess[str]:
    """Render and run the image-based 2D simulation."""
    data_file = parse_template_image(image, output_name)
    return call_moose(data_file, moose_executable)


def run_simulation_mesh(
    mesh: str | Path,
    output_name: str | Path,
    moose_executable: str | Path,
) -> subprocess.CompletedProcess[str]:
    """Render and run the mesh-based 2D simulation."""
    data_file = parse_template_mesh(mesh, output_name)
    return call_moose(data_file, moose_executable)
