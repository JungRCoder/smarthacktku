PY_PATH = ./smarthack/manage.py

all:
	${PY} ${PY_PATH} runserver 127.0.0.1:8000
mi:
	${PY} ${PY_PATH} migrate
mmi:
	${PY} ${PY_PATH} makemigrations
