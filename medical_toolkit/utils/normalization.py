import numpy as np

__all__ = [
    "normalize_min_max",
    "normalize_percentile",
    "standardize_z_score",
]


def _normalize(image: np.ndarray, min_val: float, max_val: float) -> np.ndarray:
    """
    Helper function to normalize the image using provided min and max values.

    Parameters:
    - image (np.ndarray): The input image to be normalized.
    - min_val (float): The minimum value for normalization.
    - max_val (float): The maximum value for normalization.

    Returns:
    - np.ndarray: The normalized image.
    """
    if min_val == max_val:
        return np.zeros_like(image, dtype="float32")  # Avoid division by zero
    normalized_image = (image - min_val) / (max_val - min_val)
    return np.clip(normalized_image, 0, 1)  # Ensure the result is in range [0, 1]


def normalize_min_max(image: np.ndarray) -> np.ndarray:
    """
    Normalize the given image using Min-Max normalization.

    Parameters:
    - image (np.ndarray): The input image to be normalized.

    Returns:
    - np.ndarray: The normalized image.
    """
    min_val = np.nanmin(image)
    max_val = np.nanmax(image)
    return _normalize(image, min_val, max_val)


def normalize_percentile(
    image: np.ndarray, min_percentile: float, max_percentile: float
) -> np.ndarray:
    """
    Normalize the given image using percentile normalization.

    Parameters:
    - image (np.ndarray): The input image to be normalized.
    - min_percentile (float): The minimum percentile value.
    - max_percentile (float): The maximum percentile value.

    Returns:
    - np.ndarray: The normalized image.
    """
    min_val = np.nanpercentile(image, min_percentile)
    max_val = np.nanpercentile(image, max_percentile)
    return _normalize(image, min_val, max_val)


def standardize_z_score(image: np.ndarray) -> np.ndarray:
    """
    Normalize the given image using Z-score normalization.

    Parameters:
    - image (np.ndarray): The input image to be normalized.

    Returns:
    - np.ndarray: The normalized image.
    """
    mean_val = np.nanmean(image)
    std_val = np.nanstd(image)
    if std_val == 0:
        return np.zeros_like(image, dtype="float32")  # Avoid division by zero
    standardize_image = (image - mean_val) / std_val
    return standardize_image
