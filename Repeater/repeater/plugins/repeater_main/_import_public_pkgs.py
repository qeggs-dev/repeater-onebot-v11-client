import os
import sys
import inspect
import pkgutil
import importlib
from typing import Any, Generator
from types import ModuleType
from .logger import logger
from .client_net_configs import storage_configs

class ImportPublicPkgs:
    """Import public packages"""

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
    
    def import_pkgs_iter(self) -> Generator[ModuleType, None, None]:
        for _, module_name, _ in pkgutil.iter_modules([self.package_path]):
            try:
                if module_name.startswith("_"):
                    continue
                self.subpackages.append(module_name)
                module = importlib.import_module("." + module_name, package = self.package)
                self.modules.append(module)
                yield module
            except Exception as e:
                logger.exception(
                    "Import error: {error}",
                    error = str(e)
                )
                if not storage_configs.continue_on_error:
                    raise

    def import_pkgs(self) -> list[ModuleType]:
        models: list[ModuleType] = []
        for module in self.import_pkgs_iter():
            models.append(module)
        return models
    
    def model_names_iter(self) -> Generator[str, None, None]:
        for module in self.modules:
            if module.__name__.startswith(self.caller_name + "."):
                module_name = module.__name__.removeprefix(self.caller_name + ".")
            else:
                module_name = module.__name__
            yield module_name
    
    def inject_modules(self) -> None:
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