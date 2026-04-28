"""
Indexer Module for PySearch
---------------------------
This script builds the core Inverted Index from the raw crawled data (raw.jsonl). 
To prevent Out-of-Memory (OOM) crashes with massive datasets, 
it streams the file line-by-line, maintaining O(1) auxiliary memory per document. 
It cleans the text using the tokenization pipeline and maps each unique term to a 
Hash Map containing its source URIs and Term Frequencies (TF). The final structure 
is saved to disk, enabling O(1) time complexity for future search lookups.
"""

import json
import os
# Importing function from the fast Tokenization file
from Tokenization import clean_text

# ==========================================
# 📂 PATH SETUP (Static Absolute Paths)
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

INPUT_FILE = os.path.join(DATA_DIR, "raw.jsonl")
OUTPUT_INDEX_FILE = os.path.join(DATA_DIR, "inverted_index.json")
DOCS_STORE_FILE = os.path.join(DATA_DIR, "docs_store.json")

def build_inverted_index(input_path, output_index_path, output_store_path):
    print("Inverted Index and Document Store generation is starting...")
    inverted_index = {}
    docs_store = {} # Dictionary to store text previews for snippets
    
    try:
        # Line-by-line read for O(1) space complexity
        with open(input_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file):
                try:
                    # Convert JSON line to dictionary
                    doc = json.loads(line.strip())
                    uri = doc.get("uri", "")
                    text = doc.get("text", "")
                    
                    if not uri or not text:
                        continue
                    
                    # Store a small chunk of text (800 chars) for snippets
                    if uri not in docs_store:
                        clean_preview = " ".join(text[:800].split())
                        docs_store[uri] = clean_preview

                    # 🚀 FAST TOKENIZATION: Clean text and get tokens
                    tokens = clean_text(text)
                    
                    # ==========================================
                    # 🧠 INVERTED INDEX LOGIC
                    # ==========================================
                    for token in tokens:
                        if token not in inverted_index:
                            inverted_index[token] = {}
                        
                        # Counting Term Frequency (TF)
                        if uri not in inverted_index[token]:
                            inverted_index[token][uri] = 1
                        else:
                            inverted_index[token][uri] += 1
                            
                except json.JSONDecodeError:
                    print(f"Skipping Line {line_num}: JSON parsing error.")
                    continue
                
                # Progress Update
                if (line_num + 1) % 50 == 0:
                    print(f"{line_num + 1} documents indexed...")
                    
    except FileNotFoundError:
        print(f"Error: Input file not found at path: {input_path}")
        print("Make sure you have run the Crawler and raw.jsonl exists.")
        return

    # Saving Files to Disk
    print("Saving Inverted Index to disk...")
    with open(output_index_path, 'w', encoding='utf-8') as idx_file:
        json.dump(inverted_index, idx_file, ensure_ascii=False, indent=2)
        
    print("Saving Document Store for snippets to disk...")
    with open(output_store_path, 'w', encoding='utf-8') as doc_file:
        json.dump(docs_store, doc_file, ensure_ascii=False, indent=2)
        
    print("\nSuccess! Index and Document Store have been saved.")

if __name__ == "__main__":
    build_inverted_index(INPUT_FILE, OUTPUT_INDEX_FILE, DOCS_STORE_FILE)