import nltk
from itertools import islice
from tqdm.notebook import tqdm
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log
from Logger import logger

class KeywordExtractor:
    dict_idf = {}
    num_lines = None

    def __init__(self):
        self.num_lines = sum(1 for line in open("wiki_tfidf_terms.csv"))
        
        with open("wiki_tfidf_stems.csv") as file:
            with tqdm(total=self.num_lines) as pbar:
                for i, line in tqdm(islice(enumerate(file), 1, None)):
                    try: 
                        cells = line.split(",")
                        idf = float(sub("[^0-9.]", "", cells[3]))
                        self.dict_idf[cells[0]] = idf
                    except:
                        logger.error("Error on: " + line)
                    finally:
                        pbar.update(1)

    def extract_keywords(self, text, num_keywords=10):
        text_clean = self.__clean_text(text)
        text_clean = self.__exclude_words(text_clean)
        text_clean_stemmed = self.__stemm_text(text_clean)
        
        vectorizer = CountVectorizer()
        tf = vectorizer.fit_transform([text_clean_stemmed.lower()])
        tf = tf.toarray()
        tf = log(tf + 1)

        tfidf = tf.copy()
        words = array(vectorizer.get_feature_names_out())

        with tqdm(total=self.num_lines) as pbar:
            for k in tqdm(self.dict_idf.keys()):
                if k in words:
                    tfidf[:, words == k] = tfidf[:, words == k] * self.dict_idf[k]
                pbar.update(1)

        for j in range(tfidf.shape[0]):
            logger.info("Keywords of article", str(j+1), words[tfidf[j, :].argsort()[-num_keywords:][::-1]])

        return words[tfidf[0, :].argsort()[-num_keywords:][::-1]]
    
    def __exclude_words(self, text):
        words_to_exclude = ["lost", "found"]
        return " ".join([w for w in text.split() if w not in words_to_exclude])

    def __clean_text(self, text):
        text_clean = text.replace("\n", " ").replace("\'", "")
        text_clean = sub(r'[^\w\s]', '', text_clean)
        text_clean = sub(r'\s+', ' ', text_clean)
        text_clean = sub(r'\s+$', '', text_clean)
        text_clean = sub(r'\s+^', '', text_clean)
        return text_clean

    def __stemm_text(self, text):
        stemmer = nltk.stem.SnowballStemmer('english')
        text_clean_stemmed = " ".join([stemmer.stem(w) for w in text.split()])
        return text_clean_stemmed
