#!/bin/bash
pip3 list >> installed.tmp
python3 verif_requirements.py
rm installed.tmp
python3 main.py
