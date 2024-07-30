from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer       #pip install vaderSentiment
import spacy                                                               #pip install spacy

nlp = spacy.load("en_core_web_lg")                                         #python -m spacy download en_core_web_lg

# --- examples -------
tweet_list = [
    "Just watched a fantastic movie!",
    "The weather today is gloomy.",
    "Won the game tonight!",
    "Bought some trendy clothes today.",
    "Had an amazing dinner at the new restaurant. ",
    "The food at the party was not up to the mark. ",
    "What a beautiful day! ",
    "Loving my new dress! ",
    "The house needs some serious cleaning. ",
    "The show was a blast! ",
    "Had a great time at the dance class. ",
    "Enjoying the holiday season. ",
    "Can't wait for the vacation to start! ",
    "My new outfit is on point! ",
    "These shoes are hurting my feet. ",
    "The shirt I bought doesn't fit me. ",
    "Listening to my favorite song. ",
    "The concert was too crowded."
]


def find_subject_of_adjective(doc):
    for token in doc:
        if token.pos_ == "NOUN":
            subject = str(token)
            return subject


def TweetAnalyser(tweets):
    indexcount = 1
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweets:
        doc = nlp(tweet)
        for sent in doc.sents:
            vs = analyzer.polarity_scores(str(sent))
            if vs["compound"] > 0:
                emotion = "Positive"
            if vs["compound"] < 0:
                emotion = "Negative"
            if vs["compound"] == 0:
                emotion = "Neutral"
            subject = find_subject_of_adjective(sent)
            print(sent, (str(vs['compound'])))
            print(f"It was found that Tweet{indexcount} expressed a {emotion} emotion about {subject}.")
            indexcount += 1

TweetAnalyser(tweet_list)
    