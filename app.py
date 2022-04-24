from flask import Flask, request
from service.Service import Service
import json
from Logger import logger
from flask import Response


matcher_app = Flask(__name__)
service = Service()


logger.info("Listening on port 5000...")


@matcher_app.route('/api/v1/posts/<post_uuid>/matches', methods=['GET'])
def matches(post_uuid):
    matches = service.get_matches(post_uuid)
    return Response(json.dumps(matches), mimetype='application/json')


@matcher_app.route('/api/v1/posts/process', methods=['POST'])
def process_post():
    post = request.get_json()
    service.process_post(post)
    return Response(json.dumps({'status': 'ok'}), mimetype='application/json')


@matcher_app.route('/api/v1/posts/<postUuid>', methods=['DELETE'])
def delete_posts(postUuid):
    if service.delete_post_by_uuid(postUuid):
        return Response(json.dumps({'message': "Deleted post with uuid: " + postUuid}), mimetype='application/json')
    return Response(json.dumps({'message': "Post with uuid: " + postUuid + " cannot be deleted"}), mimetype='application/json')


if __name__ == "__main__":
    from waitress import serve
    serve(matcher_app, host="0.0.0.0", port=5000)
