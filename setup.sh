sudo apt-get install libapache2-mod-wsgi
sudo apt-get install virtualenv
sudo apt-get install gcc

sudo apt-get install libmysqlclient-dev
sudo apt-get install nodejs

virtualenv venv
. venv/bin/activate
	pip install flask
	pip install sqlalchemy
	pip install urllib3
	pip install certifi
	pip install mysql-python
	pip install pyreact
deactivate

mkdir -p data
chown -R :www-data data
