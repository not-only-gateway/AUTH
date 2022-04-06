import json

from profile.models import AccessProfile
from app import app
from app import db
from endpoint.models import Endpoint
from flask import jsonify
from flask import request

from sqlalchemy.exc import SQLAlchemyError
from utils import Utils


from profile.models import AccessPrivilege
from privilege.models import Privilege

from api.api import ApiView

api = ApiView(class_instance=AccessProfile, identifier_attr='id', relationships=[])
access_api = ApiView(class_instance=AccessPrivilege, identifier_attr='',
                     relationships=[{'key': 'access', 'instance': AccessProfile},
                                    {'key': 'privilege', 'instance': Privilege}])


@app.route('/auth/access_profile/<e_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/auth/access_profile', methods=['POST'])
def access(e_id=None):
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


@app.route('/auth/list/access_profile', methods=['GET'])
def list_access():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401



@app.route('/auth/access_profile/privilege/<e_id>/<f_id>', methods=['POST'])
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


@app.route('/auth/access_profile/privilege/<e_id>/<f_id>', methods=['DELETE'])
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


@app.route('/auth/list/access_profile/privilege', methods=['GET'])
def list_access_privilege():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401

