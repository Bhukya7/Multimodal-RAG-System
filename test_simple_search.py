"""
Simple search test with manual processing
"""

import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("🧪 SIMPLE SEARCH TEST")

try:
    from src.core.rag_system import MultimodalRAG
    
    rag = MultimodalRAG()
    
    print("📝 Adding test document...")
    test_content = """
    Artificial Intelligence is the simulation of human intelligence in machines.
    AI systems can perform tasks like learning, reasoning, and problem-solving.
    Machine learning is a subset of AI that focuses on algorithms that learn from data.
    """
    temp_file = Path("./data/input/test_ai.txt")
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("🔄 Processing test file...")
    result = rag.process_file(str(temp_file))
    print(f"✅ Processing result: {result}")
    
    import time
    time.sleep(1)
    
    queries = [
        "artificial intelligence",
        "machine learning", 
        "AI systems",
        "human intelligence"
    ]
    
    print("\n🔍 Testing searches...")
    for query in queries:
        print(f"  Query: '{query}'")
        results = rag.search(query, top_k=5, threshold=0.1)
        print(f"    Results: {len(results)}")
        if results:
            for r in results:
                print(f"      - {r['score']:.3f}: {r['metadata'].get('filename', 'Unknown')}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()