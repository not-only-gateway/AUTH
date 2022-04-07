import json
from app import app
from app import db
from active_directory.models import ActiveDirectory
from flask import jsonify
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from utils import Utils

from api.api import ApiView
api = ApiView(class_instance=ActiveDirectory, identifier_attr='id', relationships=[], db=db)

@app.route('/api/active_directory/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/active_directory', methods=['POST'])
def ad(e_id=None):
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


@app.route('/api/list/active_directory', methods=['GET'])
def list_ad():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
