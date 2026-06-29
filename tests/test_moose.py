from pathlib import Path

from rockmicro import moose


def test_render_image_template(tmp_path: Path):
    result = moose.parse_template_image(
        "sample.png",
        "results/sample",
        output_dir=tmp_path,
    )

    rendered = result.read_text()
    assert "file = sample.png" in rendered
    assert "file_base = results/sample" in rendered
