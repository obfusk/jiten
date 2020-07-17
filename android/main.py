import sys
if isinstance(getattr(sys.stdout, "buffer", None), str):
  print("Fixing stdout/stderr...")
  import androidembed
  class LogFile:
    def __init__(self):
      self.__buf = ""
    def write(self, s):
      s = self.__buf + s
      lines = s.split("\n")
      for l in lines[:-1]:
        androidembed.log(l)
      self.__buf = lines[-1]
    def flush(self):
      return
  sys.stdout = sys.stderr = LogFile()

from jiten.cli import cli
cli("-v serve -p 29483".split())
