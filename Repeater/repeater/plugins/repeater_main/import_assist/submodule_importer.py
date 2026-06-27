import os
import sys
import inspect
import pkgutil
import importlib
from typing import Any, Generator, Callable
from types import ModuleType
from ..logger import logger
from ..client_configs import storage_configs

class SubmoduleImporter:
    """
    Import submodules recursively from a package.

    Usage:

        >>> importer = SubmoduleImporter()
        >>> importer.import_pkgs(
        ...     lambda: x = not x.startswith("_"),
        ... )
        >>> importer.inject_modules() # Optional, because the program already registers these variables at import time.
    """

    def __init__(self):
        caller_globals, caller_locals = self._get_caller_variables()

        caller_name = caller_globals.get("__name__", None)
        if caller_name is None:
            raise RuntimeError("No caller name found")
        elif not isinstance(caller_name, str):
            raise RuntimeError("Caller name is not a string")
        self.caller_name: str = caller_name
        
        caller_file = caller_globals.get("__file__", None)
        if caller_file is None:
            raise RuntimeError("No caller file found")
        elif not isinstance(caller_file, str):
            raise RuntimeError("Caller file is not a string")
        self.caller_file: str = caller_file
       
        self.package_path: str = os.path.dirname(self.caller_file)
        self.package: str = self.caller_name
        self.subpackages: list[str] = []
        self.modules: list[ModuleType] = []
    
    def import_pkgs_iter(self, name_filter: Callable[[str], bool] = lambda x: not x.startswith("_")) -> Generator[ModuleType, None, None]:
        """
        Iterate over all subpackages and modules in the package.
        """
        for _, module_name, _ in pkgutil.iter_modules([self.package_path]):
            try:
                if name_filter(module_name):
                    self.subpackages.append(module_name)
                    module = importlib.import_module("." + module_name, package = self.package)
                    self.modules.append(module)
                    yield module
            except Exception as e:
                logger.exception(
                    "Import error: {error}",
                    error = str(e)
                )
                if not storage_configs.loading.continue_on_error:
                    raise

    def import_pkgs(self) -> list[ModuleType]:
        """
        Import all subpackages and modules in the package.
        """
        models: list[ModuleType] = []
        for module in self.import_pkgs_iter():
            models.append(module)
        return models
    
    def model_names_iter(self) -> Generator[str, None, None]:
        """
        Iterate over the name of the module that has been imported.
        """
        for module in self.modules:
            if module.__package__:
                yield module.__package__
            else:
                if module.__name__.startswith(self.caller_name + "."):
                    module_name = module.__name__.removeprefix(self.caller_name + ".")
                else:
                    module_name = module.__name__
                yield module_name
    
    def inject_modules(self) -> None:
        """
        Injects the imported module into the context.
        """
        caller_globals, caller_locals = self._get_caller_variables()

        caller_name = caller_globals.get("__name__", None)
        if caller_name is None:
            raise RuntimeError("No caller name found")
        elif not isinstance(caller_name, str):
            raise RuntimeError("Caller name is not a string")
        
        current_module = sys.modules[caller_name]
        for module_name, module in zip(self.model_names_iter(), self.modules):
            setattr(current_module, module_name, module)
    
    def all_list(self) -> list[str]:
        all_list: list[str] = []
        for module_name in self.model_names_iter():
            all_list.append(module_name)
        return all_list
    
    @staticmethod
    def _get_caller_variables() -> tuple[dict[str, Any], dict[str, Any]]:
        """
        Gets the caller's variables.
        """
        frame = inspect.currentframe()
        if frame is None:
            raise RuntimeError("Not found frame")
        
        f_back = frame.f_back
        if f_back is None:
            raise RuntimeError("This method frame is not found")
        
        f_double_back = f_back.f_back
        if f_double_back is None:
            raise RuntimeError("Caller frame is not found")
        
        caller_globals = f_double_back.f_globals
        caller_locals = f_double_back.f_locals

        return caller_globals, caller_locals