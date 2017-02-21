from reviews.simple_sentence import extract_simple_sentences
# from spacy.en import English
from collections import namedtuple
from sklearn.cluster import DBSCAN
SimpleReview = namedtuple('SimpleReview', ['tokens', 'full_sentence', 'simplified_sentence', 'review'])


class Review(object):
    """
    Represents an Amazon review.
    """

    def __init__(self, text, summary, overall, helpful, review_time,
                 rid=None):
        """
        Creates a new Review with the given data. text is the text of the
        review, summary is the title, overall is the overall rating given
        (1-5 stars), helpful is a tuple (a, b) which means a out of b found
        this review helpful, and review_time is a datetime for the review.
        You can also pass an optional review ID.
        """

        self.id = rid
        self.text = text
        self.summary = summary
        self.overall = overall
        self.helpful = helpful
        self.review_time = review_time

        # self.doc = English(self.text)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    # def get_tokens(self):
    #     return list(map(str, list(self.doc) + list(English(self.summary))))

    def to_json(self):
        return {'text': self.text, 'summary': self.summary,
                'overall': self.overall, 'helpful': list(self.helpful),
                'review_time': self.review_time}


def reviews_to_simple_reviews(reviews):
    simp_revs = []
    for review in reviews:
        simple_sentences = extract_simple_sentences(review.text)
        for simple_sent in simple_sentences:
            simp_rev = SimpleReview(tokens=simple_sent.tokens,
                                    full_sentence=simple_sent.full_sentence,
                                    simplified_sentence=simple_sent.simplified_sentence,
                                    review=review)
            simp_revs.append(simp_rev)
    return simp_revs

# from sklearn.cluster import KMeans

def cluster_simple_reviews(simple_reviews, epsilon=0.5, min_samples=5):
    # This must take in a SimpleReview object as defined at the top of this file
    dbscanner = DBSCAN(metric='cosine', algorithm='brute', eps=epsilon, min_samples=min_samples)
    # dbscanner = KMeans(n_clusters=20, init='k-means++', max_iter=100, n_init=1)
    labels = dbscanner.fit_predict([sentence.simplified_sentence.vector for sentence in simple_reviews])
    clusters = {}
    for i in range(len(simple_reviews)):
        label = labels[i]
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(simple_reviews[i])
    return clusters
