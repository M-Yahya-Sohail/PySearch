"""
Search and Ranking Engine for PySearch
--------------------------------------
This script is the main interface for the search engine.
It takes a user's search query, cleans the text, and looks for matching
words in the Inverted Index. To make sure the best results come first,
it uses the TF-IDF formula to score and rank the documents based on relevance.
While we have already captured the Term Frequency (TF) in our Inverted Index, we still need to implement the Inverse Document Frequency (IDF) logic. In the worst-case scenario, without a proper ranking system, the search engine would display the most irrelevant and useless links at the top. Therefore, we must mathematically score these results to ensure accuracy and relevance.
"""

import json
import os
import math
import re  # Snippet highlighter ke liye add kiya
from Tokenization import clean_text

# ==========================================
# 📂 PATH SETUP
# ==========================================
INDEX_FILE = r"C:\Users\user\Documents\GitHub\PySearch\data\inverted_index.json"
DOCS_STORE_FILE = (
    r"C:\Users\user\Documents\GitHub\PySearch\data\docs_store.json"  # Nayi file ka path
)


class PySearchEngine:
    def __init__(self, index_path, docs_path):
        print("Loading Inverted Index and Document Store into memory... Please wait.")
        with open(index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

        with open(docs_path, "r", encoding="utf-8") as f:
            self.docs_store = json.load(f)

        # Calculate the total number of documents for IDF calculation
        self.total_docs = self._calculate_total_docs()
        print(f"Index loaded successfully! Total indexed documents: {self.total_docs}")

    def _calculate_total_docs(self):
        # Extract total unique URLs by adding them to a set
        unique_docs = set()
        for token, docs in self.index.items():
            for doc_uri in docs.keys():
                unique_docs.add(doc_uri)
        return max(1, len(unique_docs))  # Max 1 to prevent Divide by Zero errors

    # ==========================================
    # ✂️ SNIPPET GENERATOR LOGIC
    # ==========================================
    def _generate_snippet(self, text, tokens):
        lower_text = text.lower()
        for token in tokens:
            idx = lower_text.find(token)
            if idx != -1:
                # Word found! Uske aage peeche ka context uthao
                start = max(0, idx - 50)
                end = min(len(text), idx + 80)
                snippet = text[start:end]

                # HTML <b> tags lagao taake UI mein bold nazar aaye
                highlighted_snippet = re.sub(
                    f"({token})", r"<b>\1</b>", snippet, flags=re.IGNORECASE
                )
                return "..." + highlighted_snippet.strip() + "..."

        # Agar exact match preview mein na mile toh shuru ka text bhej do
        return text[:100] + "..."

    def search(self, query, page=1, page_size=10):
        tokens = clean_text(query)
        if not tokens:
            return [], 0

        scores = {}
        for token in tokens:
            if token in self.index:
                doc_freq = len(self.index[token])
                idf = math.log10(self.total_docs / doc_freq)
                for uri, tf in self.index[token].items():
                    if uri not in scores:
                        scores[uri] = 0
                    scores[uri] += tf * idf

        ranked_results = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        total_matches = len(ranked_results)

        # Pagination Logic (Slice the array)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        final_results = []
        for uri, score in ranked_results[start_idx:end_idx]:
            text_preview = self.docs_store.get(uri, "No text preview available.")
            snippet = self._generate_snippet(text_preview, tokens)
            final_results.append({"url": uri, "score": score, "snippet": snippet})

        return final_results, total_matches


# ==========================================
# 🚀 INTERACTIVE TERMINAL
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(INDEX_FILE) or not os.path.exists(DOCS_STORE_FILE):
        print("Error: Required files not found. Please run indexer.py first.")
    else:
        engine = PySearchEngine(INDEX_FILE, DOCS_STORE_FILE)

        print("\n" + "=" * 40)
        print("   🔍 WELCOME TO PYSEARCH ENGINE   ")
        print("=" * 40)

        while True:
            # Translated the user prompt to English
            user_query = input("\nEnter your search query (or type 'exit' to quit): ")

            if user_query.lower() == "exit":
                print("PySearch is closing. Goodbye!")
                break

            results = engine.search(user_query)

            if not results:
                print("No results found. Please try searching for something else.")
            else:
                print(f"\nTop {len(results)} Results for '{user_query}':")
                for i, res in enumerate(results, 1):
                    # Ab dictionary se data print kar rahe hain
                    print(f"{i}. {res['url']} (Relevance Score: {res['score']:.4f})")
                    print(f"   Snippet: {res['snippet']}")
