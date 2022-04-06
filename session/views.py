import uuid
from datetime import datetime, timedelta

from app import app, db
from flask import jsonify
from flask import request
from session.models import Session
from user.models import User
from sqlalchemy.exc import SQLAlchemyError
from utils import Utils
from active_directory.models import ActiveDirectory


@app.route('/auth/authentication', methods=['GET'])
def authenticate():
    allowed = Utils.authenticate(request.headers.get('authorization', None), method=request.args.get('method', None),
                                 path=request.args.get('path', None))
    if allowed:
        return jsonify({'status': 'success', 'description': 'accepted', 'code': 202}), 202
    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401


@app.route('/auth/authentication', methods=['POST'])
def sign_in():
    data = request.json
    base_ad = ActiveDirectory.query.order_by(ActiveDirectory.id.asc()).all()
    base_ad = base_ad[0].id if len(base_ad) > 0 else None
    if Utils.validate_authentication(
            active_directory=data.get('active_directory', base_ad),
            email=data.get('email', None).strip(),
            password=data.get('password', None)
    ):
        token_uuid = uuid.uuid4()
        max_life = datetime.now() + timedelta(days=7)
        current_session = Session.query.filter(
            Session.user == data.get('email', None).strip(),
            Session.max_life > datetime.now()).first()
        if current_session is None:
            current_session = Session({
                'user': data.get('email', None).strip(),
                'token_uuid': token_uuid,
                'ip_address': request.remote_addr,

                'creation_time': datetime.now(),
                'max_life': max_life,
                'ad': data.get('active_directory', base_ad)
            })
        else:
            current_session.max_life = max_life
            db.session.commit()

        milliseconds = max_life.timestamp() * 1000
        new_token = Utils.make_jwt({
            'user_email': data.get('email', None).strip(),
            'session_id': current_session.id,
            'exp': milliseconds,
            'uuid': str(token_uuid)
        })
        user = User.query.get(data.get('email', None).strip())
        user = user.__dict__ if user is not None else {}
        if user.get('_sa_instance_state', None) is not None:
            del user['_sa_instance_state']

        return jsonify({
            'token': str(new_token),
            'exp': milliseconds,
            'user': user
        }), 202


    else:
        return jsonify({'status': 'error', 'description': 'unauthorized', 'code': 401}), 401
