import asyncio
from MongoDB import MongoDB
from LangTranslator import LangTranslator
from KeywordExtractor import KeywordExtractor
from PostsMatcher import PostsMatcher


class Service:
    mongo = MongoDB()
    keywordExtractor = KeywordExtractor()
    lang_translator = LangTranslator('en')
    posts_matcher = PostsMatcher()
    loop = asyncio.get_event_loop()


    def __init__(self):
        pass


    def delete_post_by_uuid(self, post_uuid):
        ai_post = self.mongo.get_ai_post_data(post_uuid)

        if ai_post is None:
            print("Post with uuid: " + post_uuid + " not found")
            return False
        if ai_post['status'] != 'processed':
            print("Can't delete post with status: " + ai_post['status'])
            return False

        self.delete_matching_pairs(post_uuid)
        self.mongo.delete_post_by_uuid(post_uuid)
        
        return True

    
    def delete_matching_pairs(self, post_uuid):
        self.mongo.delete_matching_pairs(post_uuid)


    def process_post(self, post):
        self.loop.run_until_complete(self.__async_process_post(post))


    async def __async_process_post(self, post):
        ai_post = self.mongo.get_ai_post_data(post['post_uuid'])
        if ai_post is None:
            ai_post = {'post_uuid': post['post_uuid']}

        ai_post.update({'status': 'processing'})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'searching_keywords', 'keywords': []})
        self.mongo.update_ai_post_data(ai_post)
        
        keywords = self.keywordExtractor.extract_keywords(post['details']).tolist()
        ai_post.update({'status': 'keywords_just_set', 'keywords': keywords})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'searching_matches', 'matches': []})
        self.mongo.update_ai_post_data(ai_post)
        
        self.posts_matcher.update_matches(ai_post)

        ai_post.update({'status': 'matches_just_set'})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'processed'})
        self.mongo.update_ai_post_data(ai_post)


    def __del__(self):
        self.loop.close()