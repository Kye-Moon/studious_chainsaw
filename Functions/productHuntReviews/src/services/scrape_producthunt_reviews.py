from urllib.parse import urlencode
import json

import requests
from ..clients.dynamodb import DynamoDB
from ..models.ProductHuntMention import ProductHuntMention

API = '55ee7a6b8c6644bb0c01cd93ed246548'
product = "webwave"


def process_producthunt_review_integration(campaign_id, product_slug, db: DynamoDB):
    """
    Entry point to the scraper.
    get the query based on the cursor and then call self.parse on result
    """
    cursor = None
    hasNextPage = True

    while hasNextPage:
        response = fetch_producthunt_reviews(cursor, product_slug)
        if response.status_code == 200:
            reviews = response.json()
            partition_key = f"{reviews['data']['product']['slug']}#PH_REVIEW"
            listOfEdges = reviews["data"]["product"]["reviews"]["edges"]
            listOfReviews = list(
                map(lambda edge: create_producthunt_mention(partition_key=partition_key, campaign_id=campaign_id,
                                                            edge=edge), listOfEdges))
            filteredReviews = filter_existing_reviews(listOfReviews, db, pk=partition_key)

            for mention in filteredReviews:
                try:
                    db.put_item(pk=mention.PK, sk=mention.SK, item=mention.dict(exclude={"PK", "SK"}))
                except RuntimeError:
                    raise Exception(f"Comment not able to be saved.")
                finally:
                    print(f"mention and user with external ids {mention.PK}:{mention.SK} were created")

            hasNextPage = reviews["data"]["product"]["reviews"]["pageInfo"]["hasNextPage"]
            cursor = reviews["data"]["product"]["reviews"]["pageInfo"]["endCursor"]
        else:
            raise Exception(f"Query failed to run with a {response.status_code}.")
    print("done")

def filter_existing_reviews(post_mentions, mentionsTable, pk):
    existing_reviews = mentionsTable.get_items(pk=pk)
    existing_mentions_id_list = list(map(lambda mention: mention["SK"], existing_reviews["Items"]))
    filteredMentions = list(filter(lambda mention: mention.SK not in existing_mentions_id_list, post_mentions))
    print(f"filtered mentions: {filteredMentions}")
    return filteredMentions


def fetch_producthunt_reviews(cursor, product_slug):
    """
    Entry point to the scraper.
    get the query based on the cursor and then call self.parse on result
    """
    url = f'https://www.producthunt.com/frontend/graphql'
    response = requests.post(get_url(url=url), data=json.dumps(get_query(cursor, product_slug)),
                             headers={'content-type': 'application/json'})
    return response


def create_producthunt_mention(partition_key, campaign_id, edge):
    review = ProductHuntMention(
        PK=partition_key,
        SK=f"{edge['node']['id']}#{campaign_id}",
        body=edge["node"]["body"],
        source="producthunt",
        username=edge["node"]["user"]['name'],
        userDescription=None,
        profileImageUrl=edge["node"]["user"]["avatarUrl"],
        createAt="2020-01-01T00:00:00.000Z",
    )
    return review


def get_url(url):
    """
     Prepend the scraperapi proxy url to the front of the product hunt URL
     This helps with the bot not getting blocked by PH.
             Parameters:
                     url (str): the product hunt url to scrape.
             Returns:
                     proxy_url (str): the product hunt url prefixed with the scraperapi url
     """
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def get_query(cursor, product_slug):
    """
    Query for the graphql endpoint.
    """
    json_data = {
        "query": query,
        "variables": {
            "slug": product_slug,
            "query": None,
            "reviewsLimit": 100,
            "reviewsOrder": "HELPFUL",
            "includeReviewId": None,
            "rating": "0",
            "reviewsCursor": cursor
        },
        "operationName": "ProductReviewsPage"
    }
    return json_data


# The Graphql Query for the product hunt product reviews page.
# Some of this may be filtered later
query = """
      query ProductReviewsPage(
      $slug: String!
      $reviewsLimit: Int!
      $reviewsCursor: String
      $reviewsOrder: ReviewsOrder
      $includeReviewId: ID
      $query: String
      $rating: String
      $tags: [String!]
    ) {
      product(slug: $slug) {
        id
        slug
        name
        reviewsRating
        reviewsCount
        isMaker
        isTrashed
        ...ProductReviewsPageReviewsFeedFragment
      }
    }
    fragment ProductReviewsPageReviewsFeedFragment on Product {
      id
      reviewsCount
      ...ReviewListFragment
      __typename
    }
    fragment ReviewListFragment on Reviewable {
      id
      reviews(
        first: $reviewsLimit
        after: $reviewsCursor
        order: $reviewsOrder
        includeReviewId: $includeReviewId
        query: $query
        rating: $rating
        tags: $tags
      ) {
        edges {
          node {
            id
            sentiment
            comment {
              id
              bodyHtml
              __typename
            }
            ...RatingReviewFragment
            __typename
          }
          __typename
        }
        totalCount
        pageInfo {
          hasNextPage
          endCursor
          __typename
        }
        __typename
      }
      __typename
    }
    fragment RatingReviewFragment on Review {
      id
      rating
      body
      sentiment
      user {
        id
        username
        name
        url
        work {
          id
          jobTitle
          companyName
          product {
            id
            name
            __typename
          }
          __typename
        }
        ...UserImage
        __typename
      }
      comment {
        id
        body
        __typename
      }
      post {
        id
        name
        slug
        __typename
      }
      __typename
    }
    fragment UserImage on User {
      id
      name
      username
      avatarUrl
      __typename
    }
"""
