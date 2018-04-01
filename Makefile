PY = python3
PY_PATH = ./smarthack/manage.py

init:
	${PY} ${PY_PATH} makemigrations
	${PY} ${PY_PATH} migrate

run:
	${PY} ${PY_PATH} runserver 127.0.0.1:8000

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d | xargs rm -fr
