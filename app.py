from flask import Flask, request
from service.Service import Service
import json


matcher_app = Flask(__name__)
service = Service()


print("Listening on port 5000...")


@matcher_app.route('/api/v1/posts/<post_uuid>/matches', methods=['GET'])
def matches(post_uuid):
    matches = service.get_matches(post_uuid)
    return json.dumps(matches)


@matcher_app.route('/api/v1/posts/process', methods=['POST'])
def process_post():
    post = request.get_json()
    service.process_post(post)
    return json.dumps({'status': 'ok'})


@matcher_app.route('/api/v1/posts/<postUuid>', methods=['DELETE'])
def delete_posts(postUuid):
    if service.delete_post_by_uuid(postUuid):
        return "Deleted post with uuid: " + postUuid
    return "Post with uuid: " + postUuid + " cannot be deleted"