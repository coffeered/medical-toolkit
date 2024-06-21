import numpy as np
import pytest

from medical_toolkit.utils.normalization import (
    normalize_min_max,
    normalize_percentile,
    standardize_z_score,
)


@pytest.fixture
def example_image():
    # Example numpy array for testing
    return np.asarray([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype="float32").reshape([1, 3, 3])


def test_normalize_min_max(example_image):
    normalized_image = normalize_min_max(example_image)
    expected_min_max_normalized = np.array(
        [[[0.0, 0.125, 0.25], [0.375, 0.5, 0.625], [0.75, 0.875, 1.0]]]
    )
    np.testing.assert_almost_equal(normalized_image, expected_min_max_normalized)


def test_normalize_percentile(example_image):
    normalized_image = normalize_percentile(example_image, 10, 90)
    expected_percentile_normalized = np.array(
        [[[0.0, 0.03125, 0.1875], [0.34375, 0.5, 0.65625], [0.8125, 0.96875, 1.0]]]
    )
    np.testing.assert_almost_equal(normalized_image, expected_percentile_normalized)


def test_normalize_z_score(example_image):
    normalized_image = standardize_z_score(example_image)
    expected_z_score_normalized = np.array(
        [
            [
                [-1.54919, -1.1619, -0.7746],
                [-0.3873, 0.0, 0.3873],
                [0.7746, 1.1619, 1.54919],
            ]
        ]
    )
    np.testing.assert_almost_equal(
        normalized_image, expected_z_score_normalized, decimal=5
    )
