@echo off
pip list >> installed.tmp
python verif_requirements.py
del installed.tmp
python main.py
pause