import datetime as dt
import json

import nltk
import praw
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# import re
ps = PorterStemmer()
# nltk.download('punkt')
# nltk.download('stopwords')

tokenizer = nltk.RegexpTokenizer(r"\w+")


# url_reg_exp = r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(
# )<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])) '''


def n_gram(n, sentences, scores, use_scores=True):
    counts = {}
    for words, s in zip(sentences, scores):
        for i in range(len(words) - n + 1):
            curr = " ".join(words[i:i + n])
            # just to ignore urls in the n-grams
            if curr.count("http") > 0 or curr.count("www") > 0 or curr.count("com") > 0 or curr.count("reddit") > 0:
                continue
            cc = 1
            if use_scores:
                cc = s
            if curr in counts:
                counts[curr] = counts[curr] + cc
            else:
                counts[curr] = cc
    return counts


def print_top(grams, top):
    for x in sorted([(value, key) for (key, value) in grams.items()], reverse=True)[:top]:
        print(x)


# please substitute your own id, etc here from the reddit api account
reddit = praw.Reddit(client_id="#", client_secret="#", user_agent="#", username="#")
subreddit = reddit.subreddit("Coronavirus")

data = {'threads': []}
i = 0
# just taking 100 right now since it was taking long, and reddit has a upper limit of 1000.
# But even the top 100 give a pretty good idea of what the people are talking about.
for thr in subreddit.top(limit=100):
    # print(submission.__dict__.keys())
    comments = []
    thr.comments.replace_more(limit=None)
    for c in thr.comments.list():
        comments.append({
            "comment": c.body,
            "score": c.score
        })
    key_dict = {
        "titles": thr.title,
        "selftext": thr.selftext,
        "score": thr.score,
        "url": thr.url,
        "created": dt.datetime.fromtimestamp(thr.created).__str__(),
        "id": thr.id,
        "comments": comments
    }
    data['threads'].append(key_dict)
    print(i)
    i += 1

with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

sentences = []
scores = []

with open("data.json", "r") as f:
    data = json.load(f)
    # n-grams weighted by the score (up-votes), since that roughly is the number of people that like/agree with
    # that comment or post.
    for t in data['threads']:
        if t["titles"] != "":
            sentences.append(t["titles"])
            scores.append(t["score"] + 1)
        if t["selftext"] != "":
            sentences.append(t["selftext"])
            scores.append(t["score"] + 1)
        for comment in t["comments"][1:]:
            # the [1:] is there to remove the first comment which is always by the bot.
            if comment["comment"] != "":
                sentences.append(comment["comment"])
                scores.append(comment["score"] + 1)

print("Data loaded.")
print(len(sentences))

new_sentences = []
for s in sentences:
    # not removing the urls because it was really slow.
    # sent = re.sub(url_reg_exp, "", s)
    words = tokenizer.tokenize(s.lower())
    words = [ps.stem(w) for w in words if w not in stopwords.words('english')]
    new_sentences.append(words)
sentences = new_sentences

print("Data tokenized")

# more n-grams can be added later if required.
unigrams_scored = n_gram(1, sentences, scores, use_scores=True)
print("===============Scored Unigrams===============")
print_top(unigrams_scored, 100)
bigrams_scored = n_gram(2, sentences, scores, use_scores=True)
print("===============Scored Bigrams===============")
print_top(bigrams_scored, 100)
trigrams_scored = n_gram(3, sentences, scores, use_scores=True)
print("===============Scored Trigrams===============")
print_top(trigrams_scored, 100)
quadgrams_scored = n_gram(4, sentences, scores, use_scores=True)
print("===============Scored Quadgrams===============")
print_top(quadgrams_scored, 100)
pentagrams_scored = n_gram(5, sentences, scores, use_scores=True)
print("===============Scored Pentagrams===============")
print_top(pentagrams_scored, 100)

unigrams = n_gram(1, sentences, scores, use_scores=False)
print("===============Unscored Unigrams===============")
print_top(unigrams, 100)
bigrams = n_gram(2, sentences, scores, use_scores=False)
print("===============Unscored Bigrams===============")
print_top(bigrams, 100)
trigrams = n_gram(3, sentences, scores, use_scores=False)
print("===============Unscored Trigrams===============")
print_top(trigrams, 100)
quadgrams = n_gram(4, sentences, scores, use_scores=False)
print("===============Unscored Quadgrams===============")
print_top(quadgrams, 100)
pentagrams = n_gram(5, sentences, scores, use_scores=False)
print("===============unscored Pentagrams===============")
print_top(pentagrams, 100)
