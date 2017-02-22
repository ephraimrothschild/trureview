import logging

from flask import Flask, request
from flask import render_template

app = Flask(__name__)
app.debug = True

logging.info('loading models...')

from reviews.scrape import scrape_yelp_reviews_from_url, scrape_yelp_title_from_url
from reviews.structure import reviews_to_simple_reviews
from reviews.structure import cluster_simple_reviews
from collections import namedtuple
import random
import time



@app.route('/')
def index():
    return render_template('index.html')

ReviewClust = namedtuple('ReviewClust', ['simple_sentence_str', 'num_stars', 'cluster_size'])

@app.route('/review-it')
def review_it():
    product_url = request.args.get('url')
    if product_url is not None:
        print('Scraping reviews from', product_url)
        start_time = time.time()
        reviews = scrape_yelp_reviews_from_url(product_url)
        title = scrape_yelp_title_from_url(product_url)
        end_time = time.time()

        print('Scraping finished. Scraped',len(reviews), 'reviews in', end_time-start_time, 'seconds')
        logging.info('scraped %d reviews', len(reviews))
        print('Extracting Simple Senteces...')
        start_time = time.time()
        simple_reviews = reviews_to_simple_reviews(reviews)
        end_time = time.time()
        print("Simple Sentence extraction finished. Extracted", len(simple_reviews), 'Simple Sentences in', end_time-start_time, 'seconds')
        logging.info('extracted %d phrases', len(simple_reviews))

        eps = float(request.args.get('eps', '0.1'))
        minpts = int(request.args.get('minpts', '3'))
        print('Beginning Clustering...')
        start_time = time.time()
        clusters = cluster_simple_reviews(simple_reviews, eps, minpts)
        end_time = time.time()
        print('Clustering finished. Found', len(clusters), 'clusters in', end_time-start_time, 'seconds')

        review_clusters = []
        overall = sum([simple_rev.review.overall for simple_rev in simple_reviews])/float(len(simple_reviews))
        # Get the cluster keys except the one that represents noise
        keys = clusters.keys() - set([-1])
        # Find the largest cluster that isn't noise (since it appears that the largest non-noise cluster is actually
        # also noise)
        largest_cluster = sorted([(key, len(clusters[key])) for key in keys], key=len, reverse=True)[0][0]
        # Remove from list of clusters
        # keys = keys - set([largest_cluster])
        keys = [key for key in keys if len(clusters[key]) < 100]
        for key in keys:
            cluster = clusters[key]
            # Get average numbers of stars for cluster
            num_stars = int(sum([simple_rev.review.overall for simple_rev in cluster])/len(cluster))
            current_clust = {'simple_sentence_str': cluster[0].simplified_sentence.text.capitalize(),
                             'full_sentence_str': cluster[0].full_sentence.text,
                             'num_stars': num_stars,
                             'cluster_size': len(cluster),
                             'cluster': cluster,
                             'num_to_display': min(len(cluster), 20),
                             'cluster_index': key}
            review_clusters.append(current_clust)
        quotes = [clust['simple_sentence_str'] for clust in random.sample(review_clusters, min(7, len(review_clusters)))]

        # Sort by number of times this type of sentence was said
        review_clusters.sort(key=lambda x:x['cluster_size'], reverse=True)
    return render_template('review.html', item_name=title,
                           overall=int(overall), overall_float=float("{0:.2f}".format(overall)), clusters=review_clusters, url=product_url,
                           quotes=quotes, item_abreviation=''.join([w[0] for w in title.split(' ')]))

if __name__ == '__main__':
    app.run()
