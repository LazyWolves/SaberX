from saberx.executers.groupexecuter import GroupExecuter
import threading
import os

class ThreadExecuter:
    def __init__(self, **kwargs):
        self.__groups = kwargs.get("groups")
        self.__lock = threading.Lock()

    def __aquire_lock()
        try:
            if not os.path.exists("/run/saberx/saberx.lock"):
                with open("/run/saberx/saberx.lock", "w") as lock_file:
                    lock_file.write(os.getpid())
            return True
        except Exception as e:
            return False

    def __release_lock():
        try:
            if os.path.exists("/run/saberx/saberx.lock"):
                os.unlink("/run/saberx/saberx.lock")
            return True
        except Exception as e:
            return False
