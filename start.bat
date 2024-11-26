@echo off
call "%~dp0\.venv\Scripts\activate.bat"
set PATH="%~dp0\.venv\Scripts\"
.venv\Scripts\python.exe launcher.pyw