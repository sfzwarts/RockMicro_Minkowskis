from pathlib import Path

from rockmicro import microstructures


def test_generate_small_random_packing(tmp_path: Path):
    output = microstructures.create_random_packing_porespy(
        tmp_path,
        seed=1,
        packing_fraction=0.1,
        radius_pixels=2,
        shape=(32, 32),
    )

    assert output.is_file()
    assert len(output.read_text().splitlines()) > 0
