from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import env

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config[
    'SQLALCHEMY_DATABASE_URI'] = env.DATABASE + '://' + env.USER + ':' + env.PASSWORD + '@' + env.HOST_NAME + '/' + env.DATABASE_NAME
db = SQLAlchemy(app)
CORS(app)

from privilege.models import Privilege
from profile.models import AccessProfile
from endpoint.models import Endpoint, Access
from user.models import User
from active_directory.models import ActiveDirectory
from session.models import Session
from active_directory import views
from privilege import views
from session import views
from endpoint import views
from profile import views

db.create_all()

ad = ActiveDirectory.query.order_by(ActiveDirectory.id.asc()).all()
if len(ad) == 0:
    ActiveDirectory({
        'base': env.BASE,
        'attr': env.ATTRS,
        'server': env.SERVER,
        'filter': env.FILTER,
        'denomination': env.DENOMINATION,
        'description': env.DESCRIPTION
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1025)
