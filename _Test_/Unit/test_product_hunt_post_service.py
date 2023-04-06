from src.clients.dynamodb import DynamoDB

from src.service_modules import product_hunt_post_service

access_token = "GT6Vx3FsGNcjI8BifASZiRltohnnWFoEeUoRtVtAImM"
ph_url = "https://api.producthunt.com/v2/api/graphql"
headers = {"Authorization": f"Bearer {access_token}"}
import json

with open('producthunt_post_response.json') as f:
    test_data = json.load(f)


# product_hunt_service.fetch_from_product_hunt = MagicMock(name='fetch_from_product_hunt_mock')

class TestProductHuntPostService:

    def test_fetch_from_product_hunt_returns_200(self):  ## TESTING REAL PH API
        response = product_hunt_post_service.fetch_from_product_hunt(slug="webwave")
        assert response.status_code == 200

    def test_get_post_comments(self, requests_mock):
        # given
        db = DynamoDB(table_name="mentions", instance="test")
        db.get_table()
        ph_graphql_api = "https://api.producthunt.com/v2/api/graphql"
        url = "https://www.producthunt.com/posts/webwave"
        requests_mock.post(ph_graphql_api, text=json.dumps(test_data))

        # when
        response = product_hunt_post_service.process_ph_post_integration_record(url=url, campaign_id="1", db=db)

        # clean up
        db.delete_table()


var = {
    "status_code": 200,
    "data": {
        "post": {
            "id": "374968",
            "description": "WebWave is the only true drag and drop website builder that works like a graphic design tool. You can position elements anywhere on the canvas, work with Layers, and create websites featuring a shop, email, SEO, domain, hosting, and more.",
            "commentsCount": 624,
            "comments": {
                "edges": [
                    {
                        "node": {
                            "id": "2198970",
                            "body": "@mac_czaj and I just wanted to thank you, guys. It is a truly unique community. We are 3rd Product of the Day and still have chances to win Product of a Week! It was an incredible journey! Your feedback is crucial for our future!",
                            "createdAt": "2023-02-10T16:21:15Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "url"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2186313",
                            "body": "I have been waiting for this launch for two months! Please share your thoughts about our graphical design approach to building websites!",
                            "createdAt": "2023-02-06T08:22:44Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2186246",
                            "body": "Hello Product Hunt! \n\nI’m Mac. Before I founded WebWave I was a software developer, and I created websites for clients as a side hustle. I was ace with code, but lacked the imagination and creativity necessary to design great websites. It helped me to realize, engineers only slow the process. Marketers and graphic designers should be in charge of web design. Creative people have all the skills and knowledge, but miss proper web design software. So I started creating a tool for designers so that they can create websites in an environment that is friendly and familiar to them.\n\nSince then, WebWave has grown to over 500,000 users in the EU, and now we want to show WebWave to the rest of the World. \n\nWhat makes WebWave unique?\nOur superpower is that WebWave looks and feels much like a graphic design tool, Figma, Canva, or Photoshop, rather than other website builders. There’s no invisible table in the background where you have to fit your elements. Instead, you’ve got the freedom and flexibility to position, resize, and style elements however you want. You can work with Layers, and elements can overlay or overlap. We call this “true drag-and-drop” and it is tailor-made for creative people.\n\nJoin us\nJoin us on our mission to bring back the design from engineers to designers. Start your adventure for free, or use a 50% discount for a 12-month premium plan. We are thrilled to partner with Product Hunt and are committed to giving back to this fantastic community.\n\nThanks for supporting us, and we love to see your feedback in the comments! \n\nPS. Big thanks to @chrismessina for hunting us and for your amazing advice!",
                            "createdAt": "2023-02-06T08:04:55Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2214267",
                            "body": "❤️❤️❤️",
                            "createdAt": "2023-02-17T17:17:08Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2213846",
                            "body": "I love how dynamic the page is and how fast the website is 😍🙌 and everything is intuitive!!",
                            "createdAt": "2023-02-17T15:03:49Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2213629",
                            "body": "Congratulation on the recent launch of WebWave on the Product Hunt! This is an excellent website builder for anyone looking for a simple and efficient way to create a professional-looking website, without needing to invest time in learning how to code.",
                            "createdAt": "2023-02-17T12:52:57Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2211985",
                            "body": "Best app that I found for creating landing page. I wanted SEO support and I got it. The site has robots.txt, sitema.xml, headers control and more. Only tricky thing is that paid plans hasn't some features of free plan.",
                            "createdAt": "2023-02-16T18:51:20Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2211514",
                            "body": "I really like WebWave. I use it from years to my webside. I love it!",
                            "createdAt": "2023-02-16T15:21:55Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2209768",
                            "body": "Really enjoying webwave. I am planning on running a blog site on my business sites and doing simple order processing. Maybe I can move completely away from the other builder we use at our agency.",
                            "createdAt": "2023-02-16T00:03:14Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2208295",
                            "body": "Congratulations on your launch!",
                            "createdAt": "2023-02-15T12:34:27Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2203008",
                            "body": "Love the simplicity. \nThanks for creating an awesome product for dummies like me. \n\nWhat I love the most is customization abilities. \nMailbox included and it’s a very big bonus for me. \nNo need to deal with mail marketing system.",
                            "createdAt": "2023-02-13T09:56:16Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2202638",
                            "body": "Awesome guys, upvotes have increased significantly, great job!\nHighly recommend this platform: you have everything in place and what is missing, just suggest, they will implement as soon as possible!",
                            "createdAt": "2023-02-13T08:29:24Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2202485",
                            "body": "I've been building sites for over 20 years. I used dozens of builders, each have their merits, but none compare to the fun I have with WebWave. WebWave has just the right amount of flexibility and features and originality that make me think they will stay ahead of the pack. Exciting pleasurable experience.",
                            "createdAt": "2023-02-13T07:43:24Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2202142",
                            "body": "Hi, Webvawe is a great tool, no question about it. But does it offer a possibility to whitelist sites you make for clients?",
                            "createdAt": "2023-02-13T00:48:29Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201995",
                            "body": "Great Website Builder",
                            "createdAt": "2023-02-12T19:39:21Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201983",
                            "body": "This definitely deserves a spot at the top. I am super impressed with the free style designer. It is like building sites in Photoshop! It gives you the freedom to place everything exactly as you want it, even in sites for mobile browsers.",
                            "createdAt": "2023-02-12T19:17:53Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201964",
                            "body": "WebWave is very easy to use website builder. WebWave is very well organised and liaded with very much inbuild features. The included hosting also is very good and fest. I like to say that this is All in one website builder that you ever need.",
                            "createdAt": "2023-02-12T18:37:49Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201828",
                            "body": "Do you guys allow to insert css or JS scripts.py?",
                            "createdAt": "2023-02-12T17:13:38Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201825",
                            "body": "It would be great to see a white label option so we can resell the builder under our own brand. ;)",
                            "createdAt": "2023-02-12T17:09:49Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    },
                    {
                        "node": {
                            "id": "2201694",
                            "body": "Move away from wordpress and other website builders with this one. Speed, functionality, updates are great. The templates are well suited for most of businesses and they keep adding. Congrats to the team!",
                            "createdAt": "2023-02-12T15:47:43Z",
                            "user": {
                                "id": "0",
                                "username": "username",
                                "profileImage": "profilepicurl"
                            }
                        }
                    }
                ]
            }
        }
    }
}
