import sublime
import sublime_plugin
import os

command_path = "C:\\Windows\\System32\\sublime\\"
flags = ["/c"]
sflags = ["/Fa"]

def ifext(ext, view):

	return view is not None and view.file_name() is not None and view.file_name().endswith(ext)

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view()) or ifext(".asm", self.window.active_view())

	def run(self):

		self.window.run_command("save_all") #taskkill /IM "path\main.exe" 2> nul
		filename = self.window.active_view().file_name()
		t = os.path.split(filename)[0] + '\\' + "new.txt"
		cmd = ["tasklist", "/v" > t]
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$"})
		with open(t) as f:
			sublime.error_message(f.readline())


class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		self.window.run_command("save")
		if ifext(".c", self.window.active_view()):
			c = 'c'
		if ifext(".asm", self.window.active_view()):
			c = 'm'
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

