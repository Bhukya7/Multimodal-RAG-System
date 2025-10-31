#!/usr/bin/env python3
"""
Simple launcher for Multimodal RAG System Interactive Mode
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from src.main import main
    print("🚀 Starting Multimodal RAG System Interactive Mode...")
    main()
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")