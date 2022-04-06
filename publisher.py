# TODO
# from datetime import datetime
# import pika, json
# from pika import exceptions
# from publish.models import Publish
#
# from backend_utils.utils.publisher import publish
#
#
# def publisher(request, status_code, response_time, response, service_id):
#     publish(
#         method='request',
#         body={
#             'params': request.args if request.method == 'get' else request.json,
#             'method': request.method,
#             'request_time': str(datetime.now()),
#             'full_url': request.full_path,
#             'url': request.path,
#             'service_id': service_id,
#             'headers': dict(request.headers),
#             'status_code': status_code,
#             'response_time': response_time,
#             'response': response
#         },
#         routing='request'
#     )
#
#
# def publisher_user(email):
#     all = Publish.query.all()
#
#     for i in all:
#         publish(
#             method=i.method,
#             body={
#                 'user_email': email
#             },
#             routing=i.routing
#         )