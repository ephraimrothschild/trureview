import logging

from flask import Flask, request
from flask import render_template

app = Flask(__name__)
app.debug = True

logging.info('loading models...')

from reviews.scrape import scrape_yelp_reviews_from_url
from reviews.structure import reviews_to_simple_reviews
from reviews.structure import cluster_simple_reviews
from collections import namedtuple


@app.route('/')
def index():
    return render_template('index.html')

ReviewClust = namedtuple('ReviewClust', ['simple_sentence_str', 'num_stars', 'cluster_size'])

@app.route('/review-it')
def review_it():
    product_url = request.args.get('url')
    if product_url is not None:
        logging.info('scraping reviews from %s', product_url)
        reviews = scrape_yelp_reviews_from_url(product_url)
        logging.info('scraped %d reviews', len(reviews))
        simple_reviews = reviews_to_simple_reviews(reviews)
        logging.info('extracted %d phrases', len(simple_reviews))

        eps = float(request.args.get('eps', '0.1'))
        minpts = int(request.args.get('minpts', '2'))
        clusters = cluster_simple_reviews(simple_reviews, eps, minpts)

        review_clusters = []
        overall = int(sum([simple_rev.review.overall for simple_rev in simple_reviews])/len(simple_reviews))
        for cluster in clusters.values():
            # Get average numbers of stars for cluster
            num_stars = int(sum([simple_rev.review.overall for simple_rev in cluster])/len(cluster))
            current_clust = {'simple_sentence_str': cluster[0].simplified_sentence.text,
                             'full_sentence_str': cluster[0].full_sentence.text,
                             'num_stars': num_stars,
                             'cluster_size': len(cluster),
                             'cluster': cluster,
                             'num_to_display': min(len(cluster), 20)}
            review_clusters.append(current_clust)

    return render_template('review.html', item_name="The unstoppable passage of time #entropyalwaysincreases",
                           overall=overall, clusters=review_clusters)

if __name__ == '__main__':
    app.run()
