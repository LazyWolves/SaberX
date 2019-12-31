"""
.. module:: processhandler
   :synopsis: Module for evaluating process trigger.
"""

import psutil
import subprocess
import re

class ProcessHandler:

    """
        **Class for performing process trigger operation
    """

    @staticmethod
    def get_name_count(regex):

        """
            **Method for getting count of process**

            This method returns the count of processes whose
            name matches the given regex

            Args:
                regex (string): String containing regex for filtering process names

            Returns:
                bool, Integer, String : status, count, error if any
        """
        pattern = re.compile(regex)
        count = 0

        try:

            # loop over all the processes fetched via psutil
            for proc in psutil.process_iter(attrs=['name']):
                proc_name = proc.info['name']

                # filter them using the regex
                if pattern.search(proc_name):
                    count += 1

            return True, count, None
        except Exception:
            '''
                Log error
            '''

            return False, None, "CANNOT_ACCESS_PROCESS_NAMES"

    @staticmethod
    def get_cmdline_count(regex):

        """
            **Method for getting count of process**

            This method returns the count of processes whose
            cmdline matches the given regex

            Args:
                regex (string): String containing regex for filtering process cmdline

            Returns:
                bool, Integer, String : status, count, error if any
        """

        # command for getting all processes in the system filtered
        # by the process name
        command = 'ps aux | grep -E "{}" | grep -v grep | wc -l'.format(regex)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        output, errors = proc.communicate()
        proc_exit_code = proc.returncode
        if proc_exit_code != 0:
            return False, None, "CANNOT_ACCESS_PROCESSES"

        output = int(output.strip())

        return True, output, None

    @staticmethod
    def check_name(regex):

        """
            **Method for checking if a process exists by name**

            This method checks if there is any process whose name matches the
            given pattern

            Args:
                regex (string): String containing regex

            Returns:
                bool, Integer, String : status, count, error if any
        """
        response, count, error = ProcessHandler.get_name_count(regex)

        if error:
            return False, error

        if count != 0:
            return True, None

        return False, None

    @staticmethod
    def check_cmdline(regex):
        """
            **Method for checking if a process exists by cmdline text**

            This method checks if there is any process whose cmdline arg matches the
            given pattern

            Args:
                regex (string): String containing regex

            Returns:
                bool, Integer, String : status, count, error if any
        """
        response, count, error = ProcessHandler.get_cmdline_count(regex)

        if error:
            return False, error

        if count != 0:
            return True, None

        return False, None

    @staticmethod
    def __operate(current, count, operator):

        """
            **Method to evaluate the required operation**

            Args:
                current (Integer) : Current number of processes filtered by the given regex
                count (Integer) : Desired threshold
                operator (String) : The operation to be performed

            Returns:
                bool: Result of the operattion
        """
        return {
            '=': lambda current, count: current == count,
            '<': lambda current, count: current < count,
            '>': lambda current, count: current > count,
            '<=': lambda current, count: current <= count,
            '>=': lambda current, count: current >= count
        }.get(operator)(current, count)

    @staticmethod
    def check_name_count(regex, count, operator):

        """
            **Method to get the Number of regex filtered processes and perform the deired operation**

            Args:
                regex (string): Regex to filter processes
                count (string): Threshold
                operation (string): Desired operation

            Returns:
                bool, string : Result, error if any
        """
        response, current, error = ProcessHandler.get_name_count(regex)

        if error:
            return False, error

        operation_result = ProcessHandler.__operate(current, count, operator)

        return operation_result, None

    @staticmethod
    def check_cmdline_count(regex, count, operator):

        """
            **Method to get the Number of regex filtered processes by cmd and perform the deired operation**

            Args:
                regex (string): Regex to filter processes
                count (string): Threshold
                operation (string): Desired operation

            Returns:
                bool, string : Result, error if any
        """
        response, current, error = ProcessHandler.get_cmdline_count(regex)

        if error:
            return False, error

        operation_result = ProcessHandler.__operate(current, count, operator)

        return operation_result, None


if __name__ == "__main__":
    print (ProcessHandler.check_cmdline_count("/usr/sbin/haproxy", 2, "<="))
