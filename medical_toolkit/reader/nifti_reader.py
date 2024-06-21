import SimpleITK as sitk
from medical_toolkit.reader.base_reader import BaseReader
from medical_toolkit.utils.extensions import NIFTI_EXT


__all__ = ["NiftiReader"]

class NiftiReader(BaseReader):
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
        sitk_reader = sitk.ReadImage(path, imageIO="NiftiImageIO")
        data_array = sitk.GetArrayFromImage(sitk_reader)
        return {"data_array": data_array}
