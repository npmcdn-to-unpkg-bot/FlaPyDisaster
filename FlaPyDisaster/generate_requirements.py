import os


os.system("conda list --explicit > conda_requirements.txt")
os.system("pip freeze > requirements.txt")
