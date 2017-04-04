import sublime
import sublime_plugin

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		self.window.run_command("save_all")


class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		self.window.run_command("save")


class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		filename = None
		if self.window.active_view():
			filename = self.window.active_view().file_name()
		if filename is None or not filename.endswith(".c"):
			filename = None
		return filename is not None

	def run(self):

		path = "C:\\Windows\\System32\\sublime\\"
		filename = self.window.active_view().file_name()
		flags = ["/c", "/Fa"]
		cmd = [path + "cl.bat"] + flags + [filename, "&", path + "subl.exe", filename.replace(".c",".asm")]
		self.window.run_command("save")
		self.window.run_command("exec", {"cmd": cmd, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$"})

