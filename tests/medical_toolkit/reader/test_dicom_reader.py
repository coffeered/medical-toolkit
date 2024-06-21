import os
from unittest.mock import patch

import pytest
import SimpleITK as sitk

from medical_toolkit.reader.dicom_reader import DicomReader, DicomSeriesReader


TAG_STUDY_INSTANCE_UID = "0020|000d"
TAG_SERIES_INSTANCE_UID = "0020|000e"
TAG_IMAGE_POSITION = "0020|0032"


@pytest.fixture
def reader():
    return DicomReader()


@pytest.fixture
def series_reader():
    return DicomSeriesReader()


@pytest.fixture
def dicom_file(tmpdir):
    # Create a temporary DICOM file for testing
    file_path = os.path.join(tmpdir, "test.dcm")
    img = sitk.Image(10, 10, sitk.sitkUInt8)
    sitk.WriteImage(img, file_path)
    return file_path


@pytest.fixture
def dicom_series_dir(tmpdir):
    # Create a temporary directory with multiple DICOM files for testing
    series_dir = os.path.join(tmpdir, "dicom_series")
    os.makedirs(series_dir, exist_ok=True)

    # fake 5 slices which are duplcated
    for i in range(5):
        file_path = os.path.join(series_dir, f"image_{i}.dcm")
        img = sitk.Image(10, 10, sitk.sitkUInt8)

        # Set metadata
        pos_z = i * 10.0  # Adjust this to set unique positions

        img.SetMetaData(TAG_STUDY_INSTANCE_UID, "study_uid")
        img.SetMetaData(TAG_SERIES_INSTANCE_UID, "series_uid")
        img.SetMetaData(TAG_IMAGE_POSITION, f"-114.381\\-161.092\\{pos_z}")
        sitk.WriteImage(img, file_path)
    return series_dir


@pytest.fixture
def invalid_file(tmpdir):
    # Create a temporary txt file for testing
    file_path = os.path.join(tmpdir, "invalid_file.txt")
    with open(file_path, "w"):
        pass
    return file_path


def test_dicom_reader_check_valid(reader, dicom_file):
    assert reader.check_valid(dicom_file)


def test_dicom_reader_check_invalid(reader, invalid_file):
    with pytest.raises(ValueError):
        reader.check_valid(invalid_file)


def test_dicom_reader_read(reader, dicom_file):
    data = reader.read(dicom_file)
    assert "data_array" in data
    assert "origin" in data
    assert "spacing" in data
    assert "direction" in data


@patch("medical_toolkit.reader.dicom_reader.DicomSeriesReader._extract_metadata")
def test_dicom_series_reader_check_valid(
    mock_extract_metadata, series_reader, dicom_series_dir
):
    mock_extract_metadata.return_value = ("study1", "series1", 0)
    valid_files = series_reader.check_valid(dicom_series_dir)
    assert len(valid_files) == 1  # Expecting 1 valid files with same mocking positions


@patch("medical_toolkit.reader.dicom_reader.DicomSeriesReader._extract_metadata")
def test_dicom_series_reader_read(
    mock_extract_metadata, series_reader, dicom_series_dir
):
    mock_extract_metadata.return_value = ("study1", "series1", 0)
    valid_files = series_reader.check_valid(dicom_series_dir)
    data = series_reader.read(valid_files)
    assert "data_array" in data
    assert "origin" in data
    assert "spacing" in data
    assert "direction" in data
    assert "study_id" in data
    assert "series_id" in data
    assert "resampled_array" in data


@patch("medical_toolkit.reader.dicom_reader.DicomSeriesReader._extract_metadata")
def test_dicom_series_reader_call(
    mock_extract_metadata, series_reader, dicom_series_dir
):
    mock_extract_metadata.return_value = ("study1", "series1", 0)
    data = series_reader(dicom_series_dir)
    assert "data_array" in data
    assert "origin" in data
    assert "spacing" in data
    assert "direction" in data
    assert "study_id" in data
    assert "series_id" in data
    assert "resampled_array" in data
