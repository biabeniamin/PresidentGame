#generated automatically
from flask import Flask, make_response
from flask_restful import Api
from SqlAlchemyMain import createDatabase, session
from SqlAlchemy import convertToJson
from flask_cors import CORS
from CardEndpoints import CardEndpoints
from PlayerEndpoints import PlayerEndpoints
from NotificationEndpoints import NotificationEndpoints

app = Flask(__name__)
CORS(app)
api = Api(app)
createDatabase()

api.add_resource(CardEndpoints, '/Cards', resource_class_kwargs ={ 'session' : session}) 
api.add_resource(PlayerEndpoints, '/Players', resource_class_kwargs ={ 'session' : session}) 
api.add_resource(NotificationEndpoints, '/Notifications', resource_class_kwargs ={ 'session' : session}) 

@api.representation('application/json')
def output_json(data, code, headers=None):
	print(data)
	resp = make_response(convertToJson(data), code)
	resp.headers.extend(headers or {})
	return resp


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)
