import requests

from .clients.dynamodb import DynamoDB
from .models.ProductHuntPostResponse import ProductHuntPostResponse
from .models.ProductHuntMention import ProductHuntMention

access_token = "GT6Vx3FsGNcjI8BifASZiRltohnnWFoEeUoRtVtAImM"
ph_url = "https://api.producthunt.com/v2/api/graphql"
headers = {"Authorization": f"Bearer {access_token}"}
PRODUCT_HUNT = "PRODUCT_HUNT"


def process_ph_post_integration_record(url: str, campaign_id: str, db: DynamoDB):
    slug = url.split("/")[-1]
    partition = f"{slug}#PH_COMMENT"

    request = fetch_from_product_hunt(slug=slug)

    if request.status_code == 200:
        product_hunt_post = ProductHuntPostResponse.parse_obj(request.json())
        listOfEdges = product_hunt_post.data.post.comments.edges
        post_mentions = list(map(lambda edge: create_producthunt_mention(edge.node, pk=partition, campaign_id=campaign_id), listOfEdges))
        filteredMentions = filter_existing_mentions(post_mentions, db, pk=partition)

        for mention in filteredMentions:
            try:
                db.put_item(pk=mention.PK, sk=mention.SK, item=mention.dict(exclude={"PK", "SK"}))
            except RuntimeError:
                raise Exception(f"Comment not able to be saved.")
            finally:
                print(f"mention and user with external ids {mention.PK}:{mention.SK} were created")
    else:
        raise Exception(f"Query failed to run with a {request.status_code}.")


def create_producthunt_mention(node, pk, campaign_id):
    mention = ProductHuntMention(
        PK=f"{pk}",
        SK=f"{node.id}#{campaign_id}",
        createAt=node.createdAt,
        body=node.body,
        source=PRODUCT_HUNT,
        username=node.user.username,
        profileImageUrl=node.user.profileImage if node.user.profileImage else "",
    )
    return mention


def filter_existing_mentions(post_mentions, mentionsTable, pk):
    existing_mentions = mentionsTable.get_items(pk=pk)
    print(existing_mentions)
    existing_mentions_id_list = list(map(lambda mention: mention["SK"], existing_mentions["Items"]))
    filteredMentions = list(filter(lambda mention: mention.SK not in existing_mentions_id_list, post_mentions))
    print(f"filtered mentions: {filteredMentions}")
    return filteredMentions


def fetch_from_product_hunt(slug: str):
    query = build_query(slug=slug)
    request = requests.post(ph_url, json=query, headers=headers)
    return request


def build_query(slug: str):
    get_post_comments_query = """
          query MyQuery($slug: String!) {
              post(slug: $slug) {
                  id
                  description
                  commentsCount
                  comments {
                    edges {
                      node {
                        id
                        body
                        createdAt
                        user {
                          id
                          username
                          profileImage
                        }
                      }
                    }
                  }
               }
          }"""
    variables = {"slug": slug}
    payload = {
        "query": get_post_comments_query,
        "variables": variables
    }
    return payload


class ProductHuntCrud:
    pass
