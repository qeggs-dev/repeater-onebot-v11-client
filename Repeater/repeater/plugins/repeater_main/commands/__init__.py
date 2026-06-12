import os as _os
import pkgutil as _pkgutil
import importlib as _importlib
from ..logger import logger as _logger

_package_path = _os.path.dirname(__file__)
_package = __name__
_subpackages = []

for _, _module_name, _ in _pkgutil.iter_modules([_package_path]):
    try:
        if _module_name.startswith("_"):
            continue
        _subpackages.append(_module_name)
        _importlib.import_module("." + _module_name, package = _package)
    except Exception as e:
        _logger.exception(
            "Import error: {error}",
            error = str(e)
        )