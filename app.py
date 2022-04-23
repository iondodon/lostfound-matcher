from flask import Flask, request
from Service import Service
import json


matcher_app = Flask(__name__)
service = Service()


print("Listening...")


@matcher_app.route('/api/v1/posts/<postUuid>/matches', methods=['GET'])
def matches(postUuid):
    # convert keywords to json string 
    return json.dumps()


@matcher_app.route('/api/v1/posts/process', methods=['POST'])
def process_post():
    post = request.get_json()
    service.process_post(post)
    return post


@matcher_app.route('/api/v1/posts/<postUuid>', methods=['DELETE'])
def delete_posts(postUuid):
    if service.delete_post_by_uuid(postUuid):
        return "Deleted post with uuid: " + postUuid
    return "Post with uuid: " + postUuid + " cannot be deleted"