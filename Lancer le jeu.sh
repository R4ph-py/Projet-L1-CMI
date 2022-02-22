#!/bin/bash
pip3 list >> installed.tmp
python3 launch.py
rm installed.tmp
python3 main.py
