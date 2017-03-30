import sublime
import sublime_plugin

class CompileCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")

class RunCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")

class AsmOutCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")
