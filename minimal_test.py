print("🧪 MINIMAL RAG TEST")

# Test basic imports
try:
    from src.utils.config import Config
    config = Config()
    print("✅ Config - SUCCESS")
except Exception as e:
    print(f"❌ Config - FAILED: {e}")

try:
    from src.utils.image_processor import ImageProcessor
    print("✅ ImageProcessor - SUCCESS")
except Exception as e:
    print(f"❌ ImageProcessor - FAILED: {e}")

try:
    from src.core.rag_system import MultimodalRAG
    print("✅ MultimodalRAG - SUCCESS")
    
    # Test creating instance
    rag = MultimodalRAG()
    print("✅ RAG System Creation - SUCCESS")
except Exception as e:
    print(f"❌ MultimodalRAG - FAILED: {e}")

print("🎯 Minimal test completed!")