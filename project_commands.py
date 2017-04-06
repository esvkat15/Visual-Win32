import sublime, sublime_plugin, os, hashlib

command_path = "C:\\Windows\\System32\\sublime\\"
flags = ["/c"]
sflags = ["/Fa"]

def ifext(ext, view):

	return view is not None and view.file_name() is not None and view.file_name().endswith(ext)

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view()) or ifext(".asm", self.window.active_view())

	def run(self):

		self.window.run_command("save_all")
		#taskkill /IM "path\main.exe" 2> nul
		s = hashlib.sha1()
		s.update(os.path.split(self.window.active_view().file_name())[0])
		n = "C:\\Windows\\Temp\\" + s.hexdigest() + ".txt"
		cmd = ["tasklist", "/FI", "SESSIONNAME eq Console", "|", "findstr", "main.exe", ">", n]
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})
		with open(n) as f:

			sublime.error_message(f.readline())

		cmd = ["del", n]
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})


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
			self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$"})



class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view())

	def run(self):

		self.window.run_command("save")
		filename = self.window.active_view().file_name()
		cmd = [command_path + "cl.bat"] + flags + sflags + [filename, "&", command_path + "subl.exe", filename.replace(".c", ".asm")]
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$"})

