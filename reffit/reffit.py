###############################################################################
#
# reffit: Search Reddit for product keywords and suggest items from Amazon
# Copyright (C) 2016 Winson Luk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import ConfigParser
import math
import random
import re
import sqlite3
import sys
import time
import urllib2

import pandas # Must import before OAuth2Util to avoid numpy.ufunc warnings
import numpy
import OAuth2Util
import praw

from amazon.api import AmazonAPI
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def main():
    #Configure variables from config.ini
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    NUM_RETRIEVE = int(config.get('setup', 'NUM_RETRIEVE'))
    MIN_CONFIDENCE = int(config.get('setup', 'MIN_CONFIDENCE'))
    SENTENCES_IN_REPLY = int(config.get('setup', 'SENTENCES_IN_REPLY'))
    SLEEP_TIME = int(config.get('setup', 'SLEEP_TIME'))
    USER_AGENT = config.get('praw', 'USER_AGENT')
    AMAZON_KEY = config.get('amazon', 'AMAZON_KEY')
    AMAZON_SECRET = config.get('amazon', 'AMAZON_SECRET')
    AMAZON_ASSOCIATE = config.get('amazon', 'AMAZON_ASSOCIATE')

    #Initialize variables
    global keywords, c
    alreadyReplied = []  #Tracks users who have already been replied to
    keywords = pandas.read_csv('data.csv')
    conn = sqlite3.connect('templates.db')
    c = conn.cursor()
    subreddits = '+'.join([line for line in keywords['subreddits'].dropna()])

    #Connect to Reddit and Amazon
    r = praw.Reddit(USER_AGENT)
    o = OAuth2Util.OAuth2Util(r)
    amazon = AmazonAPI(AMAZON_KEY, AMAZON_SECRET, AMAZON_ASSOCIATE)

    while True:
        o.refresh()
        submissions = r.get_subreddit(subreddits)
        posts = submissions.get_new(limit=NUM_RETRIEVE)
        for i in posts:
            try:
                if str(i.author) in alreadyReplied:
                    raise ValueError('SKIPPING: ALREADY REPLIED TO AUTHOR')
                if 'reddit.com' not in i.url:
                    raise ValueError('SKIPPING: LINK SUBMISSION')

                #If Amazon link is found in submission (self) text
                selfStr = i.selftext.encode('ascii', 'ignore').lower()
                if  ('/dp/' in selfStr) or ('/gp/' in selfStr):
                    productData = find_in_amazon(
                        amazon, AMAZON_ASSOCIATE,
                        amazon.similarity_lookup(ItemId=get_asin(selfStr))[0]
                        )
                    if type(productData) is dict:
                        print 'FOUND', productData['link'], 'IN SELF:', i.id
                        alreadyReplied.append(str(i.author))
                        print ''
                        print generate_comment(
                            SENTENCES_IN_REPLY, productData['link'],
                            productData['brand'],
                            str(productData['category']).lower(),
                            productData['price'], productData['features'],
                            productData['reviews']
                            )
                        #comment.reply(
                        #    generate_comment(
                        #        SENTENCES_IN_REPLY, productData['link'],
                        #        productData['brand'],
                        #        str(productData['category']).lower(),
                        #        productData['price'],
                        #        productData['features'],
                        #        productData['reviews']
                        #        )
                        #    )
                        print ''
                        raise ValueError('SKIPPING: DONE REPLYING')
                    elif type(productData) is str:
                        print productData  #Error message

                #If Amazon link is found in comment
                for comment in i.comments:
                    commentStr = str(comment).encode('ascii', 'ignore').lower()
                    if (
                            (str(comment.author) not in alreadyReplied) and
                            (('/dp/' in commentStr) or ('/gp/' in commentStr))
                        ):
                        productData = find_in_amazon(
                            amazon, AMAZON_ASSOCIATE,
                            amazon.similarity_lookup(
                                ItemId=str(get_asin(commentStr))
                                )[0]
                            )
                        if type(productData) is dict:
                            print (
                                'FOUND', productData['link'],
                                'IN COMMENT', comment.id
                                )
                            alreadyReplied.append(str(i.author))
                            alreadyReplied.append(str(comment.author))
                            print ''
                            print generate_comment_with_reply(
                                SENTENCES_IN_REPLY, productData['link'],
                                productData['brand'],
                                str(productData['category']).lower(),
                                productData['price'], productData['features'],
                                productData['reviews']
                                )
                            #comment.reply(
                            #    generate_comment_with_reply(
                            #        SENTENCES_IN_REPLY, productData['link'],
                            #        productData['brand'],
                            #        str(productData['category']).lower(),
                            #        productData['price'],
                            #        productData['features'],
                            #        productData['reviews']
                            #        )
                            #    )
                            print ''
                            raise ValueError('SKIPPING: DONE REPLYING')
                        elif type(productData) is str:
                            print productData  #Error message

                #If item keyword is found in title
                for word in keywords['items'].dropna():
                    if (
                            word.lower()
                            in i.title.encode('ascii', 'ignore').lower()
                        ):
                        if calculate_confidence(i) >= MIN_CONFIDENCE:
                            productData = find_in_amazon(
                                amazon, AMAZON_ASSOCIATE,
                                amazon.search_n(
                                    1, Keywords=word, SearchIndex='All'
                                    )[0]
                                )
                            if type(productData) is dict:
                                print 'FOUND', word, 'IN TITLE', i.id
                                alreadyReplied.append(str(i.author))
                                productData['category'] = word
                                print ''
                                print generate_comment(
                                    SENTENCES_IN_REPLY, productData['link'],
                                    productData['brand'],
                                    str(productData['category']).lower(),
                                    productData['price'],
                                    productData['features'],
                                    productData['reviews']
                                    )
                                #comment.reply(
                                #    generate_comment(
                                #        SENTENCES_IN_REPLY,
                                #        productData['link'],
                                #        productData['brand'],
                                #        str(productData['category']).lower(),
                                #        productData['price'],
                                #        productData['features'],
                                #        productData['reviews']
                                #        )
                                #    )
                                print ''
                                raise ValueError('SKIPPING: DONE REPLYING')
                            elif type(productData) is str:
                                print productData  #Error message

                raise ValueError('SKIPPING: NOTHING FOUND')
            except KeyboardInterrupt:
                raise
            except ValueError as err:
                print err
            except:
                print 'ERROR: PROBLEM IN MAIN'
                print sys.exc_info()[0]
        print 'SLEEPING FOR', SLEEP_TIME, 'SECONDS...'
        time.sleep(SLEEP_TIME)

