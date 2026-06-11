from .base import RepeaterException

class RepeaterCommandException(RepeaterException):
    """
    Repeater Command Base Exception
    """
    pass

class ProcessControlException(RepeaterCommandException):
    """
    Process Control Exception
    """
    pass

class BreakHandler(ProcessControlException):
    """
    Break Handler Exception
    """
    pass

class ExitHandler(ProcessControlException):
    """
    Exit Handler Exception
    """
    pass

class BreakWithErrorMessage(BreakHandler):
    """
    Break Handler Exception with Error Message
    """
    pass

class ExitWithErrorMessage(ExitHandler):
    """
    Exit Handler Exception with Error Message
    """
    pass