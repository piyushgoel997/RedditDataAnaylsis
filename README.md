The data is collected using praw, a python library to access the data on Reddit using the Reddit API.
It is used to collect the top 100 threads (this number can be increased later, and is set to 100 right now due to processing constraints) on the subreddit r/CoronaVirus.

The following attributes of a thread are saved - title, selftext (body, if any), score (number of upvotes), url, created, id, comments (a list of mappings from the comment to the number of upvotes).
This data is then saved to a JSON, afterwards the processing is done on thread titles, selftext, comments.

Processing techniques used: removal of stop words, porter stemming.

Then 5 n-grams (uni, bi, tri, quad, penta) are calculated and the top 100 printed.
The n-grams are calculated in two ways - 1. just the count of occurrence of each n-gram, 2. instead of adding 1 for each occurrence, add the number of upvotes for that comment (thread in case of title, selftext).