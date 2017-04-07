import sublime, sublime_plugin, os, hashlib

subl_print = sublime.message_dialog

def cmexe(c, w):

	w.run_command("exec", {"cmd": c, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

def ifext(e, v):

	return v and v.file_name() and v.file_name().endswith(e)

def chpro(w):

	s = hashlib.sha1()
	s.update(os.path.split(w.active_view().file_name())[0].encode())
	n = "C:\\Windows\\Temp\\subl\\" + s.hexdigest() + ".txt"
	cmd = ["md", os.path.split(n)[0], "2>", "nul", "&", "tasklist", "/FI", "IMAGENAME eq main.exe", "/FI", "SESSIONNAME eq Console", ">", n]
	cmexe(cmd, w)
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
	cmexe(cmd, w)
	return s

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view()) or ifext(".asm", self.window.active_view())

	def run(self):

		self.window.run_command("save_all")
		filename = os.path.split(self.window.active_view().file_name())[0] + "\\main.exe"
		cmd = ["taskkill", "/F", "/IM", "main.exe", "2>&1", ">", "nul", "&", "C:\\Windows\\System32\\sublime\\link.bat", "/OUT:" + filename, filename.replace( "\\main.exe", "\\*.obj"), "&", filename]
		cmexe(cmd, self.window)


class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		self.window.run_command("save")
		#c = None
		if ifext(".c", self.window.active_view()):

			c = "c"

		if ifext(".asm", self.window.active_view()):

			c = "m"

		if c:

			cmd = ["C:\\Windows\\System32\\sublime\\%sl.bat" % c, "/c", self.window.active_view().file_name()]
			cmexe(cmd, self.window)
			if not "INFO: No tasks are running which match the specified criteria." in chpro(self.window):

				self.window.run_command("to_exe")




class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return ifext(".c", self.window.active_view())

	def run(self):

		self.window.run_command("save")
		filename = self.window.active_view().file_name()
		cmd = ["C:\\Windows\\System32\\sublime\\cl.bat", "/c", "/Fa", filename, "&", "C:\\Windows\\System32\\sublime\\subl.exe", filename.replace(".c", ".asm")]
		cmexe(cmd, self.window)

