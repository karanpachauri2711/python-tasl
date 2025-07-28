


import tweepy

# Replace with your actual credentials
api_key = input('YOUR_API_KEY')
api_secret = input('YOUR_API_SECRET')
access_token = input('YOUR_ACCESS_TOKEN')
access_token_secret = input('YOUR_ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Post a tweet
tweet = "Hello, Twitter (X)! This is a tweet from Python. 🐍🚀"
api.update_status(tweet)

print("Tweet posted successfully!")