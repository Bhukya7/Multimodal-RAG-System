#!/usr/bin/env python3
"""
Debug script for search issues
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("🔍 DEBUGGING SEARCH ISSUE")

try:
    from src.core.rag_system import MultimodalRAG
    from src.core.vector_store import VectorStore
    from src.utils.config import Config
    
    # Initialize system
    print("🔄 Initializing system...")
    rag = MultimodalRAG()
    
    # Check stats
    stats = rag.get_stats()
    print(f"📊 Vector store stats: {stats}")
    
    # Test search directly with lower threshold
    print("\n🧪 Testing search with threshold 0.1...")
    results = rag.search("artificial intelligence", top_k=10, threshold=0.1)
    print(f"🔍 Search results count: {len(results)}")
    
    if results:
        print("✅ SEARCH IS WORKING!")
        for i, r in enumerate(results, 1):
            print(f"  {i}. Score: {r['score']:.3f} - {r['metadata'].get('filename', 'Unknown')}")
            print(f"     {r['content'][:100]}...")
    else:
        print("❌ Still no results with threshold 0.1")
        
        # Let's check what's in the vector store directly
        print("\n🔧 Checking vector store directly...")
        config = Config()
        vector_store = VectorStore(config)
        
        # Get collection count
        collection = vector_store.collection
        count = collection.count()
        print(f"📁 Documents in collection: {count}")
        
        if count > 0:
            print("💡 Documents exist but search not returning results")
            print("   This might be an embedding similarity issue")
        else:
            print("💡 No documents in collection - processing might not be saving properly")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()