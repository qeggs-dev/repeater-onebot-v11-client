class SubCmdExit:
    _instance: "SubCmdExit | None" = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {id(self)}>"

class SubCmdBreaked(SubCmdExit):
    pass

class SubCmdCacelled(SubCmdExit):
    pass