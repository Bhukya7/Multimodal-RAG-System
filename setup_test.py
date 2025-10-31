print("🧪 SIMPLE TEST SCRIPT")
print("Testing basic functionality...")

# Test basic Python
print("✅ Python is working")

# Test imports
try:
    import chromadb
    print("✅ chromadb imported")
except ImportError as e:
    print(f"❌ chromadb failed: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence_transformers imported")
except ImportError as e:
    print(f"❌ sentence_transformers failed: {e}")

try:
    import fitz  # PyMuPDF
    print("✅ PyMuPDF imported")
except ImportError as e:
    print(f"❌ PyMuPDF failed: {e}")

try:
    import pytesseract
    print("✅ pytesseract imported")
except ImportError as e:
    print(f"❌ pytesseract failed: {e}")

print("🎯 Test completed!")