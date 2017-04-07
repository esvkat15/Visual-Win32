import sublime, sublime_plugin, os, hashlib

# subl_print = sublime.message_dialog

def cmexe(w, c):

	w.run_command("exec", {"cmd": c, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

def chext(v):

	n = v.file_name()
	return v and n and (n.endswith(".asm") or n.endswith(".c")) and n[-1]

def chpro(w):

	s = hashlib.sha1()
	s.update(os.path.split(w.active_view().file_name())[0].encode())
	n = "C:\\Windows\\Temp\\subl\\" + s.hexdigest() + ".txt"
	cmexe(w, ["md", os.path.split(n)[0], "2>", "nul", "&", "tasklist", "/FI", "IMAGENAME eq main.exe", "/FI", "SESSIONNAME eq Console", ">", n])
	while True:

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
		
	cmexe(w, ["del", n])
	return s

class ToExeCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return chext(self.window.active_view()) and True

	def run(self):

		w = self.window
		w.run_command("save_all")
		n = os.path.split(w.active_view().file_name())[0] + "\\main.exe"
		cmexe(w, ["taskkill", "/F", "/IM", "main.exe", "2>&1", ">", "nul"])
		w.run_command("to_obj")
		cmexe(w, ["C:\\Windows\\System32\\sublime\\link.bat", "/OUT:" + n, n.replace( "\\main.exe", "\\*.obj"), "&", n])


class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		w = self.window
		v = w.active_view()
		w.run_command("save")
		if chext(v):

			cmexe(w, ["C:\\Windows\\System32\\sublime\\%sl.bat" % chext(v), "/c", v.file_name()])
			if "INFO: No tasks are running which match the specified criteria." not in chpro(w):

				w.run_command("to_exe")
				



class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return chext(self.window.active_view()) is "c"

	def run(self):

		w = self.window
		w.run_command("save")
		n = w.active_view().file_name()
		cmexe(w, ["C:\\Windows\\System32\\sublime\\cl.bat", "/c", "/Fa", n])
		w.open_file(n.replace(".c", ".asm"))
		#cmexe(w, ["C:\\Windows\\System32\\sublime\\subl.exe", n.replace(".c", ".asm")])

