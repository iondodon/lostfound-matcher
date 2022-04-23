from db.MongoDB import MongoDB


class PostsMatcher:
    mongo = MongoDB()


    def __init__(self):
        pass


    def update_matches(self, updated_ai_post):
        if updated_ai_post['keywords'] is None or len(updated_ai_post['keywords']) == 0:
            raise Exception('No keywords found to perform mathcing')
        
        all_ai_posts = self.mongo.get_all_ai_posts()
        for match_candidate in all_ai_posts:
            if match_candidate['post_uuid'] == updated_ai_post['post_uuid']:
                continue
            if match_candidate['status'] != 'processed':
                continue
            if match_candidate['keywords'] is None or len(match_candidate['keywords']) == 0:
                continue

            if len(set(match_candidate['keywords']).intersection(updated_ai_post['keywords'])) > 0:
                self.mongo.add_matching_pair(updated_ai_post['post_uuid'], match_candidate['post_uuid'])