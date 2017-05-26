# Analyze article content
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Use NLTK to parse article information
def full_article(title):

  stop_words    = set(stopwords.words('english'))
  word          = word_tokenize(title)
  title_t1_fail = [w for w in word if w in stop_words]
  title_t1_pass = [w for w in word if not w in stop_words]

#  print('\nPassed', title_t1_pass, '\nFailed', title_t1_fail)
#  print(summary)
