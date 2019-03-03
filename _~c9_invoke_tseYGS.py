from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from time import perf_counter
import re


def summarize(article):

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
                #scores[x][y] = len(matches)

    """
    Sum the common words
    """
    total = []
    for x in range(len(scores)):
        total.append(sum(scores[x]))

    """
    Select the best sentences that meet the desired range of size reduction.
    Also, remove duplicate sentences.
    """

    guess = .5
    low_range = .70
    high_range = .80
    attempts = 0
    while True:
        selection = []

        # List the best sentences
        for s in range(len(total)):
            if total[s] > guess * max(total):
                selection.append(body[s])

        # Check and delete any replicate sentences; keeping only the first instance
        for x in reversed(range(len(selection))):
            if x != 0:
                for y in reversed(range(x)):
                    if selection[x] == selection[y]:
                        del selection[x]
                        break

        # Make summary
        summary = '\n'.join(selection)

        # Check if summary meets criteria
        if (len(article)-len(summary))/len(article) < low_range:
            guess = guess * 1.5
        elif (len(article)-len(summary))/len(article) > high_range:
            guess = guess * .75
        else:
            break

        # Allow for only five attempts at calibrating the percent reduction in size
        attempts += 1
        if attempts == 5:
            break

    return summary