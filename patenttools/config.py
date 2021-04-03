# User-definable configuration for PatentTools.
# Variables defined here are imported by outside functions as needed.

# Define stop words to be ignored in word frequency counts and related
# analyses.
cust_stopwords = ["method",
                  "comprising", 
                  "fig", 
                  "figure", 
                  "ex", 
                  "example",
                  "may",
                  "embodiment",
                  "including",
                  "limited",
                  "claim", 
                  "invention", 
                  "description",
                  "describe",
                  "technical", 
                  "related",
                  "patent",
                  "application",
                  "thereof",
                  "therein",
                  "yet",
                  "eg",
                  "et",
                  "al",
                  "etc",
                  "ex",]

# When summarizing the patents cited by a user-specified patent,
# what is the maximum number of distinct, most common assignees to display? 
# The remainder will be aggregated as "other".
top_cited_cutoff = 3