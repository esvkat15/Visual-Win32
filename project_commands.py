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
    return filename is not None

  def run(self):
    self.window.run_command("save")
    self.window.run_command("build", {"select": True})
