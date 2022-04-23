from pymongo import MongoClient


class MongoDB:
    client = None
    db = None
    ai_posts_data = None


    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db = self.client['lostfound-matcher-db']
        self.ai_posts_data = self.db['ai_posts_data']
        self.matching_pairs = self.db['matching_pairs']
        

    def update_ai_post_data(self, ai_post):
        self.ai_posts_data.update_one(
            {'post_uuid': ai_post['post_uuid']},
            {'$set': ai_post},
            upsert=True
        )


    def get_ai_post_data(self, post_uuid):
        return self.ai_posts_data.find_one({'post_uuid': post_uuid})


    def delete_post_by_uuid(self, post_uuid):
        self.ai_posts_data.delete_one({'post_uuid': post_uuid})


    def get_all_ai_posts(self):
        return self.ai_posts_data.find()


    def add_matching_pair(self, post_uuid_0, post_uuid_1):
        self.matching_pairs.insert_one({
            'post_uuid_0': post_uuid_0,
            'post_uuid_1': post_uuid_1
        })

    
    def delete_matching_pairs(self, post_uuid):
        self.matching_pairs.delete_many({'post_uuid_0': post_uuid})
        self.matching_pairs.delete_many({'post_uuid_1': post_uuid})