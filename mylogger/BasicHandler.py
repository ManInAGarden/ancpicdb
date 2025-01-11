class BasicHandler():
    def __init__(self):
        self._isactive = True
        self._lb = "\n"

    @property
    def isactive(self):
        return self._isactive

    def set_active(self, state : bool):
        self._isactive = state

    def activate(self):
        self._isactive = True

    def deactivate(self):
        self._isactive = False
        
    def write(self, msg):
        """must be overriden in any derived class"""
        raise NotImplementedError