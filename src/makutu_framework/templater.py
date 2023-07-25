from jinja2 import Template

from .utils import get_path_to_file


def render(template_name: str, **kwargs):
    """
    Args:
        template_name (str): template file name
        kwargs (dict): template variables
    Returns:
        str: rendered template
    """

    with open(get_path_to_file(template_name), encoding="utf-8") as template_file:
        template = Template(template_file.read())

    return template.render(**kwargs)
