"""
.. module:: cpuhandler
   :synopsis: Module for evaluating trigger conditions.
"""

import os


class CPUHandler:

    """
        Class for evaluatingcputrigger params
    """

    @staticmethod
    def __operate(current, count, operator):

        """
            **Method for comparing given count with current cpu load everage.**

            Thos metho takes the current value and the threshold for load 
            average and performs the desired operation.

            Args:
                current (Float) : Current value of load average
                count (Float) : Given threshold
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
    def check_loadavg(**kwargs):

        """
            **Method to check loadaverage**

            This method evaluates the trigger param and descied whether the 
            trigger is fired or not.

            Args:
                kwargs (object) : Object containing thresholds and operation

            Returns:
                bool, string : status of the trigger and error string if any
        """

        thresholds = kwargs.get("thresholds")
        operation = kwargs.get("operation")

        loadavg = os.getloadavg()

        final_result = True
        index = 0

        # evaluate the condition for each component of load average
        for value in thresholds:
            final_result = final_result and CPUHandler.__operate(
                loadavg[index], value, operation)
            index += 1

        return final_result, None


if __name__ == "__main__":
    print(CPUHandler.check_loadavg(thresholds=[10.0, 1.0], operation="<"))
