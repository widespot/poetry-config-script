import importlib

from poetry.core.pyproject.toml import PyProjectTOML

from poetry_config_script.utils import patch_class_property


def patch_getter(config):
    config_script = config.pop("config_script", None)
    if config_script:
        if not isinstance(config_script, str):
            raise Exception("config_script in tool.poetry section must be a string")

        try:
            [module, method] = config_script.split(":")
        except ValueError:
            raise Exception("config_script must be in format 'module:method'")

        method = getattr(importlib.import_module(module), method)
        config = method.__call__(config)

    return config


def patch():
    patch_class_property(PyProjectTOML, "poetry_config", patch_getter)
