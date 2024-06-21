from medical_toolkit.utils.normalization import (
    normalize_min_max,
    normalize_percentile,
    standardize_z_score,
)
import SimpleITK as sitk


class BaseReader:
    def __init__(self):
        self.extensions = None

    def check_valid(self, path: str) -> bool:
        """
        Check if the given path is valid.

        Parameters:
            path (str): The file path to check.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()

    def read(self, path: str) -> dict:
        """
        Read the data from the given path.

        Parameters:
            path (str): The file path to read.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError()

    def normalization(self, data: dict, normalization: str = None) -> dict:
        """
        Normalize the data array within the provided data dictionary.

        Parameters:
            data (dict): The data dictionary containing the data array.
            normalization (str, optional): The normalization method to use. Defaults to None.

        Returns:
            dict: The data dictionary with the normalized data array.

        Raises:
            ValueError: If the normalization method is invalid.
        """
        if normalization is not None:
            if normalization == "min_max":
                data["data_array"] = normalize_min_max(data["data_array"])
            elif normalization == "z_score":
                data["data_array"] = standardize_z_score(data["data_array"])
            elif normalization == "percentile":
                data["data_array"] = normalize_percentile(data["data_array"])
            else:
                raise ValueError(f"Invalid normalization method: {normalization}")
        return data

    def __call__(
        self, path: str, check: bool = False, normalization: str = None
    ) -> dict:
        """
        Execute the reader, optionally checking for validity and applying
        normalization.

        Parameters:
            path (str): The file path to read.
            check (bool, optional): Whether to check for validity. Defaults to False.
            normalization (str, optional): The normalization method to use. Defaults to None.

        Returns:
            dict: The read and normalized data.
        """
        if check and not self.check_valid(path=path):
            raise ValueError("Invalid file path.")
        data = self.read(path)
        if normalization:
            data = self.normalization(data, normalization)
        return data


class BaseCTMRIReader(BaseReader):
    def __init__(self):
        super().__init__()

    def resample_image(
        self,
        image: sitk.Image,
        new_spacing: tuple,
        interpolator=sitk.sitkLinear,
    ) -> sitk.Image:
        """
        Resample the given SimpleITK image to new spacing.

        Parameters:
            image (sitk.Image): The SimpleITK image to resample.
            new_spacing (tuple): The new spacing to resample the image to, specified as a tuple of
                                 three floats.
            interpolator: The interpolator to use. Defaults to sitk.sitkLinear.

        Returns:
            sitk.Image: The resampled SimpleITK image.
        """
        original_size = image.GetSize()
        original_spacing = image.GetSpacing()

        new_size = [
            int(round(original_size[i] * original_spacing[i] / new_spacing[i]))
            for i in range(3)
        ]

        # Create the resampler
        resampler = sitk.ResampleImageFilter()
        resampler.SetOutputSpacing(new_spacing)
        resampler.SetSize(new_size)
        resampler.SetOutputDirection(image.GetDirection())
        resampler.SetOutputOrigin(image.GetOrigin())
        resampler.SetInterpolator(interpolator)

        # Resample the image
        resampled_sitk = resampler.Execute(image)

        return sitk.GetArrayFromImage(resampled_sitk)
