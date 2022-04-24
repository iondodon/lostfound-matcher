from pymongo import MongoClient


class MongoDB:
    client = None
    db = None
    ai_posts_data = None


    def __init__(self):
        self.client = MongoClient("mongodb", 27017)
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


    def add_matching_pair(self, matching_pair):
        self.matching_pairs.insert_one(matching_pair)

    
    def delete_matching_pairs(self, post_uuid):
        self.matching_pairs.delete_many({
            '$or': [
                {'post_uuid_1': post_uuid},
                {'post_uuid_2': post_uuid}
            ]
        })

    
    def get_matching_pairs(self, post_uuid):
        return self.matching_pairs.find({
            '$or': [
                {'post_uuid_1': post_uuid},
                {'post_uuid_2': post_uuid}
            ]
        })