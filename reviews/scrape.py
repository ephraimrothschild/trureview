from bs4 import BeautifulSoup
from datetime import datetime
import re
import logging
import grequests



from reviews.structure import Review

def scrape_yelp_title_from_url(url):
    product_page = grequests.map([grequests.get(url)])[0]
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    title = product_soup.find(class_='biz-page-title').text.strip()
    return title

def scrape_yelp_reviews_from_url(url):
    """
    Given the URL of an Amazon product page, scrapes the reviews of that
    product and returns them as a list.
    """

    reviews = []
    product_page = grequests.map([grequests.get(url)])[0]
    # print(product_page.content)
    # print('Scraping data from ' + url)
    product_soup = BeautifulSoup(product_page.content, 'html.parser')
    num_pages = int(re.search('of ([0-9]+)', product_soup.find(class_="page-of-pages").text.strip()).group(1))

    # Set up asyncronous requests
    urls = [url + "?start=" + str(i*20) for i in range(num_pages)]
    # print(urls)
    rs = [grequests.get(u) for u in urls]
    responses = grequests.map(rs)
    for current_page in responses:
        review_soup = BeautifulSoup(current_page.content, 'html.parser')
        review_wrappers = review_soup.find_all(class_='review-wrapper')
        shouldcontinue = True
        for wrapper in review_wrappers:
            if shouldcontinue:
                shouldcontinue = False
                continue
            stars = float(re.search('([0-9.]+) star', wrapper.select('.i-stars')[0].attrs['title']).group(1))
            body = wrapper.find_all(class_='review-content')[0].select('p')[0].text
            helpful = wrapper.find_all(class_='useful')[0].find(class_='count').text.strip()
            helpful_num = int(helpful) if len(helpful) else 0
            date_text = wrapper.find(class_='review-content').find(class_='rating-qualifier').contents[0].strip()
            try:
                review_date = datetime.strptime(date_text, '%m/%d/%Y')
            except Exception:
                pass
            summary = ""
            reviews.append(Review(body, summary, stars, (helpful_num, helpful_num),
                                  review_date, len(reviews)))
    return reviews