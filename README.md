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

A comment's subreddit, proportion of suggestive keywords, and mentions of general products can together give us a coherent presumption towards the user's tendency to purchase.


Generating a Credible Response
------------------------------
A personalized and enthusiastic suggestion is more persuasive than any combination of price, rating, or even relevance. But how can this be automated while still maintaining a level of compassion and recognition?

The first step is not to suggest to a user, but to reply to one. By responding to a user's comment directly, we will have already established a sense of shared reciprocity with the user before he or she even begins to read our suggestion.

The suggestion itself must sound like a suggestion that a user would hear from his or her peers. This bot achieves this by implementing randomized sentence templates customized to a user's past comment history. (While this method may not exactly pass the Turing test, genuine, human-like responses may soon be possible with natural language processing and neural networks.)

Finally, the recommended product must be highly relevant to what the user is looking for. The bot determines nouns in a user's comment which correlate to a specific Amazon product category, then returns a relevant, highly-rated product in such category with such keywords. The product's brand, price, decription, reviews, and specifications are then seamlessly woven into a natural language recommendation.

Technical Implementation
------------------------
Broadly, Reffit works in three steps.

1. For all recent comments from within a set of subreddits with high purchasing activity, calculate a reply confidence for each comment by parsing for relevant keywords.
2. If a comment exceeds the confidence threshold, search Amazon for a relevant product to the user's comment.
3. Using data from this product, generate a convincing, human-like recommendation for the product, then return to step 1 to scrape new comments.

###Header

>yrdy
>test
>## test
