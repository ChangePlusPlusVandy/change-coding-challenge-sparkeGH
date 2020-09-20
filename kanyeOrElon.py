#Access token: '1144331689080086528-IKiFLd6AOB37yZOmd5GL7xM6bUv6QQ'
#Secret access token: 'YqblAvhZHYyzWyfq50uL1zLw6QnLn5pYOfLcER9HTTmtA'
#API Key: tybNMmBDJ0zBZukMz3C5FrA1p
#API Key Secret: eTPlDaERikB1tderYpbXIPlFNrXflGvFcnmGQjX2fQmsoz4n7F
#GET https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=100

#just some packages needed to pull the tweets from Twitter
import requests
import json
import base64
import random

#Authentication via Twitter API client information
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

#setting up inputs for the pull requests from the API
search_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

#search_url = '{}1.1/statuses/user_timeline.json'.format(base_url)
search_url = '{}1.1/search/tweets.json'.format(base_url)

#Pulls 3200 Tweets from @elonmusk, excluding replies and retweets and stores them in elonData
search_params = {
    'q': 'from:elonmusk -filter:links -filter:media -filter:retweets -filter:replies',
    'result_type':'recent',
    'tweet_mode':'extended',
    #'screen_name': 'elonmusk',
    #'exclude_replies': True,
    #'include_rts': False,
    'count': 3200
}

req = requests.get(search_url, headers=search_headers, params=search_params)
#print(req.status_code)
elonData = req.json()

#Pulls 3200 Tweets from @kanyewest, excluding replies and retweets and stores them in kanyeData
search_params = {
    'q': 'from:kanyewest -filter:links -filter:images -filter:retweets -filter:replies',
    'result_type':'recent',
    'tweet_mode':'extended',
    #'screen_name': 'kanyewest',
    #'exclude_replies': True,
    #'include_rts': False,
    'count': 3200
}

req = requests.get(search_url, headers=search_headers, params=search_params)
#print(req.status_code)
kanyeData = req.json()

#Stores Kanye's and Elon's tweets in separate elements of an dictionary
tweetData = {"k": kanyeData,"e": elonData}

#Initializes variables for tracking player's stats
trueKanyes = 0
falseKanyes = 0
trueElons = 0
falseElons = 0
roundsPlayed = 0
userInput = "arbitrary initial value"
keyIndex = "k"
tweetIndex = 0

print(len(tweetData["k"]['statuses']))
for i in range(len(tweetData["k"]['statuses'])):
    print(tweetData["k"]['statuses'][i]['full_text'])
print(len(tweetData["e"]['statuses']))
for i in range(len(tweetData["e"]['statuses'])):
    print(tweetData["e"]['statuses'][i]['full_text'])

#Say hello and introduce rules
print("         Let's play Kanye or Elon!          \n")
print(" The rules are simple: we give you a tweet, \n")
print(" and you tell us whether you think Kanye or \n")
print("            Elon is responsible.            \n")
print(" Enter \"k\" if you think it was Kanye, \n")
print("and enter \"e\" if you think it was Elon.\n")
print("Enter \"q\" to end the game and view your\n")
print("           stats for this round.            \n")
print("       Good luck, young grasshopper.        \n")

#begin game loop
while not(userInput=="q"):
    #initialize indices for grabbing tweets, but only when the user previously entered a valid guess
    if userInput == "k" or userInput == "e":
        coinToss = random.randint(0,1)
        if coinToss == 0:
            keyIndex = "k"
        else:
            keyIndex = "e"
        tweetIndex = random.randint(0, len(tweetData[keyIndex]['statuses'])-1)

    #pose the question
    print("Your tweet is: ")
    print(tweetData[keyIndex]['statuses'][tweetIndex]['full_text']+"\n")
    print("So...Kanye or Elon?\n")

    #accept a response and determine accuracy
    userInput = input()
    if userInput == "k" or userInput == "e":
        roundsPlayed += 1
        if keyIndex == userInput:
            print("Correct! Great job.\n")
            if userInput == "k":
                trueKanyes += 1
            else:
                trueElons += 1
        else:
            print("Wrong! Better luck next time.\n")
            if userInput == "k":
                falseKanyes += 1
            else:
                falseElons += 1

    elif userInput == "q":
        print("Thanks for playing!\n")
    else:
        print("  That doesn't look like a valid response.  \n")
        print(" Remember: \"k\" for Kanye, \"e\" for Elon, \n")
        print("or \"q\" to end the game and get your stats.\n")

#calculate and print some stats for the player
if roundsPlayed>0:
    print("Score: "+str(trueKanyes+trueElons)+" out of "+str(roundsPlayed)+" tweets correctly identified")
    print("Accuracy: "+str((trueKanyes+trueElons)/roundsPlayed)+"\n")
    print("Incorrect Guesses for Kanye: "+str(falseKanyes))
    print("Incorrect Guess for Elon: "+str(falseElons))
    if falseKanyes > falseElons:
        print("You had a slight tendency to guess Yeezus over Elon.\n")
    elif falseKanyes == falseElons:
        print("Even when you were wrong, you balanced guessing Elon and Kanye. Thanos would be proud.\n")
    else:
        print("You had a slight tendency to guess the Muskrat over Kanye.")
    if (trueKanyes+falseElons) > 0 and (trueElons+falseKanyes) > 0:
        print("Kanye Accuracy: "+str((trueKanyes)/(trueKanyes+falseElons))+"\n")
        print("Elon Accuracy: "+str((trueElons)/(trueElons+falseKanyes))+"\n")
else:
    print("You didn't actually play the game, which means you're either testing\n")
    print("edge cases or you're a total loser. Either way, no stats for you.   \n")
#print(tweetData[1]['statuses'][i]['full_text']+"\n")
