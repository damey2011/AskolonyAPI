**Title**
Accounts
- Get/Update/Delete the user information:
    Endpoint: /accounts/user/<username>/
    Method: GET, PATCH, DELETE
    Returns data in format:
        {
            "id": 1,
            "email": "neefemee@gmail.com",
            "first_name": "",
            "last_name": "",
            "full_name": "",
            "username": "oluwanifemi",
            "bio": "I love God",
            "picture": "http://127.0.0.1:8000/media/default/user.png",
            "followings": 0,
            "followers": 0,
            "profile": {
                "college": "NA",
                "works": "Senseandserve",
                "lives": "NA",
                "facebook_link": "http://facebook.com",
                "twitter_link": "http://twitter.com",
                "linked_in_profile": "http://linkedin.com"
            },
            "stats": {
                "reads": 0,
                "comments": 0,
                "writes": 0,
                "ups": 0,
                "downs": 0
            }
        }

- Create account:
    Endpoint: /accounts/user/
    Method: POST
    Receives Data in the format:
        {
            'email': REQUIRED
            'password', REQUIRED (at least 6 digits)
            'first_name', OPTIONAL
            'last_name', OPTIONAL
            'username', OPTIONAL
        }

- Follow User
    endpoint: /accounts/user/<username>/follow/
    method: POST
    requires Authentication: True
    Receives no payload

- UnFollow User
    endpoint: /accounts/user/<username>/unfollow/
    method: POST
    requires Authentication: True
    Receives no payload