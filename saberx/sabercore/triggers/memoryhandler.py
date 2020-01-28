"""
.. module:: memoryhandler
   :synopsis: Module for performing the memory trigger operation.
"""

import os
import psutil


class MemoryHandler:

    """
        **Class for handling memory trigger operation**
    """

    @staticmethod
    def __operate(current, count, operator):

        """
            **Method for comparing given count with current memory metric 
            value.**

            This method takes the current value and the threshold for memory 
            metric and performs the desired operation.

            Args:
                current (Float) : Current value of memory metric
                count (Float) : Given value
                operator (string) : Given operator

            Returns:
                bool : Opeartion returned true or false
        """
        return {
            '=': lambda current, count: current == count,
            '<': lambda current, count: current < count,
            '>': lambda current, count: current > count,
            '<=': lambda current, count: current <= count,
            '>=': lambda current, count: current >= count
        }.get(operator)(current, count)

    @staticmethod
    def get_mem_type(check):

        """
            **Method for getting metric type from trigger check**

            This method accepts the check type and returns the desired
            method to get the value of the metric specified in type.

            Args:
                check (string): Type of check : virtial | swap

            Returns:
                psutil method : psutl method to get virtual or swap memory 
                values.
        """

        MEM_TYPES = {
            "virtual": psutil.virtual_memory,
            "swap": psutil.swap_memory
        }

        return MEM_TYPES.get(check)

    @staticmethod
    def check_mem(**kwargs):

        """
            **Method to perform the memory operation**

            This method accpets the trigger attributes, performs the
            specified operation and returns the trigger status.

            Args:
                kwargs (dict): Contains all check attributes

            Returns:
                bool : trigger status - fire or not
        """

        check_type = kwargs.get("check_type")
        attr = kwargs.get("attr")
        threshold = kwargs.get("threshold")
        operator = kwargs.get("operation")

        check = MemoryHandler.get_mem_type(check_type)

        metrics = check()
        attr_val = getattr(metrics, attr)

        check_result = MemoryHandler.__operate(attr_val, threshold, operator)

        return check_result, None


if __name__ == "__main__":
    print(MemoryHandler.check_mem(
        check_type="swap", attr="free", threshold=1, operator=">"))
