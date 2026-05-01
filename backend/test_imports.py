import os
import sys
import time

print("Testing imports...")
start = time.time()

print("Importing FastAPI...")
try:
    import fastapi
    print(f"FastAPI imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"FastAPI import failed: {e}")

print("Importing Torch...")
try:
    import torch
    print(f"Torch imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Torch import failed: {e}")

print("Importing Transformers...")
try:
    import transformers
    print(f"Transformers imported in {time.time() - start:.2f}s")
except Exception as e:
    print(f"Transformers import failed: {e}")

print("Importing NLTK...")
try:
    import nltk
    print(f"NLTK imported in {time.time() - start:.2f}s")
    nltk.download('vader_lexicon', quiet=True)
    print(f"NLTK download finished in {time.time() - start:.2f}s")
except Exception as e:
    print(f"NLTK import/download failed: {e}")

print("Importing app.main...")
from app.main import app
print(f"App imported in {time.time() - start:.2f}s")
