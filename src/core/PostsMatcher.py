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
            if match_candidate['status'] != 'ready':
                continue
            if match_candidate['keywords'] is None or len(match_candidate['keywords']) == 0:
                continue
            if match_candidate['type'] == updated_ai_post['type']:
                continue

            numnber_intersected_keywords = len(set(match_candidate['keywords']).intersection(updated_ai_post['keywords']))
            if numnber_intersected_keywords > 0:
                matching_pair = {
                    'post_uuid_1': updated_ai_post['post_uuid'], 
                    'post_uuid_2': match_candidate['post_uuid'],
                    'number_intersected_keywords': numnber_intersected_keywords
                }
                self.mongo.add_matching_pair(matching_pair)

    
    def get_matches(self, post_uuid):
        ai_post = self.mongo.get_ai_post_data(post_uuid)

        matching_pairs = self.mongo.get_matching_pairs(post_uuid)
        matches = []
        for pair in matching_pairs:
            if pair['post_uuid_1'] == pair['post_uuid_2']:
                raise Exception('Matching pair contains same post uuid')

            return_pair = {'number_intersected_keywords': pair['number_intersected_keywords']}
            if pair['post_uuid_1'] == post_uuid:
                matched_post_uuid = pair['post_uuid_2']
            else:
                matched_post_uuid = pair['post_uuid_1']

            return_pair = return_pair | {'matched_post_uuid': matched_post_uuid}
            if not any(d['matched_post_uuid'] == matched_post_uuid for d in matches):
                matches.append(return_pair)
        
        return {'status': ai_post['status'], 'matches': matches}

