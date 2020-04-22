#generated automatically
import flask
import flask_restless
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session, validates
from sqlalchemy import *
from SqlAlchemy import Base, engine
from ValidationError import ValidationError
from Cards import Cards
from Players import Players
from Notifications import Notifications

def add_cors_headers(response):
	response.headers['Access-Control-Allow-Origin'] = '*'
	response.headers['Access-Control-Allow-Credentials'] = 'true'
	response.headers['Access-Control-Allow-Headers'] = '*'
	response.headers['Access-Control-Allow-Methods'] = '*'
	return response

app = flask.Flask(__name__)
app.after_request(add_cors_headers)
Session = sessionmaker(bind = engine, autocommit = False, autoflush = False)
s = scoped_session(Session)
manager = flask_restless.APIManager(app, session = s)
manager.create_api(Cards,
	methods =['GET', 'PUT', 'POST', 'DELETE'], validation_exceptions=[ValidationError], results_per_page=-1)
manager.create_api(Players,
	methods =['GET', 'PUT', 'POST', 'DELETE'], validation_exceptions=[ValidationError], results_per_page=-1)
manager.create_api(Notifications,
	methods =['GET', 'PUT', 'POST', 'DELETE'], validation_exceptions=[ValidationError], results_per_page=-1)

Base.metadata.bind = engine
Base.metadata.create_all()
app.run(debug=True, host='0.0.0.0', port=5000)