def find_in_amazon(amazon, associate, product):
    '''Return formatted product data as a dictionary'''
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', str(UserAgent().random))]

    #Initialize product info
    try:
        brand = product.brand
        category = product.browse_nodes[len(product.browse_nodes)-1].name
        features = product.features
        price = max(product.price_and_currency[0], product.list_price[0])
        price = '$'+ str(int(math.ceil(price/10.0) * 10.0))
        reviews = []
        link = ''
    except:
        return 'ERROR: PRODUCT NOT FOUND'
        print sys.exc_info()[0]

    #Add editorial and customer reviews
    try:
        reviews.extend(
            re.split(
                '(?<=[.!?]) +',
                (BeautifulSoup(product.editorial_review, 'lxml')
                .get_text().encode('ascii', 'ignore'))
                )
            )  #Scrape and add editorial reviews
        review = (BeautifulSoup(opener.open(product.reviews[1]).read(), 'lxml')
            .findAll('div', {'class':'reviewText'}))  #Scrape customer reviews
        for i in range(len(review)):
            reviews.extend(
                re.split(
                    '(?<=[.!?]) +',
                    review[i].get_text().encode('ascii', 'ignore')
                    )
                )  #Add customer reviews
    except:
        print 'ERROR: PROBLEM FETCHING REVIEWS'
        print sys.exc_info()[0]

    productData = {}

    #Create Amazon link
    if ',' in product.title:
        link = (
            '[' + product.title[:product.title.index(',')]
            + '](https://smile.amazon.com/dp/' + product.asin + '/?tag='
            + associate + ')'
            )
    else:
        link = (
            '[' + product.title + '](https://smile.amazon.com/dp/'
            + product.asin + '/?tag=' + associate + ')'
            )

    #Clean up scraped text
    features = [
        'This has ' + x.encode('ascii', 'ignore').lower() + '. '
        for x in features
        ]
    reviews = [x.encode('ascii', 'ignore')for x in reviews]
    for word in keywords['blacklist'].dropna():
        features = [x for x in features if not word.lower() in x.lower()]
        reviews = [x for x in reviews if not word.lower() in x.lower()]

    productData['brand'] = brand
    productData['category'] = category
    productData['features'] = features
    productData['price'] = price
    productData['reviews'] = reviews
    productData['link'] = link
    return productData

