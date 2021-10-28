Laba4

install flask

install waitress

requires python_version = "3.6.0"

virtualenv

URL = /api/v1/hello-world-12


###########################################
 
 Datebase:
 
 install alecmbic
 install sqlalchemy
 
 alembic init alembic
 
 >alemic.ini
 
  sqlalchemy.url = mysql://{User}:{Password}@127.0.0.1/{Name_bd}
  
 >env.py 

  import os
  import sys
  sys.path.append(os.getcwd())
  import main
  target_metadata = main.Base.metadata


