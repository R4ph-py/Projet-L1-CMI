import os, sys

if not os.path.exists("installed.tmp"):
    print("Fichier contenant les packages installés introuvable.")
    sys.exit()

with open("requirements.txt", 'r', encoding='utf8') as req:
    with open("installed.tmp", 'r', encoding='utf8') as inst:
        for module in req.readlines():
            if module not in inst.readlines():
                print(f"Installation du module {module} nécessaire au fonctionnement du jeu...")
                os.system(f"python3 -m pip install {module}")
                print("Installation terminée !")

sys.exit()
