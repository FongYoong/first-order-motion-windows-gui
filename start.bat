@echo off
cmd /k "cd first-order-model && venv\Scripts\activate.bat && python -W ignore main_gui.py && deactivate && cd .."