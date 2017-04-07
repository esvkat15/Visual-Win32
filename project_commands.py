import sublime, sublime_plugin, os, hashlib

oldprint = print
print = sublime.message_dialog # sublime wont let me just print shit

command_path = "C:\\Windows\\System32\\sublime\\"
flags = ["/c"]
sflags = ["/Fa"]

def ifext(ext, view):

	return view is not None and view.file_name() is not None and view.file_name().endswith(ext)

def chpro(window):

	s = hashlib.sha1()
	s.update(os.path.split(window.active_view().file_name())[0].encode())
	n = "C:\\Windows\\Temp\\subl\\" + s.hexdigest() + ".txt"
	cmd = ["md", os.path.split(n)[0], "2>", "nul", "&", "tasklist", "/FI", "IMAGENAME eq main.exe", "/FI", "SESSIONNAME eq Console", ">", n]
	window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})
	while True:

		s = None
		try:

			s = os.stat(n).st_size

		except:

			continue

		else:

			if s is 0:

				continue

			break

	with open(n) as f:

		s = f.read()
		
	cmd = ["del", n]
	window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})
	return s

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view()) or ifext(".asm", self.window.active_view())

	def run(self):

		self.window.run_command("save_all")
		# cmd = ["taskkill", "/IM", "main.exe", "2>", "nul"]
		# window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})



class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		self.window.run_command("save")
		c = None
		if ifext(".c", self.window.active_view()):

			c = "c"

		if ifext(".asm", self.window.active_view()):

			c = "m"

		if c:

			cmd = [command_path + c + "l.bat"] + flags + [self.window.active_view().file_name()]
			self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

		if 'INFO: No tasks are running which match the specified criteria.' in chpro(self.window):

			self.window.run_command("to_exe")



class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view())

	def run(self):

		self.window.run_command("save")
		filename = self.window.active_view().file_name()
		cmd = [command_path + "cl.bat"] + flags + sflags + [filename, "&", command_path + "subl.exe", filename.replace(".c", ".asm")]
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})


print = oldprint