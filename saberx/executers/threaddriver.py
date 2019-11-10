from saberx.executers.groupexecuter import GroupExecuter
import threading
import os

class ThreadExecuter:
    def __init__(self, **kwargs):
        self.__groups = kwargs.get("groups")
        self.__lock = threading.Lock()
        self.__workers = []
        self.__logger = kwargs.get("logger")

    def __aquire_lock(self):
        try:
            if not os.path.exists(self.__lock_file):
                with open(self.__lock_file, "w") as lock_file:
                    lock_file.write(str(os.getpid()))
                return True
            return False
        except Exception as e:
            if self.__logger:
                self.__logger.critical("Unable to aquire lock file : Exception : {}".format(str(e)))
            return False

    def __release_lock(self):
        try:
            if os.path.exists(self.__lock_file):
                os.unlink(self.__lock_file)
            return True
        except Exception as e:
            if self.__logger:
                self.__logger.critical("Unable to release lock file : Exception : {}".format(str(e)))
            return False
    
    def __worker(self, group_id, group, logger):
        print ("first thread")
        group_status = GroupExecuter.execute_group(group=group, thread_lock=self.__lock, logger=logger)

    def spawn_workers(self, lock_file):
        self.__lock_file = lock_file

        if self.__aquire_lock():
            for group_index, group in enumerate(self.__groups):
                worker = threading.Thread(target=self.__worker, args=(group_index, group, self.__logger))
                self.__workers.append(worker)
                worker.start()

            for worker in self.__workers:
                worker.join()
            lock_released = self.__release_lock()
            if not lock_released:

                '''
                    Log lock issue. The lock must be released at this step or else
                    future runs wont take place. Issue must be fixed why lock is not
                    being released.
                '''

                if self.__logger:
                    self.__logger.critical("Lock could not be released. This needs to be fixed for future runs")

                return False

            # Run succeeded
            return True

        # could not aquire lock, so run wont take place. Hence send false
        return False
