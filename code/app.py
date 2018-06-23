from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, jwt_required, current_identity

from security import authenticate, identity as identity_function
from user import UserRegister
from item import Item, ItemList
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'Marty D'
app.config['JWT_AUTH_URL_RULE'] = '/login'
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

jwt = JWT(app, authenticate, identity_function)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user_id': identity.id
    })

@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code

api = Api(app)

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
