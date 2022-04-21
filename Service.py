from MongoDB import MongoDB
from LangTranslator import LangTranslator
from KeywordExtractor import KeywordExtractor


class Service:
    mongo = MongoDB()
    keywordExtractor = KeywordExtractor()
    lang_translator = LangTranslator('en')

    def __init__(self):
        pass


    def delete_post_by_uuid(self, postUuid):
        self.mongo.delete_post_by_uuid(postUuid)

    def process_post(self, post):
        keywords = self.keywordExtractor.extract_keywords(post['details']).tolist()
        self.mongo.update_ai_post_data({'post_uuid': post['post_uuid'], 'keywords': keywords})