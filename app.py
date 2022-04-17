from flask import Flask, request
import numpy
from MongoDB import MongoDB
from TranslatorFacade import TranslatorFacade
from KeywordExtractor import KeywordExtractor
import json


matcher_app = Flask(__name__)


keywordExtractor = KeywordExtractor()
# translator = TranslatorFacade('en')
mongo = MongoDB()


print("Starting server...")

@matcher_app.route('/api/v1/posts/<postId>/matches', methods=['GET'])
def matches(postId):
    args = request.args
    _maxMatches = args.get('maxMatches')

    # convert keywords to json string 
    return json.dumps()


@matcher_app.route('/api/v1/posts/process', methods=['POST'])
def process_post():
    post = request.get_json()
    keywords = keywordExtractor.extract_keywords(post['details']).tolist()
    mongo.update_ai_post_data({'post_uuid': post['post_uuid'], 'keywords': keywords})
    return post


@matcher_app.route('/api/v1/posts/<postUuid>', methods=['DELETE'])
def delete_posts(postUuid):
    mongo.delete_post_by_uuid(postUuid)
    return '', 204