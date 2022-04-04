import nltk
import trafilatura
from itertools import islice
from tqdm.notebook import tqdm
from re import sub
from sklearn.feature_extraction.text import CountVectorizer
from numpy import array, log

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

html = trafilatura.fetch_url("https://en.wikipedia.org/wiki/Vienna")
text = trafilatura.extract(html)
text_clean = text.replace("\n", " ").replace("\'", "")
text_clean = sub(r'[^\w\s]', '', text_clean)
text_clean = sub(r'\s+', ' ', text_clean)
text_clean = sub(r'\s+$', '', text_clean)
text_clean = sub(r'\s+^', '', text_clean)
text_clean = text_clean[0:5000]



stemmer = nltk.stem.SnowballStemmer('english')
text_clean_stemmed = " ".join([stemmer.stem(w) for w in text_clean.split()])

# print("==========================================")
# print(text_clean)
# print("----------------------------------------")
# print(text_clean_stemmed)
# print("==========================================")

# words = text_clean.split()
# words_stemmed = text_clean_stemmed.split()

# # write words in two columns
# with open("words.csv", "w") as f:
#     for word in words:
#         clean_words = word
#         stemmed_word = words_stemmed[words.index(word)]
#         f.write(f"{clean_words},{stemmed_word}\n")


num_lines = sum(1 for line in open("wiki_tfidf_terms.csv"))


dict_idf = {}
with open("wiki_tfidf_stems.csv") as file:
    with tqdm(total=num_lines) as pbar:
        for i, line in tqdm(islice(enumerate(file), 1, None)):
            try: 
                cells = line.split(",")
                idf = float(sub("[^0-9.]", "", cells[3]))
                dict_idf[cells[0]] = idf
            except: 
                print("Error on: " + line)
            finally:
                pbar.update(1)


vectorizer = CountVectorizer()
tf = vectorizer.fit_transform([text_clean_stemmed.lower()])
tf = tf.toarray()
tf = log(tf + 1)

tfidf = tf.copy()
words = array(vectorizer.get_feature_names())

for k in tqdm(dict_idf.keys()):
    if k in words:
        tfidf[:, words == k] = tfidf[:, words == k] * dict_idf[k]
    pbar.update(1)

for j in range(tfidf.shape[0]):
    print("Keywords of article", str(j+1), words[tfidf[j, :].argsort()[-5:][::-1]])

