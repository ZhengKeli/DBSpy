import sys

from dbspy.gui import Application

args = sys.argv
print("args=", args)
if len(args) > 1:
    conf_file_path = args[1]
else:
    conf_file_path = None
Application(conf_file_path=conf_file_path)
