import psutil
import subprocess
import re

class ProcessHandler:

	@staticmethod
	def check_name_and_count(regex):
		pattern = re.compile(regex)
		count = 0

		for proc in psutil.process_iter(attrs=['name']):
			proc_name = proc.info['name']
			if pattern.search(proc_name):
				count += 1

		return count

	@staticmethod
	def check_cmdline_count(regex):
		command = 'ps aux | grep {} | grep -v grep | wc -l'

		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		proc_exit_code = proc.returncode
		output, errors = proc.communicate()

		if proc_exit_code != 0:
			return False, errors, proc_exit_code

		return True, output, proc_exit_code
