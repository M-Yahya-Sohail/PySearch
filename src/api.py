"""
Web API for PySearch
--------------------
This script creates a web server using FastAPI. It acts as a bridge 
between our backend search engine and any future frontend (like a React web page).
"""

import math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import PySearchEngine

# ==========================================
# 📂 PATH SETUP
# ==========================================
INDEX_FILE = r"C:\Users\user\Documents\GitHub\PySearch\data\inverted_index.json"
DOCS_STORE_FILE = r"C:\Users\user\Documents\GitHub\PySearch\data\docs_store.json"

# Initialize FastAPI app
app = FastAPI(title="PySearch API")

# ==========================================
# 🌐 CORS SETUP (To allow frontend connections)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the search engine into memory
print("Starting PySearch API...")
# 👈 Ab engine ko dono files de rahe hain (Index aur Snippets dono)
engine = PySearchEngine(INDEX_FILE, DOCS_STORE_FILE) 

@app.get("/")
def read_root():
    return {"message": "Welcome to PySearch API! The engine is online."}

@app.get("/search")
def search_query(q: str, page: int = 1, limit: int = 10):
    results, total_matches = engine.search(q, page=page, page_size=limit)
    
    # Calculate total pages
    total_pages = math.ceil(total_matches / limit) if total_matches > 0 else 0
    
    return {
        "query": q,
        "total_results": total_matches,
        "current_page": page,
        "total_pages": total_pages,
        "results": results
    }