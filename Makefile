PY = python3
PY_PATH = ./smarthack/manage.py

all:
	${PY} ${PY_PATH} makemigrations
	${PY} ${PY_PATH} migrate
	${PY} ${PY_PATH} runserver 127.0.0.1:8000
