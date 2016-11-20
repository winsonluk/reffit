<a href="docs/images/logo.gif">
    <img src="docs/images/logo_tiny.gif" align="right" height="70" />
</a>

reffit: Referrals on Reddit [![Build Status](https://travis-ci.org/winsonluk/reffit.svg?branch=master)](https://travis-ci.org/winsonluk/reffit)
===========================

Reffit is a natural language recommendation bot that applies predictive analysis on the social networking website Reddit to determine users who are actively inquiring for product suggestions, then builds a persuasive recommendation of a relevant and highly-rated Amazon product by intelligently synthesizing the product's price, description, and reviews.


Detecting User Inquiry
----------------------
The clearest indication of a user's readiness to purchase can be found in the subreddit (an organized categorical area of interest within Reddit) that a user's comment is written in. Examples of subreddits with high purchasing activity include [BuyItForLife](https://reddit.com/r/BuyItForLife), where users ask for suggestions of products that last a lifetime, [Frugal](https://reddit.com/r/Frugal), where users recommend low-cost alternatives to everyday purchases, and [MaleFashionAdvice](https://reddit.com/r/MaleFashionAdvice) (and its female counterpart [FemaleFashionAdvice](https://reddit.com/r/FemaleFashionAdvice)), where users are inspired to purchase the fashionable clothing of tomorrow.

Also indicative of a user's purchasing tendency is the text of his or her comment in relation to the comments within the subreddit. Comments with a comparatively high proportion of words such as "buying", "price", or "advice" correlate highly with a user's likeliness to consider a product recommendation.

Furthermore, users who mention the plural form of multiword product category keywords, such as "arm warmers", "laptop sleeves", or "hand sanitizers", are likely to be seeking a suggestions for a particular item within such category.

A comment's subreddit, proportion of suggestive keywords, and mentions of general products can together give us a coherent interpretation of the user's tendency to purchase.
