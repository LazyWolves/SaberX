import os
import psutil

class MetricHandler:

    @staticmethod
    def __operate(current, count, operator):
        return {
            '=': lambda current, count: current == count,
			'<': lambda current, count: current < count,
			'>': lambda current, count: current > count,
			'<=': lambda current, count: current <= count,
			'>=': lambda current, count: current >= count
		}.get(operator)(current, count)

    

