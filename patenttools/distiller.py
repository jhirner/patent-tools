# Import necessary modules
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

class TextDistiller:

    """
    Instances of this class are used to 'distill' a text corpus by extracting
    a user-defined number of sentences that are most representative of the overall text.
    Sentences are selected based on the average frequency of their constituent words
    within the broader corpus.
    """
    
    def __init__(self, raw_fulltext):
        self.fulltext_raw = raw_fulltext
        self.fulltext_clean = self.clean_text(self.fulltext_raw)
        self.word_freqs = self.get_word_freq(self.fulltext_clean)
    
    def clean_text(self, raw_text):
        # This function scrubs extra white spaces and non-letter characters from
        # the input text, and converts it to lowercase. 

        processed_text = re.sub(r"\s+", " ", raw_text)  # Delete extra white spaces
        processed_text = processed_text.lower()         # Convert to lowercase
        processed_text = re.sub(r"[^a-zA-Z]", " ", processed_text) # allow only letters 
        return processed_text


    def get_word_freq(self, cleaned_corpus):
        # This function generates a dict showing the frequency of each non-stopword
        # word in the corpus, normalized to the most frequent word (i.e.: max = 1).

        # First, generate counts for each word.
        word_cts = {}
        stopword_list = stopwords.words("english")
        for word in word_tokenize(cleaned_corpus):
            if word not in stopword_list:
                if word not in word_cts.keys():
                    word_cts[word] = 1
                else:
                    word_cts[word] += 1

        # Then use the counts to determine frequency.
        word_freq = {}
        for word in word_cts.keys():
            word_freq[word] = word_cts[word] / max(word_cts.values())

        return word_freq


    def score_sentences(self, raw_text, word_freqs):
        # This function scores each sentence based on the a dict of frequencies
        # each of its constituent words shows up in the corpus.
        # It returns a dict of scored sentences.

        sent_scores = {}
        sent_tokens = sent_tokenize(raw_text)
        for sentence in sent_tokens:
            score = 0
            for word in word_tokenize(sentence):
                if word.lower() in word_freqs.keys():
                    score += word_freqs[word.lower()]
            sent_scores[sentence] = score / len(word_tokenize(sentence))

        return sent_scores


    def pick_summary_sents(self, sent_score_dict, num_top_sentences):
        # This function selects the num_top_sentences-most highly ranked sentences
        # and returns them.

        ranked_sent = {}
        for sentence in sent_score_dict.keys():
            if sent_score_dict[sentence] not in ranked_sent.keys():
                ranked_sent[sent_score_dict[sentence]] = [sentence]
            else:
                ranked_sent[sent_score_dict[sentence]].append(sentence)

        top_scores = sorted(list(ranked_sent.keys()), reverse = True)[:num_top_sentences]

        top_sentences = [ranked_sent[score][0] for score in top_scores]

        return top_sentences


    def highlights(self, num_top_sentences):
        # This function is the manager for Text Distiller. Call it with a
        # the number of sentences to select for the summary.

        # Clean up the corpus, calculate frequencies of each word, and use word
        # frequencies to assign a score to each sentence.

        self.scored_sents = self.score_sentences(self.fulltext_raw, self.word_freqs)

        self.sel_sentences = self.pick_summary_sents(self.scored_sents, num_top_sentences)

        return self.sel_sentences