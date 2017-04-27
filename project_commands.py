import sublime, sublime_plugin, os, hashlib

subl_print = sublime.message_dialog

def cmexe(w, c):

	w.run_command("exec", {"cmd": ["C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat", "x86", "&"] + c, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

def chext(v):

	n = v.file_name()
	return v and n and (n.endswith(".asm") or n.endswith(".c")) and ("%sl" % n[-1])

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
		cmexe(w, ["link", "/OUT:" + n, n.replace("\\main.exe", "\\*.obj"), "&", n])


class ToObjCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return True

	def run(self):

		w = self.window
		v = w.active_view()
		n = v.file_name()
		w.run_command("save")
		r = chext(v)
		if r:

			cmexe(w, [r, "/c", n()])
			try:

				t = os.stat(n.replace(".*[casm]", ".obj")).st_mtime

			except:

				t = "invalid"

			while True:

				try:

					s = os.stat(n.replace(".*[casm]", ".obj")).st_mtime

				except:

					continue

				else:

					if s in t:

						continue

					subl_print(s)
					subl_print(t)
					break


			if "INFO: No tasks are running which match the specified criteria." not in chpro(w):

				w.run_command("to_exe")
				



class ToAsmCommand(sublime_plugin.WindowCommand):

	def is_enabled(self):

		return "c" in chext(self.window.active_view())

	def run(self):

		w = self.window
		w.run_command("save")
		n = w.active_view().file_name()
		cmexe(w, ["cl", "/c", "/Fa", n])
		w.open_file(n.replace(".c", ".asm"))

