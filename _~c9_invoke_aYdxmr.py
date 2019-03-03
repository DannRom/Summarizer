from nltk.tokenize import sent_tokenize, word_tokenize
import re


def similarity(sent1, sent2):
    """Provide a score value which determines how similar two sentences are."""
    # Split the sentences into words
    list1 = word_tokenize(sent1)
    list2 = word_tokenize(sent2)

    # List of words present in each sentence
    shared = [x for x in list1 if x in list2]

    # The score will range from 0.0 to 1.0
    return len(shared) / ((len(list1) + len(list2)) / 2)


def format_sentence(sentence):
    """Remove all characters which are not a-z, A-Z, 0-9"""
    # \W matches any character which is not a words character
    # '' is the replacement of these none word characters
    # The + is a repetition qualifier
    # https://stackoverflow.com/questions/1276764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python
    # https://docs.python.org/3/library/re.html
    sentence = re.sub(r'\W+', '', sentence)
    return sentence


def rank(article):
    """Score the similarity of each two sentences"""
    # Split article into paragraphs
    paragraphs = article.split("\n\n")

    # Split paragraphs into sentences
    sentences = []
    for p in paragraphs:
        sentences.extend(sent_tokenize(p))

    print(sentences)

    # Split the article into sentences
    #sentences = sent_tokenize(article)

    # Initialize a list of lists with zeros
    n = len(sentences)
    scores = [[0 for x in range(n)] for x in range(n)]

    # Calculate the similarity of each sentences to every other,
    # and the similarity value in scores.
    for i in range(n):
        for j in range(n):
            scores[i][j] = similarity(sentences[i], sentences[j])

    # Initialize a dictionary for sentences and values called grade
    grade = {}
    value = 0
    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                value += scores[i][j]
        grade[format_sentence(sentences[i])] = value

    return grade


def best(paragraph, grade):
    """Determine the best sentence within the paragraph"""
    # Split the paragraph into sentences
    sentences = sent_tokenize(paragraph)

    # Ignore short paragraphs
    if len(sentences) < 2:
        return ""

    # Create a new string with the best sentence
    best_sentence = ""
    max_value = 0
    for s in sentences:
        strip = format_sentence(s)
        if strip:
            if grade[strip] > max_value:
                max_value = grade[strip]
                best_sentence = s

    return best_sentence


def summarize(article):
    """Summarize"""
    # Grade the article
    grade = rank(article)

    # Split article into paragraphs
    paragraphs = article.split("\n\n")

    # Build the summary
    summary = []
    for p in paragraphs:
        sentence = best(p, grade)
        if sentence:
            summary.append(sentence)

    return ("\n").join(summary)