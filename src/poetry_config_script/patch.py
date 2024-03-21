import importlib

from poetry.core.pyproject.toml import PyProjectTOML


patched_attr = "poetry_config_patched"


def patch():
    patched = getattr(PyProjectTOML, patched_attr, False)

    if patched:
        return

    poetry_config_unpatched = getattr(PyProjectTOML, "poetry_config")

    class PropertyPatch:

        def __get__(self, obj, obj_type=None):
            config = poetry_config_unpatched.__get__(obj)

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

        def __set__(self, obj, val):
            raise Exception("Not implemented")
            # self(val)

    mock = PropertyPatch()
    setattr(PyProjectTOML, "poetry_config", mock)
    setattr(PyProjectTOML, patched_attr, True)
