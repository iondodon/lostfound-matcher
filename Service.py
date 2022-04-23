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
        ai_post = self.mongo.get_ai_post_data(post['post_uuid'])
        if ai_post is None:
            ai_post = {'post_uuid': post['post_uuid']}

        ai_post.update({'status': 'processing'})
        self.mongo.update_ai_post_data(ai_post)

        keywords = self.keywordExtractor.extract_keywords(post['details']).tolist()
        ai_post.update({'status': 'ready', 'keywords': keywords})

        self.mongo.update_ai_post_data(ai_post)