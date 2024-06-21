import numpy as np

__all__ = [
    "normalize_min_max",
    "normalize_percentile",
    "normalize_z_score",
]


def normalize_min_max(image: np.ndarray) -> np.ndarray:
    """
    Normalize the given image using Min-Max normalization.

    Parameters:
        image (np.ndarray): The input image to be normalized.

    Returns:
        np.ndarray: The normalized image.
    """
    min_val = np.nanmin(image)
    max_val = np.nanmax(image)
    normalized_image = (image - min_val) * (1 / (max_val - min_val))
    return normalized_image


def normalize_percentile(
    image: np.ndarray, min_percentile: float, max_percentile: float
) -> np.ndarray:
    """
    Normalize the given image using percentile normalization.

    Parameters:
        image (np.ndarray): The input image to be normalized.
        min_percentile (float): The minimum percentile value.
        max_percentile (float): The maximum percentile value.

    Returns:
        np.ndarray: The normalized image.
    """
    min_val = np.nanpercentile(image, min_percentile)
    max_val = np.nanpercentile(image, max_percentile)
    normalized_image = (image - min_val) * (1 / (max_val - min_val))
    return normalized_image


def normalize_z_score(image: np.ndarray) -> np.ndarray:
    """
    Normalize the given image using Z-score normalization.

    Parameters:
        image (np.ndarray): The input image to be normalized.

    Returns:
        np.ndarray: The normalized image.
    """
    mean_val = np.nanmean(image)
    std_val = np.nanstd(image)
    normalized_image = (image - mean_val) * (1 / std_val)
    return normalized_image
