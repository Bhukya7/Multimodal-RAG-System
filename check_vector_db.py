#!/usr/bin/env python3
"""
Check vector database location and contents
"""

import os
from pathlib import Path

print("📁 CHECKING VECTOR DATABASE")

# Check default location
vector_db_path = Path("./data/vector_db")
print(f"Default vector DB path: {vector_db_path}")
print(f"Exists: {vector_db_path.exists()}")

if vector_db_path.exists():
    print("📄 Files in vector DB directory:")
    for file in vector_db_path.glob("*"):
        print(f"  - {file.name} ({file.stat().st_size} bytes)")

# Check if there are any ChromaDB files
chroma_files = list(vector_db_path.glob("*.sqlite3"))
if chroma_files:
    print(f"✅ Found ChromaDB database: {chroma_files[0].name}")
else:
    print("❌ No ChromaDB database file found")

# Check data directory
data_dir = Path("./data/input")
print(f"\n📁 Data input directory: {data_dir}")
print(f"Exists: {data_dir.exists()}")

if data_dir.exists():
    files = list(data_dir.glob("*"))
    print(f"Files in data directory: {len(files)}")
    for file in files:
        print(f"  - {file.name}")