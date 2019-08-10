import os

class CPUHandler:

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
    def check_loadavg(**kwargs):

        thresholds = kwargs.get("thresholds")
        operation = kwargs.get("operation")

        loadavg = os.getloadavg()

        final_result = True
        index = 0

        for value in thresholds:
            final_result = final_result and CPUHandler.__operate(loadavg[index], value, operation)
            index += 1
        
        return final_result, None

if __name__ == "__main__":
    print (CPUHandler.check_loadavg(thresholds=[10.0, 1.0], operation="<"))
