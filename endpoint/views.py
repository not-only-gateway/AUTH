from app import app
from app import db
from endpoint.models import Endpoint, Access
from flask import jsonify
from flask import request

from privilege.models import Privilege
from utils import Utils

from api.api import ApiView

api = ApiView(
    class_instance=Endpoint,
    identifier_attr='url',
    relationships=[],
    db=db
)
apiEP = ApiView(
    class_instance=Endpoint,
    identifier_attr='',
    relationships=[{'key': 'endpoint', 'instance': Endpoint},
                   {'key': 'privilege', 'instance': Privilege}], db=db)

@app.route('/api/endpoint', methods=['POST', 'GET', 'PUT', 'DELETE'])
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


@app.route('/api/list/endpoint', methods=['GET'])
def list_endpoint():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return api.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/api/endpoint_privilege/<f_id>', methods=['POST'])
def endpoint_privilege(f_id=None):
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        Access({
            'endpoint': request.args.get('identifier', None),
            'privilege': f_id
        })
        return jsonify({'status': 'success', 'description': 'created', 'code': 201}), 201
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/api/endpoint_privilege/<f_id>', methods=['DELETE'])
def delete_endpoint_privilege(f_id=None):
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        access = Access.query.filter(
            Access.access == request.args.get('identifier', None),
            Access.privilege == f_id
        ).first()
        if access is not None:
            db.session.delete(access)
            db.session.commit()
        return jsonify({'status': 'success', 'description': 'created', 'code': 201}), 201
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/api/list/endpoint_privilege', methods=['GET'])
def list_endpoint_privilege():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.method, path=request.path)
    if allowed:
        return apiEP.list(data=request.args)
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
