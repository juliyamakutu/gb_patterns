from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from .utils import get_template_folder


def render(template_name: str, **kwargs):
    """
    Args:
        template_name (str): template file name
        kwargs (dict): template variables
    Returns:
        str: rendered template
    """

    env = Environment()
    env.loader = FileSystemLoader(get_template_folder())
    template = env.get_template(template_name)

    return template.render(**kwargs)
