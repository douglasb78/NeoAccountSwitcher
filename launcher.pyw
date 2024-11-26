import os
import subprocess
from subprocess import Popen
import sys
import webview
import atexit

def streamlit_run():
    if getattr(sys, 'frozen', False):
        filepath = sys._MEIPASS + "\\application\\main.py"
    else:
        filepath = os.getcwd() + "\\application\\main.py"
    streamlit = os.path.join(sys.prefix, "Scripts", "streamlit")
    os.chdir(os.path.dirname(__file__))
    msg = '\n\n', filepath, '\n', streamlit, '\n', os.getcwd()
    cmd = [
            streamlit,
            "run",
            filepath,
            "--server.port", str(8501),
            "--server.headless", "true",
            "--server.runOnSave", "true",
            "--global.developmentMode", "false",
            "--theme.base", "dark",
            "--theme.primaryColor", "#0077aa",
            "--theme.backgroundColor", "#eeeeee",
            "--theme.secondaryBackgroundColor", "#e0e0e0",
            "--theme.textColor", "#444444"
    ]
    print(cmd)
    CREATE_NO_WINDOW = 0x08000000
    process = subprocess.Popen(cmd, creationflags=CREATE_NO_WINDOW)
    atexit.register(cleanup, process)

def cleanup(process : Popen[bytes]):
    process.terminate()
    pass

if __name__ == "__main__":
    streamlit_run()
    webview.create_window("NeoAccount", "http://localhost:8501", min_size=(800, 800), resizable=False)
    webview.start()
