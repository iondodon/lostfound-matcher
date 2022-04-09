from flask import Flask, request
from Models import Base, Post
from SqlEngine import SqlEngine
from TranslatorFacade import TranslatorFacade
from KeywordExtractor import KeywordExtractor
import json


matcher_app = Flask(__name__)


sqlEngien = SqlEngine()
keywordExtractor = KeywordExtractor()
translator = TranslatorFacade('en')


print("=================Ready!!!=================")


@matcher_app.route('/api/v1/posts/<postId>/matches', methods=['GET'])
def home(postId):
    args = request.args
    _maxMatches = args.get('maxMatches')

    post = sqlEngien.getPost_by_id(postId)
    translated_post_details = translator.translate(post.details)
    keywords = keywordExtractor.extract_keywords(translated_post_details)

    # convert keywords to json string 
    return json.dumps(keywords.tolist() )
