import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# ==========================================
# 🚀 INITIALIZATION OUTSIDE THE FUNCTION
# Loads only once into memory (RAM) for efficiency
# ==========================================
EMAIL_REGEX = re.compile(r'\S+@\S+')
PUNCT_TABLE = str.maketrans('', '', string.punctuation)
STOP_WORDS = set(stopwords.words('english'))
STEMMER = PorterStemmer()

def clean_text(text):
    # 1. Remove emails (using a pre-compiled regex for speed)
    text = EMAIL_REGEX.sub('', text)
    
    # 2. Remove emojis and non-ascii symbols
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # 3. Remove punctuation (using a pre-compiled translation table)
    text = text.translate(PUNCT_TABLE)
    
    # 4. Tokenize and convert to lowercase
    # PRO TIP: NLTK's `word_tokenize` can still be a bit slow. 
    # If you need EXTREME SPEED, you can replace this line with: `tokens = text.lower().split()`
    tokens = word_tokenize(text.lower())
    
    # 5. Remove stopwords and apply stemming
    # This uses the previously loaded STEMMER and STOP_WORDS for maximum efficiency
    cleaned_tokens = [STEMMER.stem(w) for w in tokens if w not in STOP_WORDS and w.isalnum()]
    
    return cleaned_tokens

# Testing
if __name__ == "__main__":
    sample = "The boy is running and sending emails to info@domain.org! 😊"
    
    text = """
    Hello! 😊 This is a test email@example.com. 
    Can you remove this? 👍 Also, check info@domain.org! 
    """
    
    text1 = "Hello! 😊 This is a test email@example.com. Can you remove this? 👍 Also, check info@domain.org!"
    
    print(clean_text(sample))
    print(clean_text(text))
    print(clean_text(text1))