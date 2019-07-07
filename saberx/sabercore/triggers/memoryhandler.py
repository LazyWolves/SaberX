import os
import psutil

class MemoryHandler:

    @staticmethod
    def __operate(current, count, operator):
        return {
            '=': lambda current, count: current == count,
			'<': lambda current, count: current < count,
			'>': lambda current, count: current > count,
			'<=': lambda current, count: current <= count,
			'>=': lambda current, count: current >= count
		}.get(operator)(current, count)

    @staticmethod
    def get_mem_type(check):

        MEM_TYPES = {
            "virtual": psutil.virtual_memory,
            "swap": psutil.swap_memory
        }

        return MEM_TYPES.get(check)

    @staticmethod
    def check_mem(**kwargs):

        check_type = kwargs.get("check_type")
        attr = kwargs.get("attr")
        threshold = kwargs.get("threshold")
        operator = kwargs.get("operator")

        check = MemoryHandler.get_mem_type(check_type)

        metrics = check()
        attr_val =  getattr(metrics, attr)

        check_result = MemoryHandler.__operate(attr_val, threshold, operator)

        return check_result, None

if __name__ == "__main__":
    print (MemoryHandler.check_mem(check_type="swap", attr="free", threshold=1, operator=">"))
