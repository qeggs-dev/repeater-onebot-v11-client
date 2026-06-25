import warnings

from typing import TextIO
from loguru import logger

class WarningHandler:
    """Warning Handler"""
    def __init__(self) -> None:
        self.raw_showwarning = warnings.showwarning
    
    def inject(self) -> None:
        warnings.showwarning = self.warning_handler
    
    def recovery(self) -> None:
        warnings.showwarning = self.raw_showwarning
    
    def warning_handler(
            self,
            message: Warning | str,
            category: type[Warning],
            filename: str,
            lineno: int,
            file: TextIO | None = None,
            line: str | None = None
        ) -> None:
        logger.warning(
            "[{line}] {message}",
            line = lineno,
            message = message
        )