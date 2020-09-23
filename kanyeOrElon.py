#Important info for Twitter API permissions
#Access token: '1144331689080086528-IKiFLd6AOB37yZOmd5GL7xM6bUv6QQ'
#Secret access token: 'YqblAvhZHYyzWyfq50uL1zLw6QnLn5pYOfLcER9HTTmtA'
#API Key: tybNMmBDJ0zBZukMz3C5FrA1p
#API Key Secret: eTPlDaERikB1tderYpbXIPlFNrXflGvFcnmGQjX2fQmsoz4n7F
#GET https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=100

#just some packages needed to pull the tweets from Twitter and run the game
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
timelineHeaders = {
    'Authorization': 'Bearer {}'.format(access_token)
}

#base URL for user timeline API request, onto which parameters are appended
timelineURL = '{}1.1/statuses/user_timeline.json'.format(base_url)

#Pulls 200 Tweets from @elonmusk and stores them in elonData
#NOTE: While count here is 3200, each API request returns a maximum of 200 Tweets, meaning count is functionally 200
#NOTE: parameter 'tweet_mode' set to 'extended' because some tweets would truncate output by default, instead appending a Twitter URL to the text
#NOTE: parameters to exclude replies and retweets exist; they are noted in comments below but were not used because they were overly restrictive
#      (For instance, not all replies tag the user that began the thread, and therefore should be included in the game)
timelineParameters = {
    'tweet_mode':'extended',
    'screen_name': 'elonmusk',
    #'exclude_replies': True,
    #'include_rts': False,
    'count': 3200
}

req = requests.get(timelineURL, headers=timelineHeaders, params=timelineParameters)
#print(req.status_code)
elonData = req.json()

#Pulls 200 Tweets from @kanyewest and stores them in kanyeData
timelineParameters = {
    'tweet_mode':'extended',
    'screen_name': 'kanyewest',
    #'exclude_replies': True,
    #'include_rts': False,
    'count': 3200
}

req = requests.get(timelineURL, headers=timelineHeaders, params=timelineParameters)
#print(req.status_code)
kanyeData = req.json()

#Filters out tweets containing URLs (identified by "http") and tags (identified by "@"), then stores them in a dictionary of two lists
elonTweets = []
kanyeTweets = []
for i in range(len(elonData)):
    if not('http' in elonData[i]['full_text']) and not('@' in elonData[i]['full_text']):
        elonTweets.append(elonData[i]['full_text'])
for i in range(len(kanyeData)):
    if not('http' in kanyeData[i]['full_text']) and not('@' in kanyeData[i]['full_text']):
        kanyeTweets.append(kanyeData[i]['full_text'])
tweetData = {"k": kanyeTweets,"e": elonTweets}

#Initializes variables for tracking player's stats
trueKanyes = 0
falseKanyes = 0
trueElons = 0
falseElons = 0
roundsPlayed = 0
userInput = "k"
keyIndex = "arbitrary start value"
tweetIndex = 0

#Used to test number of tweets included in the game and list their text
#print(len(tweetData["k"]))
#for i in range(len(tweetData["k"])):
#    print(tweetData["k"][i])
#print(len(tweetData["e"]))
#for i in range(len(tweetData["e"])):
#    print(tweetData["e"][i])

#Say hello and introduce rules
print("         Let's play Kanye or Elon!          \n")
print(" The rules are simple: we give you a tweet, \n")
print(" and you tell us whether you think Kanye or \n")
print("            Elon is responsible.            \n")
print("   Enter \"k\" if you think it was Kanye,   \n")
print("  and enter \"e\" if you think it was Elon. \n")
print("  Enter \"q\" to end the game and view your \n")
print("           stats for this round.            \n")
print("       Good luck, young grasshopper.        \n")

#begin game loop
while not(userInput=="q"):
    #initialize indices for grabbing tweets, but only when the user previously entered a valid guess, so that skipping isn't enabled
    if userInput == "k" or userInput == "e":
        coinToss = random.randint(0,1)
        if coinToss == 0:
            keyIndex = "k"
        else:
            keyIndex = "e"
        tweetIndex = random.randint(0, len(tweetData[keyIndex])-1)

    #pose the question
    print("Your tweet is: ")
    print(tweetData[keyIndex][tweetIndex]+"\n")
    print("So...Kanye or Elon?\n")

    #accept a response and determine accuracy
    userInput = input()
    #valid response (either 'k' or 'e')
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
    #ending the game ('q')
    elif userInput == "q":
        print("Thanks for playing!\n")
    #invalid response (any other string)
    else:
        print("  That doesn't look like a valid response.  \n")
        print(" Remember: \"k\" for Kanye, \"e\" for Elon, \n")
        print("or \"q\" to end the game and get your stats.\n")

#calculate and print some stats for the player if they played the game
if roundsPlayed>0:
    print("Score: "+str(trueKanyes+trueElons)+" out of "+str(roundsPlayed)+" tweets correctly identified")
    print("Accuracy: "+str((trueKanyes+trueElons)/roundsPlayed)+"\n")
    print("Incorrect Guesses for Kanye: "+str(falseKanyes))
    print("Incorrect Guess for Elon: "+str(falseElons))
    #Determine tendency of user to err in one direction, but only if errors were made
    if not(falseKanyes + falseElons == 0):
        if falseKanyes > falseElons:
            print("You had a slight tendency to guess Yeezus over Elon.\n")
        elif falseKanyes == falseElons:
            print("Even when you were wrong, you balanced guessing Elon and Kanye. Thanos would be proud.\n")
        else:
            print("You had a slight tendency to guess the Muskrat over Kanye.")
    #list accuracies for Kanye and Elon individually, but only when both users have been invoked at least once
    if (trueKanyes+falseElons) > 0 and (trueElons+falseKanyes) > 0:
        print("Kanye Accuracy: "+str((trueKanyes)/(trueKanyes+falseElons))+"\n")
        print("Elon Accuracy: "+str((trueElons)/(trueElons+falseKanyes))+"\n")
else:
    print("You didn't actually play the game, which means you're either testing\n")
    print("edge cases or you're a total loser. Either way, no stats for you.   \n")

#NOTE:  Due to an abundance of links and user tags in any given user's timeline, the number of Tweets available for use in this game
#       is at any time significantly lower than the 200 pulled from the API. This could be addressed by including those Tweets while
#       modifying their text to remove any links or Twitter tags.
