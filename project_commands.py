
		    ########...#     
		   ##########...#    
		  ############...#   
		 ###...#    ###...#  
		###.esvkat15 ###...# 
		 ###...#    ###...#  
		  ############...#   
		   ##########...#    
		    ########...#     

# import libraries
import hashlib, os, re, sublime, sublime_plugin

# debug printing shortcut
subl_print = sublime.message_dialog

# utility shortcuts
sha1 = hashlib.sha1
sub = re.sub
split = os.path.split
stat = os.stat

# execute visual studio shell script
def cmexe(window, command):

	# runs visual c variables-all batch script along with commands
	window.run_command("exec", {"cmd": ["C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat", "x86", "&"] + command, "file_regex": "^(..[^:]*):([0-9]+):?([0-9]+)?:? (.*)$", "shell": True})

# check file extention and get tool name
def chext(view):

	# sets local shortcut variables then returns the proper visual c tool name, if any
	name = view.file_name()
	endswith = name.endswith
	return view and name and (endswith(".asm") or endswith(".c")) and ("%sl" % name[-1])

# check if main.exe process is running
def chpro(window):

	# hashes the current directory path for a temporary filename, prompts cmd to print a tasklist into the file, then stalls until it completes
	sha = sha1()
	sha.update(split(window.active_view().file_name())[0].encode())
	temp = "C:\\Windows\\Temp\\subl\\" + sha.hexdigest() + ".txt"
	cmexe(window, ["md", split(temp)[0], "2>", "nul", "&", "tasklist", "/FI", "IMAGENAME eq main.exe", "/FI", "SESSIONNAME eq Console", ">", temp])
	while True:

		# expects error depending on whether temporary file exists
		try:

			# gets size in bytes of temporary file
			size = stat(temp).st_size

		# temporary file doesnt exist yet
		except:

			# keeps waiting for temporary file to exist
			continue

		# temporary file exists
		else:

			# checks if temporary file is empty
			if size is 0:

				# waits for file to fill
				continue

			# file is full, stops waiting
			break


	# fetches temporary file
	with open(temp) as file:

		# copies file contents
		string = file.read()

	# prompts cmd to delete temporary file, then stalls until it completes
	cmexe(window, ["del", temp])
	while True:

		# expects error depending on whether temporary file exists
		try:

			# pokes file for error
			stat(temp)

		# temporary file doesnt exist
		except:

			# temporary file is deleted, stops waiting
			break

		# temporary file exists
		else:

			# keeps waiting for temporary file to be deleted
			continue


	# returns task information
	return string

# "Run Project" button macro
class ToExeCommand(sublime_plugin.WindowCommand):

	# active if currently editing asm or c file
	def is_enabled(self):

		# returns whether file extension is valid or not
		return chext(self.window.active_view()) and True

	# save all files, compile current file, link project, and run program
	def run(self):

		# sets local shortcut variables, saves project files, prompts cmd to kill any running process, then stalls until it completes
		window = self.window
		run_command = window.run_command
		run_command("save_all")
		directory = split(window.active_view().file_name())[0]
		program = directory + "\\main.exe"
		cmexe(window, ["taskkill", "/F", "/IM", "main.exe", "2>&1", ">", "nul"])
		while "INFO: No tasks are running which match the specified criteria." not in chpro(window):

			# keeps waiting for process to die
			continue

		# saves and compiles current file, then links and runs project
		run_command("to_obj")
		cmexe(window, ["link", "/OUT:" + program, directory + "\\*.obj", "&", program])


# CTRL + S shortcut macro
class ToObjCommand(sublime_plugin.WindowCommand):

	# always active
	def is_enabled(self):

		# enables command
		return True

	# save and compile current file, restart program if already running
	def run(self):

		# sets local shortcut variables, saves file, then checks if file can be compiled
		window = self.window
		view = window.active_view()
		name = view.file_name()
		run_command = window.run_command
		run_command("save")
		tool = chext(view)
		if tool:

			# gets object file name, then expects error depending on whether it exists
			obj = sub("\.(c|asm)$", ".obj", name)
			try:

				# gets creation time of object file
				initial = stat(obj).st_ctime

			# object file doesnt exist
			except:

				# defaults creation time
				initial = ""

			# sets initial time, prompts cmd to compile current file, then stalls until it completes
			time = initial
			cmexe(window, [tool, "/c", name])
			while True:

				# expects error depending on whether object file exists
				try:

					# gets creation time of object file
					time = stat(obj).st_ctime

				# object file doesnt exist
				except:

					# keeps waiting for object file to exist
					continue

				# object file exists
				else:

					# checks if creation time is unchanged
					if time is initial:

						# waits for creation time to change
						continue

					# creation time changed, stops waiting
					break


			# checks if process is running
			if "INFO: No tasks are running which match the specified criteria." not in chpro(window):

				# restarts project
				run_command("to_exe")
				



# "Generate Assembly" button macro
class ToAsmCommand(sublime_plugin.WindowCommand):

	# active if editing c file
	def is_enabled(self):

		# returns whether file ends in .c
		return "c" in chext(self.window.active_view()) # self.window.active_view().file_name().endswith(".c")

	# compile file and open assembly step
	def run(self):

		# sets local shortcut variables, saves file, compiles object and assembly, then opens .asm file
		window = self.window
		name = window.active_view().file_name()
		window.run_command("save")
		cmexe(window, ["cl", "/c", "/Fa", name])
		window.open_file(sub("\.c$", ".asm", name))

