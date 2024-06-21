import pytest

from medical_toolkit.utils.extensions import DICOM_EXT, NIFTI_EXT, TIFF_EXT


def test_nifti_extensions():
    expected_extensions = (".nia", ".nii", ".nii.gz", ".hdr", ".img", ".img.gz")
    assert NIFTI_EXT == expected_extensions


def test_dicom_extensions():
    expected_extensions = (".dcm", ".dicom")
    assert DICOM_EXT == expected_extensions


def test_tiff_extensions():
    expected_extensions = (".tif", ".tiff")
    assert TIFF_EXT == expected_extensions


if __name__ == "__main__":
    pytest.main()
