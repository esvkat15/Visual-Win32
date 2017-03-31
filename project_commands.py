import sublime
import sublime_plugin

class CompileCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save")

class RunCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")
    self.window.run_command("build", {"args": {"select": True}})

class AsmOutCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save")
