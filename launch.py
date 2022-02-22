"""Préparation au lancement du jeu"""
#!/usr/bin/python3
import os, sys, platform

actual_os = platform.system().lower()

if "windows" in actual_os:
    COMMAND = ""

else:
    COMMAND = "3"

os.system(f"pip{COMMAND} list >> installed.tmp")

if not os.path.exists("installed.tmp"):
    print("Fichier contenant les packages installés introuvable.")
    sys.exit()

with open("installed.tmp", 'r', encoding='utf8') as inst:
    installed = inst.readlines()

installed = ' '.join(installed)

with open("requirements.txt", 'r', encoding='utf8') as req:
    for module in req.readlines():
        module = module.replace("\n", "").replace(" ", "")
        if module not in installed:
            print(f"Installation du module {module} nécessaire au fonctionnement du jeu...")
            os.system(f"python{COMMAND} -m pip install {module}")
            print("Installation terminée !")

os.remove("installed.tmp")
os.system(f"python{COMMAND} main.py")
