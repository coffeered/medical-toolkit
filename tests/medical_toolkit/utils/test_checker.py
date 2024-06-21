from unittest.mock import MagicMock, patch

import pytest

from medical_toolkit.utils.checker import check_file_extension


def test_check_file_extension_valid_file():
    file_path = "test.dcm"

    mock_elements = [
        MagicMock(extension="dcm", confidence=1.0),
        MagicMock(extension="dicom", confidence=0.8),
    ]

    with patch("puremagic.from_file", return_value="dcm"), patch(
        "puremagic.magic_file", return_value=mock_elements
    ):
        result = check_file_extension(file_path)

    assert result["filename_extension"] == "dcm"
    assert len(result["magic_extensions"]) == 2
    assert result["magic_extensions"][0] == ("dcm", 1.0)
    assert result["magic_extensions"][1] == ("dicom", 0.8)


def test_check_file_extension_no_file():
    with pytest.raises(ValueError):
        check_file_extension(None)


def test_check_file_extension_empty_path():
    with pytest.raises(ValueError):
        check_file_extension("")


def test_check_file_extension_magic_file_empty():
    file_path = "test.dcm"

    with patch("puremagic.from_file", return_value="dcm"), patch(
        "puremagic.magic_file", return_value=[]
    ):
        result = check_file_extension(file_path)

    assert result["filename_extension"] == "dcm"
    assert result["magic_extensions"] == []


if __name__ == "__main__":
    pytest.main()
