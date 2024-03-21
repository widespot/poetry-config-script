import importlib


def patch_class_property(klass, property_name, getter, patch_flag_name=None):
    if patch_flag_name is None:
        patch_flag_name = f"{property_name}_patched"

    patched = getattr(klass, patch_flag_name, False)

    if patched:
        return

    unpatched_property = getattr(klass, property_name)

    class PropertyPatch:
        def __get__(self, obj, obj_type=None):
            return getter(unpatched_property.__get__(obj))

        def __set__(self, obj, val):
            raise Exception("Not implemented")

    mock = PropertyPatch()
    setattr(klass, property_name, mock)
    setattr(klass, patch_flag_name, True)
