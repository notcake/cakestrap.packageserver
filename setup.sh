sudo apt-get install libmysqlclient-dev

virtualenv venv
. venv/bin/activate
	pip install flask
	pip install sqlalchemy
	pip install urllib3
	pip install certifi
	pip install mysql-python
deactivate

