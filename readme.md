# 🔍 PySearch - Custom AI-Powered Search Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Vanilla JS](https://img.shields.io/badge/Frontend-Vanilla_JS-yellow.svg)
![Algorithms](https://img.shields.io/badge/Course-Algorithms-orange.svg)

PySearch is a full-stack, end-to-end custom search engine built entirely from scratch. It was developed to demonstrate the practical implementation of core Data Structures and Algorithms, including **Hash Maps (O(1) lookups)**, **TF-IDF Ranking**, and **Text Parsing/Tokenization**.

It features a custom web crawler, an inverted indexer, a mathematical ranking engine, a FastAPI backend, and a Google-like paginated frontend UI.

---

## ✨ Key Features
- **🌐 Custom Web Crawler:** Fetches HTML content from raw URLs and extracts clean text.
- **🧠 NLP Tokenizer:** Cleans text, removes stopwords, and applies Stemming using NLTK.
- **⚡ O(1) Inverted Index:** Maps words to documents using Hash Maps for ultra-fast $O(1)$ search lookups.
- **📊 TF-IDF Ranking Engine:** Mathematically scores and ranks documents based on relevance (Term Frequency-Inverse Document Frequency) instead of just word counting.
- **📝 Contextual Snippets:** Dynamically generates text snippets and highlights the searched keywords using Regular Expressions (Regex).
- **📄 Pagination:** Slices data mathematically to support Google-like Next/Previous page navigation.
- **🔌 REST API:** Serves data to the frontend using FastAPI.
- **💻 Google-like UI:** A clean, responsive frontend built with HTML, CSS, and Vanilla JavaScript.

---

## 🏗️ Architecture & Core Algorithms

This project implements Several core algorithms taught in Computer Science:

1. **Crawler (`crawler.py`):** Uses Regex to parse HTML and strip out unwanted scripts/tags.
2. **Tokenizer (`Tokenization.py`):** $O(N)$ string processing pipeline to normalize user input and document data.
3. **Indexer (`indexer.py`):** Builds an **Inverted Index (Hash Map)**. This turns a slow $O(N)$ linear search across all documents into a constant time $O(1)$ lookup.
4. **Search & Rank (`search.py`):** Implements the **TF-IDF formula** and uses Python's `Timsort` ($O(N \log N)$) to sort documents by their relevance scores.

---

## 📂 Project Structure

```text
PySearch/
│
├── data/                       # Contains all generated data (ignored in git)
│   ├── raw.jsonl               # Output of the Crawler
│   ├── inverted_index.json     # The Hash Map (Core Index)
│   └── docs_store.json         # Text snippets for the frontend
│
├── src/                        # Source Code
│   ├── crawler.py              # Web scraping logic
│   ├── Tokenization.py         # Text cleaning and stemming
│   ├── indexer.py              # Inverted Index builder
│   ├── search.py               # TF-IDF Ranking and Search Logic
│   └── api.py                  # FastAPI Backend Server
│
├── index.html                  # Frontend Web UI
├── requirements.txt            # Python dependencies
└── README.md                   # Project Documentation
🚀 How to Run the Project locally
Follow these step-by-step instructions to run the search engine on your local machine.

Step 1: Install Dependencies
Open your terminal and install the required Python libraries:

Bash
pip install fastapi uvicorn nltk requests
(Note: You may need to download NLTK data. If prompted, run import nltk; nltk.download('punkt'); nltk.download('stopwords') in your python shell).

Step 2: Generate the Data (Backend Pipeline)
Run the pipeline scripts in order to crawl data and build the index:

Run the Crawler: (Fetches websites and creates raw.jsonl)

Bash
python src/crawler.py
Run the Indexer: (Builds the Hash Map and Document Store)

Bash
python src/indexer.py
Step 3: Start the Backend Server (FastAPI)
Navigate to the src folder and start the API server using Uvicorn:

Bash
cd src
uvicorn api:app --reload
The API will now be running at http://127.0.0.1:8000.

Step 4: Launch the Frontend UI
Simply open the index.html file in your favorite web browser (Chrome, Edge, Firefox).

Alternatively, if you are using VS Code, you can use the Live Server extension to open it.

Type a query (e.g., "Python", "Apple", "Machine") and hit Enter!