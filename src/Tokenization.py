"""
This is a sample program that I stried up in order to unserstand the Tokennization
Note: This is not the part of the code
"""
import re
import string
from nltk.tokenize import word_tokenize

# Sample text with punctuation, emojis, and emails
text = """
Hello! 😊 This is a test email@example.com. 
Can you remove this? 👍 Also, check info@domain.org! 
"""

def clean_text(text):
    # Step 1: Remove emails
    text = re.sub(r'S+@S+', '', text)
    
    # Step 2: Remove emojis and symbols
    emoji_pattern = re.compile(
        "["
        "U0001F600-U0001F64F"  # Emoticons
        "U0001F300-U0001F5FF"  # Symbols & pictographs
        "U0001F680-U0001F6FF"  # Transport & map symbols
        "U0001F700-U0001F77F"  # Alchemical symbols
        "U0001F780-U0001F7FF"  # Geometric Shapes Extended
        "U0001F800-U0001F8FF"  # Supplemental Arrows-C
        "U0001F900-U0001F9FF"  # Supplemental Symbols and Pictographs
        "U0001FA00-U0001FA6F"  # Chess Symbols
        "U0001FA70-U0001FAFF"  # Symbols and Pictographs Extended-A
        "U00002702-U000027B0"  # Dingbats
        "U000024C2-U0001F251" 
        "]+", 
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # Step 3: Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Step 4: Tokenize and rejoin (optional, removes extra whitespace)
    tokens = word_tokenize(text)
    cleaned_text = ' '.join(tokens)
    
    return cleaned_text

# Clean the text and make it lowercase
cleaned_text = clean_text(text).lower()
print("Original Text:", text)
print("Cleaned Text:", cleaned_text)
