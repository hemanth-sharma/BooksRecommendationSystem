import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

# lowercasing, remove punctuation, remove stop words (like "the", "is")
# word lemmatization ("processing" > "process")
nltk.download("stopwords")
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def clean_text(text):
    """
    Clean and preprocess text.
    """

    text = text.lower().replace("-", " ")
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text) # will return a list of tokens
    cleaned_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    cleaned_text = " ".join(cleaned_tokens)

    return cleaned_text