def get_asin(comment):
    '''Return Amazon ASIN'''
    if '/dp/' in comment:
        start_index = comment.find('/dp/') + 4
    elif '/gp/product/' in comment:
        start_index = comment.find('/gp/') + 12
    elif '/gp/' in comment:
        start_index = comment.find('/gp/') + 9
    else:
        raise ValueError('ERROR: ASIN NOT FOUND')

    if start_index+10 > len(comment):
        raise ValueError('ERROR: ASIN OUT OF RANGE')
    else:
        asin = comment[start_index:start_index+10]
    return asin

def calculate_confidence(submission):
    '''Calculate confidence in whether to suggest a product'''
    confidence = 0
    for word in keywords['suggestives'].dropna():
        if (
                word.lower()
                in submission.title.encode('ascii', 'ignore').lower()
            ):
            confidence += 3
        if (
                word.lower()
                in submission.selftext.encode('ascii', 'ignore').lower()
            ):
            confidence += 2
    return confidence

def random_string(tableName, columnName):
    '''Return a random template string from a specified column'''
    numColumns = c.execute('SELECT COUNT(*) FROM {tn}'.\
                format(tn=tableName)).fetchone()[0]
    c.execute('SELECT {cn} FROM {tn} WHERE id={sentenceId}'.\
            format(
                cn=columnName, tn=tableName,
                sentenceId=random.randint(1, numColumns)
                )
            )
    return str(c.fetchone()[0])

def generate_comment_with_reply(
    length, link, brand, category, price, features, reviews
    ):
    '''Return a reply plus a randomly generated reddit comment'''
    return (
        random_string('amazonCommentReply', 'badProduct')
        + generate_comment(length, link, brand, category,
            price, features, reviews
            )
        )

def generate_comment(
    length, link, brand, category, price, features, reviews
    ):
    '''Return a randomly generated reddit comment'''
    link = (
        random_string('topLevelReply', 'link')
        .format(link + ' (Amazon charity product)')
        )
    generatedSentences = [
        random_string('topLevelReply', 'brand').format(brand),
        random_string('topLevelReply', 'category').format(category),
        random_string('topLevelReply', 'price').format(price)
        ]
    try:
        feature = str(random.choice(features))
        review = str(random.choice(reviews))
    except:
        feature = ''
        review = ''
        print 'ERROR: NO FEATURE OR REVIEW'
        print sys.exc_info()[0]
    apology = '(sorry for the typos, english is my second language).'
    disclaimer = (
        '\n\n *** \n\n ^^^Bleep, ^^^bloop! ^^^This ^^^comment ^^^was '
        '^^^automatically ^^^generated ^^^by ^^^a ^^^bot ^^^as ^^^part ^^^of '
        '^^^a ^^^research ^^^study ^^^involving ^^^customized ^^^product '
        '^^^suggestions ^^^using ^^^artificial ^^^intelligence. ^^^Amazon '
        '^^^Smile ^^^proceeds ^^^will ^^^benefit ^^^a ^^^charity ^^^of '
        '^^^your ^^^choice, ^^^and ^^^additional ^^^referral ^^^proceeds '
        '^^^will ^^^help ^^^finance ^^^this ^^^study. ^^^For ^^^questions '
        '^^^or ^^^concerns, ^^^please ^^^contact ^^^/u/reffit_owner.'
        )
    return (
        link
        + ' ' + feature
        + ' ' + ' '.join(random.sample(generatedSentences[:], length - 3))
        + ' ' + review
        + ' ' + apology
        + disclaimer
        )

if __name__ == '__main__':
    main()
