# A set of tools for extracting simple, summary-type features
# from a corpus.
# The tools are available for instances of the TextDistiller class.

# Import necessary modules
import re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import config     # User-definable configuration
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

class TextDistiller:

    """
    Instances of this class are used to 'distill' a text corpus using 
    basic NLP techniques.
    """
    
    def __init__(self, raw_fulltext):
        self.crp_raw = raw_fulltext
        self.crp_clean = self.clean_text(self.crp_raw)
        stopword_list = config.tech_stopwords + config.eng_stopwords
        
        # When tokenizing the corpus, ignore stop words and words of
        # length = 1, which also excludes abbreviations like "e.g."
        # once the punctuation has been stripped.
        self.crp_toks = [word for word in word_tokenize(self.crp_clean)
                         if word not in stopword_list
                         and len(word) > 1]
        self.word_freqs = FreqDist(word for word in self.crp_toks)
    
    def clean_text(self, raw_text):
        # This function scrubs extra white spaces and non-letter characters from
        # the input text, and converts it to lowercase. 

        processed_text = re.sub(r"\s+", " ", raw_text)  # Delete extra white spaces
        processed_text = processed_text.lower()         # Convert to lowercase
        processed_text = re.sub(r"[^a-zA-Z]", " ", processed_text) # allow only letters 
        return processed_text

    def gen_bigrams(self, min_freq = config.bg_min_freq):
        # Generate ranked bigrams as a list of tuples from the tokenized corpus.
        
        bg_finder = BigramCollocationFinder.from_words(self.crp_toks,
                                                       window_size = config.bg_win)
        bg_finder.apply_freq_filter(min_freq)
        bg_ranked = bg_finder.nbest(BigramAssocMeasures.pmi, config.bg_count)
        return bg_ranked