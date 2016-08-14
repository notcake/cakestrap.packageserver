sudo apt-get install python-dev
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install virtualenv
sudo apt-get install gcc

sudo apt-get install libmysqlclient-dev
sudo apt-get install nodejs

# Update git (GIT_TERMINAL_PROMPT=0 won't work pre version 2.3)
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update
sudo apt-get install git

virtualenv venv
. venv/bin/activate
	pip install flask
	pip install sqlalchemy
	pip install urllib3
	pip install requests
	pip install certifi
	pip install mysql-python
	pip install pyreact
deactivate

mkdir -p data
chown -R :www-data data
