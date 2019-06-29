import subprocess

class ShellExecutor:

	def __init__(self, **kwargs):
		self.command_list = kwargs.get("command_list")
		self.logger = kwargs.get("logger")

	def execute_shell_single(self, command):
		'''
			TODO:
				sanity check
		'''
		proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		output, errors = proc.communicate()
		proc_exit_code = proc.returncode		

		if proc_exit_code != 0:
			return False, errors, proc_exit_code

		return True, output, proc_exit_code

	def execute_shell_list(self):
		for command in self.command_list:

			# log the command being executed

			success, reponse, proc_exit_code = self.execute_shell_single(command)
			if not success:
				# log the response and proc_exit_code
				return False

			# log the response and proc_exit_code

			return True
