import threading
from db.MongoDB import MongoDB
from service.LangTranslator import LangTranslator
from core.ai.KeywordExtractor import KeywordExtractor
from core.PostsMatcher import PostsMatcher
from Logger import logger


class Service:
    mongo = MongoDB()
    keywordExtractor = KeywordExtractor()
    lang_translator = LangTranslator('en')
    posts_matcher = PostsMatcher()
    threadLock = threading.Lock()


    def __init__(self):
        pass


    def delete_post_by_uuid(self, post_uuid):
        ai_post = self.mongo.get_ai_post_data(post_uuid)

        if ai_post is None:
            logger.info('Post with uuid: ' + post_uuid + ' not found')
            return False
        if ai_post['status'] != 'ready':
            logger.info('Can\'t delete post with status: ' + ai_post['status'])
            return False

        self.delete_matching_pairs(post_uuid)
        self.mongo.delete_post_by_uuid(post_uuid)
        
        return True


    def process_post(self, post):
        threading.Thread(target=self.__process_post_task, args=(post,)).start()


    def __process_post_task(self, post):
        self.threadLock.acquire()

        ai_post = self.mongo.get_ai_post_data(post['post_uuid'])
        if ai_post is None:
            ai_post = {'post_uuid': post['post_uuid']}

        self.validate_updated_post_data(post)

        ai_post.update(post)
        ai_post.update({'status': 'updating_data'})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'searching_keywords', 'keywords': []})
        self.mongo.update_ai_post_data(ai_post)
        
        en_details = self.lang_translator.translate(post['details'])
        keywords = self.keywordExtractor.extract_keywords(en_details).tolist()
        ai_post.update({'status': 'keywords_just_set', 'keywords': keywords})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'searching_matches'})
        self.mongo.update_ai_post_data(ai_post)
        
        self.delete_matching_pairs(ai_post['post_uuid'])
        self.posts_matcher.update_matches(ai_post)

        ai_post.update({'status': 'matches_just_set'})
        self.mongo.update_ai_post_data(ai_post)

        ai_post.update({'status': 'ready'})
        self.mongo.update_ai_post_data(ai_post)
    
        self.threadLock.release()


    def validate_updated_post_data(self, post):
        if post['type'] is None:
            logger.info('Post type is not specified')
            raise Exception('Post type is not specified')


    def delete_matching_pairs(self, post_uuid):
        self.mongo.delete_matching_pairs(post_uuid)

    
    def get_matches(self, post_uuid):
        ai_post = self.mongo.get_ai_post_data(post_uuid)
        
        if ai_post is None:
            logger.info("Post with uuid: " + post_uuid + " not found")
            return {
                'status': 'not_found', 
                'matches': [], 'message': 
                'Post with uuid: ' + post_uuid + ' not found'
            }

        if ai_post['status'] != 'ready':
            logger.info("Can't get matches for post with status: " + ai_post['status'])
            return {
                'status': ai_post['status'], 
                'matches': [], 
                'message': 'Can\'t get matches for post with status: ' + ai_post['status']
            }

        return self.posts_matcher.get_matches(post_uuid)