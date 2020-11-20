@echo off
rem %0\..\first-order-model\venv
cmd /k "cd first-order-model && set PATH=%PATH%;%0\..\venv\Scripts && set PATH=%PATH%;%0\..\venv && venv\Scripts\activate.bat && python -W ignore main_gui.py && deactivate && cd .."
exit