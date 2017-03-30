import sublime
import sublime_plugin

class TestCommand(sublime_plugin.WindowCommand):

  def is_enabled(self):
    return True

  def run(self):
    self.window.run_command("save_all")
