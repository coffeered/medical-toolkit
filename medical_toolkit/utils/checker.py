import puremagic


def check_file_extension(file_path: str = None):
    """
    Check the file extension using both filename extension and magic bytes.

    Parameters:
    file_path (str): The path to the file whose extension needs to be checked.

    Returns:
    dict: A dictionary containing two keys:
        - 'filename_extension' (str): The extension derived from the filename.
        - 'magic_extensions' (list): A list of tuples where each tuple contains:
            - Extension guessed from magic bytes.
            - Confidence level of the guessed extension.
    """

    if file_path is None:
        raise ValueError("file_path cannot be None")

    filename_extension = puremagic.from_file(file_path)
    elements = puremagic.magic_file(file_path)

    magic_extensions = [(None, None)] * len(elements)
    for idx, element in enumerate(elements):
        magic_extensions[idx] = (element.extension, element.confidence)

    return {
        "filename_extension": filename_extension,
        "magic_extensions": magic_extensions,
    }
