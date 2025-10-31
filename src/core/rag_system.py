"""
Main RAG System Orchestrator
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import glob

from src.core.document_processor import DocumentProcessor
from src.core.vector_store import VectorStore
from src.core.retrieval_engine import RetrievalEngine
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class MultimodalRAG:
    """Main Multimodal RAG System"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = Config(config_path)
        self.document_processor = DocumentProcessor(self.config)
        self.vector_store = VectorStore(self.config)
        self.retrieval_engine = RetrievalEngine(self.vector_store, self.config)
        
        logger.info("Multimodal RAG system initialized")
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file"""
        try:
            logger.info(f"Processing file: {file_path}")
            
            # Process document
            documents = self.document_processor.process_document(file_path)
            
            # Add to vector store
            if documents:
                self.vector_store.add_documents(documents)
                logger.info(f"Added {len(documents)} chunks from {file_path}")
                
                return {
                    "success": True,
                    "file_path": file_path,
                    "chunks_created": len(documents),
                    "file_type": self._get_file_type(file_path)
                }
            else:
                return {
                    "success": False,
                    "file_path": file_path,
                    "error": "No content extracted"
                }
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {
                "success": False,
                "file_path": file_path,
                "error": str(e)
            }
    
    def process_folder(self, folder_path: str) -> Dict[str, Any]:
        """Process all supported files in a folder"""
        results = {
            "text": {"files_processed": 0, "chunks_created": 0},
            "image": {"files_processed": 0, "chunks_created": 0},
            "pdf": {"files_processed": 0, "chunks_created": 0},
            "total_files": 0,
            "total_chunks": 0
        }
        
        # Find all supported files
        supported_extensions = self.config.get("processing.supported_extensions", [".txt", ".pdf", ".png", ".jpg", ".jpeg"])
        
        for ext in supported_extensions:
            pattern = os.path.join(folder_path, f"**/*{ext}")
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                result = self.process_file(file_path)
                
                if result["success"]:
                    file_type = result["file_type"]
                    if file_type in results:
                        results[file_type]["files_processed"] += 1
                        results[file_type]["chunks_created"] += result["chunks_created"]
                    results["total_files"] += 1
                    results["total_chunks"] += result["chunks_created"]
        
        return results
    
    def search(self, query: str, top_k: int = None, threshold: float = None) -> List[Dict[str, Any]]:
        """Search for relevant documents"""
        return self.retrieval_engine.search(query, top_k, threshold)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        stats = self.vector_store.get_collection_stats()
        
        return {
            "total_documents": stats,
            "document_types": ["text", "image", "pdf"],
            "collection_name": self.config.get("vector_db.collection_name"),
            "embedding_model": self.config.get("embedding.model")
        }
    
    def _get_file_type(self, file_path: str) -> str:
        """Determine file type from extension"""
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            return 'pdf'
        elif ext in ['.png', '.jpg', '.jpeg']:
            return 'image'
        elif ext == '.txt':
            return 'text'
        else:
            return 'unknown'