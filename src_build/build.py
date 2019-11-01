import subprocess
from PyInstaller.__main__ import run as pack_exe

# pack the .exe file
pack_exe([
    "--onefile",

    "--windowed",

    "--workpath=../build/work",
    "--specpath=../build/work",
    "--distpath=../build/out",
    "--name=DBSpy",

    "../src/dbspy/__main__.py"
])

# run the packed .exe file
subprocess.Popen("../build/out/DBSpy.exe")
