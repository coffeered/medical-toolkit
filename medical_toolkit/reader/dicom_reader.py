import glob
import logging
import os
from collections import defaultdict

import SimpleITK as sitk

from medical_toolkit.reader.base_reader import BaseCTMRIReader
from medical_toolkit.utils.checker import check_file_extension
from medical_toolkit.utils.extensions import DICOM_EXT

__all__ = ["DicomReader", "DicomSeriesReader"]

TAG_STUDY_INSTANCE_UID = "0020|000d"
TAG_SERIES_INSTANCE_UID = "0020|000e"
TAG_IMAGE_POSITION = "0020|0032"


class DicomReader(BaseCTMRIReader):
    def __init__(self):
        super().__init__()
        self.extensions = DICOM_EXT

    def check_valid(self, path: str) -> bool:
        """
        Check if the given path is a valid DICOM file.

        Parameters:
            path (str): The file path to check.

        Returns:
            bool: True if the path is a valid DICOM file, False otherwise.
        """
        check_results = check_file_extension(path)
        for extension, confidence in check_results["magic_extensions"]:
            if extension in self.extensions:
                return True
        return check_results["filename_extension"] in self.extensions

    def read(self, path: str) -> dict:
        """
        Read the DICOM file from the given path.

        Parameters:
            path (str): The file path to read.

        Returns:
            dict: A dictionary containing: data array, origin, spacing and direction
        """
        sitk_reader = sitk.ReadImage(path, imageIO="GDCMImageIO")
        data_array = sitk.GetArrayFromImage(sitk_reader)
        data = {
            "data_array": data_array,
            "origin": sitk_reader.GetOrigin(),
            "spacing": sitk_reader.GetSpacing(),
            "direction": sitk_reader.GetDirection(),
        }
        return data


class DicomSeriesReader(DicomReader):
    def __init__(self):
        super().__init__()

    def _extract_metadata(self, file_path: str):
        """
        Extract study ID, series ID, and Z position from a DICOM file.

        Parameters:
            file_path (str): The path to the DICOM file.

        Returns:
            tuple: A tuple containing study ID, series ID, and Z position.
        """
        dcm_sitk = sitk.ReadImage(file_path, imageIO="GDCMImageIO")
        study_id = dcm_sitk.GetMetaData(TAG_STUDY_INSTANCE_UID)
        series_id = dcm_sitk.GetMetaData(TAG_SERIES_INSTANCE_UID)
        pos_z = float(dcm_sitk.GetMetaData(TAG_IMAGE_POSITION).split("\\")[-1])
        return study_id, series_id, pos_z

    def check_valid(self, path: str) -> list:
        """
        Check if the given path is a valid DICOM series folder.

        Parameters:
            path (str): The folder path to check.

        Returns:
            list: A list of valid DICOM file paths if the series is valid,
                  otherwise an empty list.
        """
        if not os.path.isdir(path):
            logging.error(f"Provided path {path} is not a directory.")
            return []

        dicom_files = glob.glob(os.path.join(path, "**"), recursive=True)
        dcm_by_series_in_study = defaultdict(dict)

        for dicom_file in dicom_files:
            if os.path.isdir(dicom_file) or not super().check_valid(dicom_file):
                continue
            study_id, series_id, pos_z = self._extract_metadata(dicom_file)
            series_in_study = f"{study_id}-{series_id}"

            if pos_z in dcm_by_series_in_study[series_in_study]:
                logging.warning(
                    f"Duplicate file '{dicom_file}' found in series {series_id} of "
                    f"study {study_id}. Conflicting files: `{dicom_file}` and "
                    f"`{dcm_by_series_in_study[series_in_study][pos_z]}`"
                )
            dcm_by_series_in_study[series_in_study][pos_z] = dicom_file

        if len(dcm_by_series_in_study) != 1:
            logging.error(
                f"Expected exactly one series per study, but found "
                f"{len(dcm_by_series_in_study)} in directory {path}."
            )
            return []

        valid_dicom_pairs = dcm_by_series_in_study.popitem()[1]
        valid_dicom_files = [
            valid_dicom_pairs[p] for p in sorted(valid_dicom_pairs.keys())
        ]
        return valid_dicom_files

    def read(self, valid_dicom_files: list) -> dict:
        """
        Read a series of DICOM files.

        Parameters:
            valid_dicom_files (list): A list of valid DICOM file paths.

        Returns:
            dict: A dictionary containing the data array, origin, spacing, direction,
                  study ID, and series ID.
        """
        dicom_reader = sitk.ImageSeriesReader()
        dicom_reader.SetFileNames(valid_dicom_files)
        dicom_sitk = dicom_reader.Execute()
        data_array = sitk.GetArrayFromImage(dicom_sitk)
        study_id, series_id, _ = self._extract_metadata(valid_dicom_files[0])
        resample_array = self.resample_image(dicom_sitk, new_spacing=[1, 1, 1])

        return {
            "data_array": data_array,
            "origin": dicom_sitk.GetOrigin(),
            "spacing": dicom_sitk.GetSpacing(),
            "direction": dicom_sitk.GetDirection(),
            "study_id": study_id,
            "series_id": series_id,
            "resampled_array": resample_array,
        }

    def __call__(self, path: str, normalization: str = None) -> dict:
        """
        Process the DICOM series at the given path.

        Parameters:
            path (str): The folder path containing the DICOM series.
            normalization (str, optional): The normalization method to apply.

        Returns:
            dict: A dictionary containing the processed DICOM series data.
        """
        valid_dicom_files = self.check_valid(path)
        if not valid_dicom_files:
            raise ValueError(f"Invalid DICOM series folder: {path}")
        data = self.read(valid_dicom_files)
        if normalization:
            data = self.normalization(data, normalization)
        return data
