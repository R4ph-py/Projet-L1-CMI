@echo off
pip list >> installed.tmp
python verif_requirement.py
del installed.tmp
python main.py
