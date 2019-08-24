from saberx.executers.groupexecuter import GroupExecuter
import threading
import os

class ThreadExecuter:
    def __init__(self, **kwargs):
        self.__groups = kwargs.get("groups")
        self.__lock = threading.Lock()
        self.__workers = []

    def __aquire_lock(self):
        try:
            if not os.path.exists("/run/saberx/saberx.lock"):
                with open("/run/saberx/saberx.lock", "w") as lock_file:
                    lock_file.write(os.getpid())
            return True
        except Exception as e:
            return False

    def __release_lock(self):
        try:
            if os.path.exists("/run/saberx/saberx.lock"):
                os.unlink("/run/saberx/saberx.lock")
            return True
        except Exception as e:
            return False
    
    def __worker(self, group_id, group):
        group_status = GroupExecuter.execute_group(group=group, thread_lock=self.__lock)

    def spawn_workers(self):
        for group_index, group in enumerate(self.__groups):
            worker = threading.Thread(self.__worker, group_index, group)
            self.__workers.append(worker)
            worker.start()

        for worker in self.__workers:
            worker.join()
