from os.path import abspath, dirname, join


def get_path_to_file(path: str) -> str:
    """
    Args:
        path (str): relative path to file
    Returns:
        str: path to templates folder
    """
    return abspath(join(dirname(__file__), "../templates", path.lstrip("/")))


def get_template_folder() -> str:
    """
    Returns:
        str: path to templates folder
    """
    return abspath(join(dirname(__file__), "../templates"))
