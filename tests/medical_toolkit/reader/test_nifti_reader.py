import os
import pytest
import SimpleITK as sitk

from medical_toolkit.reader.nifti_reader import (
    NiftiReader,
)  # Adjust the import path as per your actual project structure


@pytest.fixture
def nifti_reader():
    return NiftiReader()


@pytest.fixture
def nifti_file(tmpdir):
    # Create a temporary NIFTI file for testing
    file_path = os.path.join(tmpdir, "test.nii.gz")
    img = sitk.Image(10, 10, sitk.sitkUInt8)
    sitk.WriteImage(img, file_path)
    return file_path


@pytest.fixture
def invalid_file(tmpdir):
    # Create a temporary text file for testing
    file_path = os.path.join(tmpdir, "invalid_file.txt")
    with open(file_path, "w"):
        pass
    return file_path


def test_nifti_reader_check_valid(nifti_reader, nifti_file, invalid_file):
    # Check valid NIFTI file
    assert nifti_reader.check_valid(nifti_file)

    # Check invalid file
    assert not nifti_reader.check_valid(invalid_file)
