from saberx.executers.groupexecuter import GroupExecuter
import threading

class ThreadExecuter:
    def __init__(self, **kwargs):
        self.__groups = kwargs.get("groups")
        self.__lock = threading.Lock()
