import SimpleITK as sitk

from medical_toolkit.reader.base_reader import BaseCTMRIReader
from medical_toolkit.utils.extensions import NIFTI_EXT

__all__ = ["NiftiReader"]


class NiftiReader(BaseCTMRIReader):
    def __init__(self):
        super().__init__()
        self.extensions = NIFTI_EXT

    def check_valid(self, path: str) -> bool:
        """
        Check if the given path is a valid NIFTI file.

        Parameters:
            path (str): The file path to check.

        Returns:
            bool: True if the path is valid, False otherwise.
        """
        for extension in self.extensions:
            if path.lower().endswith(extension):
                return True
        return False

    def read(self, path: str) -> dict:
        """
        Read the NIFTI file from the given path.

        Parameters:
            path (str): The file path to read.

        Returns:
            dict: A dictionary containing the data array.
        """
        nii_sitk = sitk.ReadImage(path, imageIO="NiftiImageIO")
        data_array = sitk.GetArrayFromImage(nii_sitk)
        spacing = nii_sitk.GetSpacing()
        origin = nii_sitk.GetOrigin()
        direction = nii_sitk.GetDirection()
        resample_array = self.resample_image(nii_sitk, new_spacing=[1, 1, 1])

        return {
            "data_array": data_array,
            "spacing": spacing,
            "origin": origin,
            "direction": direction,
            "original_path": path,
            "resample_array": resample_array,
        }
