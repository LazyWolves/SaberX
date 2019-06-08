import psutil
import subprocess
import re

class ProcessHandler:

	@staticmethod
	def get_name_count(regex):
		pattern = re.compile(regex)
		count = 0

		try:
			for proc in psutil.process_iter(attrs=['name']):
				proc_name = proc.info['name']
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
		command = 'ps aux | grep {} | grep -v grep | wc -l'

		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		proc_exit_code = proc.returncode
		output, errors = proc.communicate()

		if proc_exit_code != 0:
			return False, None, "CANNOT_ACCESS_PROCESSES"

		return True, output, None

	@staticmethod
	def check_name(regex):
		response, count, error = get_name_count(regex)

		if error:
			return False, error

		if count != 0:
			return True, None

		return False, None

	@staticmethod
	def check_cmdline(regex):
		response, count, error = get_cmdline_count(regex)

		if error:
			return False, error

		if count != 0:
			return True, None

		return False

	@staticmethod
	def check_name_count(regex, count, operation):
		pass

	@staticmethod
	def check_cmdline_count(regex, count, operation):
		pass
