class BaseReader:
    def __init__(self):
        self.order = None

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
                data["data_array"] = normalize_z_score(data["data_array"])
            elif normalization == "percentile":
                data["data_array"] = normalize_percentile(data["data_array"])
            else:
                raise ValueError(f"Invalid normalization method: {normalization}")
        return data

    def __call__(self, path: str, check: bool = False, normalization: str = None) -> dict:
        """
        Execute the reader, optionally checking for validity and applying normalization.

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
        data = self.normalization(data, normalization)
        return data