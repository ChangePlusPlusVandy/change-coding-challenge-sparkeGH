#Access token: 1144331689080086528-IKiFLd6AOB37yZOmd5GL7xM6bUv6QQ
#Secret access token: YqblAvhZHYyzWyfq50uL1zLw6QnLn5pYOfLcER9HTTmtA
#API Key: tybNMmBDJ0zBZukMz3C5FrA1p
#API Key Secret: eTPlDaERikB1tderYpbXIPlFNrXflGvFcnmGQjX2fQmsoz4n7F
#GET https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=100

import requests
import json
import base64

client_key = 'tybNMmBDJ0zBZukMz3C5FrA1p'
client_secret = 'eTPlDaERikB1tderYpbXIPlFNrXflGvFcnmGQjX2fQmsoz4n7F'

key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type': 'client_credentials'
}

auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

auth_resp.json().keys()

access_token = auth_resp.json()['access_token']

search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

search_params = {
    'screen_name': 'elonmusk',
    'exclude_replies': True,
    'include_rts': False,
    'count': 3200
}

search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)

req = requests.get(search_url, headers=search_headers, params=search_params)
print(req.status_code)
elonData = req.json()

search_params = {
    'screen_name': 'kanyewest',
    'exclude_replies': True,
    'include_rts': False,
    'count': 3200
}

search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)

req = requests.get(search_url, headers=search_headers, params=search_params)
print(req.status_code)
kanyeData = req.json()

tweetData = [elonData, kanyeData]

for i in range(10):
    print(tweetData[1][i]['text'])
