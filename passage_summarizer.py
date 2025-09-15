# Purpose: Passage summarization logic using spaCy + TF-IDF

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
import string
import math
from collections import defaultdict

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def summarize_text(text, num_sentences=3):
    """
    Extractive text summarization using TF-IDF with NLTK
    """
    try:
        sentences = sent_tokenize(text)
        if len(sentences) <= num_sentences:
            return sentences

        stop_words = set(stopwords.words('english') + list(string.punctuation))
        all_words = [word_tokenize(s.lower()) for s in sentences]
        filtered_sentences = [[w for w in words if w not in stop_words and w.isalnum()] for words in all_words]

        # Document frequency (DF)
        word_df = defaultdict(int)
        for sent in filtered_sentences:
            unique = set(sent)
            for w in unique:
                word_df[w] += 1

        total_sents = len(sentences)
        idf = {w: math.log(total_sents / df) if df > 0 else 0 for w, df in word_df.items()}

        # Sentence scores using TF-IDF
        sentence_scores = {}
        for i, sent_words in enumerate(filtered_sentences):
            if not sent_words:
                continue
            tf = FreqDist(sent_words)
            score = sum((tf[w] / len(sent_words)) * idf.get(w, 0) for w in sent_words)
            sentence_scores[i] = score

        if not sentence_scores:
            return ["No meaningful summary could be generated."]

        top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = [sentences[i] for i in sorted(top_sentences)]

        return summary

    except Exception as e:
        return [f"Summarization error: {str(e)}"]