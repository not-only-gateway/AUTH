import json

from privilege.models import Privilege
from user.models import User, AccessPrivilege
from app import app
from app import db
from endpoint.models import Endpoint
from flask import jsonify
from flask import request

from sqlalchemy.exc import SQLAlchemyError
from utils import Utils
from api.api import ApiView

api = ApiView(class_instance=User, identifier_attr='user_email', relationships=[], db=db)
access_api = ApiView(class_instance=AccessPrivilege, identifier_attr='',
                     relationships=[{'key': 'user', 'instance': User},
                                    {'key': 'privilege', 'instance': Privilege}], db=db)



@app.route('/api/user/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/user', methods=['POST'])
def user(e_id=None):
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


@app.route('/api/list/user', methods=['GET'])
def list_user():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401




@app.route('/api/access_privilege/<e_id>/<f_id>', methods=['POST'])
def create_access_privilege(e_id=None, f_id=None):
    data = request.json
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        AccessPrivilege({
            'access': e_id,
            'privilege': f_id
        })
        return jsonify({'status': 'success', 'description': 'created', 'code': 201}), 201
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/api/access_privilege/<e_id>/<f_id>', methods=['DELETE'])
def delete_access_privilege(e_id=None, f_id=None):

    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        access = AccessPrivilege.query.filter(AccessPrivilege.access == e_id,
                                              AccessPrivilege.privilege == f_id).first()
        if access is not None:
            db.session.delete(access)
            db.session.commit()
        return jsonify({'status': 'success', 'description': 'created', 'code': 201}), 201
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/api/list/access_privilege', methods=['GET'])
def list_access_privilege():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401

