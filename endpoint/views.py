from app import app
from app import db
from endpoint.models import Endpoint, Access
from flask import jsonify
from flask import request
from manager.models import Manager
from utils import Utils

from api.api import ApiView

api = ApiView(
    class_instance=Endpoint,
    identifier_attr='url',
    relationships=[],
    db=db
)

@app.route('/auth/endpoint/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/auth/endpoint', methods=['POST'])
def endpoint(e_id=None):
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        if request.method == 'GET':
            return api.get(entity_id=e_id)
        elif request.method == 'POST':
            return api.post(package=request.json)
        elif request.method == 'PUT':
            return api.put(entity_id=e_id, package=request.json)
        elif request.method == 'DELETE':
            return api.delete(entity_id=e_id)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401

@app.route('/auth/list/endpoint', methods=['GET'])
def list_endpoint():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
