from app import app
from app import db
from endpoint.models import Endpoint, Access
from flask import jsonify
from flask import request

from utils import Utils

from api.api import ApiView

api = ApiView(
    class_instance=Endpoint,
    identifier_attr='url',
    relationships=[],
    db=db
)
@app.route('/auth/endpoint', methods=['POST', 'GET', 'PUT', 'DELETE'])
def endpoint():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        if request.method == 'GET':
            return api.get(entity_id=request.args.get('identifier', None))
        elif request.method == 'POST':
            return api.post(package=request.json)
        elif request.method == 'PUT':
            return api.put(entity_id=request.json.get('identifier', None), package=request.json)
        elif request.method == 'DELETE':
            return api.delete(entity_id=request.json.get('identifier', None))
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401

@app.route('/auth/list/endpoint', methods=['GET'])
def list_endpoint():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
