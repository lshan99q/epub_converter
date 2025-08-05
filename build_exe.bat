@echo off
python -m pip install pyinstaller
pyinstaller --onefile --windowed --icon=NONE setup.py
pause
