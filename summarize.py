from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from time import perf_counter
import re

##### Base Function #####
def process_article(article):

    """
    Create a list elements for each sentence in the article.
    This will remain unmodified.
    """
    article = re.sub(r"\n(\n)+( )*", "\n\n", article)
    paragraphs = article.split("\n\n")
    body = []
    for p in paragraphs:
        if len(sent_tokenize(p)) == 1:
                continue
        else:
            body.extend(sent_tokenize(p))


    """
    Create a list of elements for each sentence,
    which contain a list of words from each sentence
    with stop words ommited
    """
    # set() time is O(1) while list time is O(n):
    # https://wiki.python.org/moin/TimeComplexity
    stop_words = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
                "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
                "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
                "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
                "he", "her", "here", "hers", "herself", "him","himself", "his", "how", "i", "i'm",
                "if", "in", "into", "is", "it", "its", "itself", "me", "more", "most", "my", "myself",
                "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves",
                "out", "over", "own", "s", "same", "she", "should", "so", "some", "such", "t", "than",
                "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these",
                "they", "this", "those", "through", "to", "too", "under", "until", "up", "very",
                "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom", "why",
                "with", "would", "you", "your", "yours", "yourself", "yourselves", ";", ":", ",", "'",
                "’", '’', '"', '“', '”', ".", "...", "?", "!", "-", "(", ")", "'d", "'re", "'s", "'ll",
                "'ve", "n't", "'m"])

    index = []
    for s in range(len(body)):
        words = word_tokenize(body[s])
        for w in range(len(words)):
            words[w] = words[w].lower()
        words = [w for w in words if not w in stop_words]
        index.append(words)


    """
    Convert the words in "index" to their stemmed counterpart,
    in order to find a greater likeness between words.
    """
    for s in range(len(index)):
        for w in range(len(index[s])):
            index[s][w] = PorterStemmer().stem(index[s][w])


    """
    Score the similarity of every sentence
    to every other sentence.
    """
    # Create a matrix of zero elements for scores
    scores = [[0 for s in range(len(index))] for s in range(len(index))]
    matches = 0
    for x in range(len(index)):
        for y in range(len(index)):
            if x != y:
                matches = [word for word in index[x] if word in index[y]]
                scores[x][y] = len(matches) / ((len(index[x])+len(index[y])) / 2)


    """
    Sum the scores for each sentence
    """
    total = []
    for x in range(len(scores)):
        total.append(sum(scores[x]))


    """
    Remove duplicate sentences and their respective score,
    leaving only the the first occurance of that sentence.
    """
    content = body.copy()
    for x in reversed(range(len(total))):
        for y in reversed(range(x)):
            if content[x] == content[y]:
                del content[x]
                del total[x]
                break

    return content, total

##### Extended Functions #####
def sumLimit(article, limit):

    """Start Performance Counter"""
    start = perf_counter()

    """Process the article"""
    content, total = process_article(article)

    """Create a summary with a specified number of sentences"""
    sort = sorted(total, reverse=True)
    best = set()

    if limit > len(total):
        limit = len(total)

    for i in range(limit):
        best.add(sort[i])

    parts = []
    for i in range(len(total)):
        if total[i] in best:
            parts.append(content[i])

    """Make Summary"""
    summary = '\n'.join(parts)

    """End Performance Counter"""
    end = perf_counter()

    """Get stats and format to strings"""
    art_len = str(len(article))
    sum_len = str(len(summary))
    reduction = str(round(((len(article)-len(summary))/len(article)) * 100, 2)) + '%'
    time = str(round(end-start, 2)) + 's'

    return {
        "summary" : summary,
        "art_len" : art_len,
        "sum_len" : sum_len,
        "reduction" : reduction,
        "time" : time
    }

def sumTarget(article, target):

    """Start Performance Counter"""
    start = perf_counter()

    content, total = process_article(article)

    """Determine the users target range"""
    low_range = float(target) * .01
    high_range = low_range + .09

    """
    Guess a score value that would remove nearly half of the article content
    when sentence is compared to it. Also keep track of attempts made to adjust
    the amount of content removed so as to not infinitely loop.
    """
    guess = .5
    attempts = 0

    """
    Select the best sentences.
    Determine whether or not the summary size is within users target range.
    Adjust guess value.
    Five attempts to make it fit.
    """
    while True:
        selection = []

        # List the best sentences
        for s in range(len(total)):
            if total[s] > guess * max(total):
                selection.append(content[s])

        # Make summary
        summary = '\n'.join(selection)

        # Look up article and summary lengths
        art_len = len(article)
        sum_len = len(summary)
        reduction = (art_len-sum_len)/art_len

        # Check if summary fit within users target range.
        # Adjust guess value
        if reduction < low_range:
            guess = guess * 1.5
        elif reduction > high_range:
            guess = guess * .75
        else:
            break

        # Five attempts to calibrate summary size
        attempts += 1
        if attempts == 5:
            break

    """End Performance Counter"""
    end = perf_counter()

    """Get stats and format to strings"""
    art_len = str(len(article))
    sum_len = str(len(summary))
    reduction = str(round(((len(article)-len(summary))/len(article)) * 100, 2)) + '%'
    time = str(round(end-start, 2)) + 's'

    return {
        "summary" : summary,
        "art_len" : art_len,
        "sum_len" : sum_len,
        "reduction" : reduction,
        "time" : time
    }