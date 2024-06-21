import SimpleITK as sitk
from medical_toolkit.reader.base_reader import BaseReader
from medical_toolkit.utils.extensions import DICOM_EXT
from medical_toolkit.utils.checker import check_file_extension


__all__ = ["DicomReader"]

class DicomReader(BaseReader):
    def __init__(self):
        super().__init__()
        self.extensions = DICOM_EXT

    def check_valid(self, path: str) -> bool:
        """
        Check if the given path is a valid DICOM file.

        Parameters:
            path (str): The file path to check.

        Returns:
            bool: True if the path is valid, False otherwise.
        """
        check_results = check_file_extension(path)

        for extension, confidence in check_results["magic_extensions"]:
            if extension in self.extensions:
                return True
        return check_results["filename_extension"] in self.extensions

    def _get_affine(self, img: sitk.Image, lps_to_ras: bool = True) -> dict:
        """
        Get or construct the affine matrix of the image.

        Parameters:
            img (sitk.Image): An ITK image object loaded from an image file.
            lps_to_ras (bool, optional): Whether to convert the affine matrix from "LPS" to "RAS". Defaults to True.

        Returns:
            dict: A dictionary containing the affine matrix, spacing, origin, and direction.
        """
        direction = np.asarray(img.GetDirection())
        spacing = np.asarray(img.GetSpacing())
        origin = np.asarray(img.GetOrigin())

        sr = min(max(direction.shape[0], 1), 3)
        affine: np.ndarray = np.eye(sr + 1)
        affine[:sr, :sr] = direction[:sr, :sr] @ np.diag(spacing[:sr])
        affine[:sr, -1] = origin[:sr]
        if lps_to_ras:
            affine = orientation_ras_lps(affine)
        return {
            "affine": affine,
            "spacing": spacing,
            "origin": origin,
            "direction": direction,
        }

    def read(self, path: str) -> dict:
        """
        Read the DICOM file from the given path.

        Parameters:
            path (str): The file path to read.

        Returns:
            dict: A dictionary containing the data array and affine matrix.
        """
        sitk_reader = sitk.ReadImage(path, imageIO="GDCMImageIO")
        data_array = sitk.GetArrayFromImage(sitk_reader)
        data = {"data_array": data_array} | self._get_affine(sitk_reader)

        return data
