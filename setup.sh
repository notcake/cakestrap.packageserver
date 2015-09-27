virtualenv venv
. venv/bin/activate
	pip install flask
	pip install sqlalchemy
deactivate

git clone https://github.com/rohe/pyoidc.git
mv pyoidc/src/oic oic
rm -rf pyoidc
