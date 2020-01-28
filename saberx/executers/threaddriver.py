"""
.. module:: threaddriver
   :synopsis: Module for spawning threads and executing groups.
"""

from saberx.executers.groupexecuter import GroupExecuter
import threading
import os


class ThreadExecuter:

    """
        **Class for spawning and managing threads for executing groups**
    """

    def __init__(self, **kwargs):

        """
            **Init method to initialise the object created from this class.**
        """
        self.__groups = kwargs.get("groups")
        self.__lock = threading.Lock()
        self.__workers = []
        self.__logger = kwargs.get("logger")

    def __aquire_lock(self):

        """
            **Method to aquire lock**

            This method is called to aquire lock before the threads are spwaned.
            The lock verifies that the previuos run has ended completely before
            the next run begins

            Returns:
                bool : Successfully aquired lock or not.
        """
        try:

            # try to aquire the lock only if there is no existing lock
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

        """
            **Method to release lock**

            This method is used to release a aquired lock. After all the threads have finished
            their work, this method is called to release the lock.

            Returns:
                bool : Successfully released the lock or not
        """
        try:
            if os.path.exists(self.__lock_file):
                os.unlink(self.__lock_file)
            return True
        except Exception as e:
            if self.__logger:
                self.__logger.critical("Unable to release lock file : Exception : {}".format(str(e)))
            return False
    
    def __worker(self, group_id, group, logger):

        """
            **Method to execute a group of actions**

            This function is the target of the thread spawned. Each thread calls this
            method and assigns a given group to it.

            Args:
                group_id (Integer) : Id of the group
                group (dict) : Dict representing groups
                logger (logging object) : logging object

            Returns:
                None : Returns nothing
        """
        group_status = GroupExecuter.execute_group(group=group, thread_lock=self.__lock, logger=logger)

    def spawn_workers(self, lock_file):

        """
            ** Method to spawn threads**

            This method is used to spawn new threads to execute groups.
            Each thread calls the __worker fuction as target with a given group.

            Args:
                lock_file (string) : Path to lock file

            Returns;
                bool: Threads spawned and executed successfully or not.
        """
        self.__lock_file = lock_file

        # First try to aquire lock
        if self.__aquire_lock():

            # Iterate over the groups and spawn a thread for each group
            for group_index, group in enumerate(self.__groups):
                worker = threading.Thread(target=self.__worker, args=(group_index, group, self.__logger))
                self.__workers.append(worker)
                worker.start()

            for worker in self.__workers:
                worker.join()

            # release lock when everything is done
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
