
    ########...#     
   ##########...#    
  ############...#   
 ###...#    ###...#  
### esvkat15 ###...# 
 ###...#    ###...#  
  ############...#   
   ##########...#    
    ########...#     

# import libraries
import hashlib, os, re, sublime, sublime_plugin

# subl_print = sublime.message_dialog # print shortcut
# utility shortcuts
sha1 = hashlib.sha1
sub = re.sub
split = os.path.split
stat = os.stat

# execute visual studio shell script
def cmexe(window, command):

	window.run_command("exec", {"cmd": ["C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat", "x86", "&"] + command, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

# check file extention and get tool name
def chext(view):

	name = view.file_name()
	endswith = name.endswith
	return view and name and (endswith(".asm") or endswith(".c")) and ("%sl" % name[-1])

# check if main.exe process is running
def chpro(window):

	sha = sha1()
	sha.update(split(window.active_view().file_name())[0].encode())
	name = "C:\\Windows\\Temp\\subl\\" + sha.hexdigest() + ".txt"
	cmexe(window, ["md", split(name)[0], "2>", "nul", "&", "tasklist", "/FI", "IMAGENAME eq main.exe", "/FI", "SESSIONNAME eq Console", ">", name])
	while True:

		try:

			size = stat(name).st_size

		except:

			continue

		else:

			if size is 0:

				continue

			break


	with open(name) as file:

		string = file.read()
		
	cmexe(window, ["del", name])
	return string

# "Run Project" button macro
class ToExeCommand(sublime_plugin.WindowCommand):

	# active if currently editing asm or c file
	def is_enabled(self):

		return chext(self.window.active_view()) and True

	# save all files, compile current file, link project, and run program
	def run(self):

		window = self.window
		run_command = window.run_command
		run_command("save_all")
		name = split(window.active_view().file_name())[0]
		program = name + "\\main.exe"
		cmexe(window, ["taskkill", "/F", "/IM", "main.exe", "2>&1", ">", "nul"])
		run_command("to_obj")
		cmexe(window, ["link", "/OUT:" + program, name + "\\*.obj", "&", program])


# CTRL + S shortcut macro
class ToObjCommand(sublime_plugin.WindowCommand):

	# always active
	def is_enabled(self):

		return True

	# save and compile current file, restart program if already running
	def run(self):

		window = self.window
		view = window.active_view()
		name = view.file_name()
		run_command = window.run_command
		run_command("save")
		tool = chext(view)
		if tool:

			obj = sub("\.(c|asm)$", ".obj", name)
			try:

				initial = stat(obj).st_ctime

			except:

				initial = ""

			time = initial
			cmexe(window, [tool, "/c", name])
			while True:

				try:

					time = stat(obj).st_ctime

				except:

					continue

				else:

					if time is initial:

						continue

					break


			if "INFO: No tasks are running which match the specified criteria." not in chpro(window):

				run_command("to_exe")
				



# "Generate Assembly" button macro
class ToAsmCommand(sublime_plugin.WindowCommand):

	# active if editing c file
	def is_enabled(self):

		return "c" in chext(self.window.active_view())

	# compile file and open assembly step
	def run(self):

		window = self.window
		window.run_command("save")
		name = window.active_view().file_name()
		cmexe(window, ["cl", "/c", "/Fa", name])
		window.open_file(sub("\.c$", ".asm", name))

