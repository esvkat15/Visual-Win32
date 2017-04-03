import sublime
import sublime_plugin

class RunCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")

class CompileCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save")

class AsmOutCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    filename = None
    if self.window.active_view():
      filename = self.window.active_view().file_name()
    if filename is None or not filename.endswith(".c"):
      filename = None
    return True#filename is not None

  def run(self):

  	cmd = ["C:\\Windows\\System32\\sublime\\cl.exe"]
  	cmd += ["/?"]
    self.window.run_command("save")
    self.window.run_command("exec", {"cmd": cmd, "file_regex": "(?i)^(?:ERROR: |WARNING: )[^C-Z]*([C-Z]:[^:]*):([0-9]+):([0-9]*)(.*)$"})
