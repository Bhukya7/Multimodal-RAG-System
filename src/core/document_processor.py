"""
Document Processor for handling multiple file types
"""

import os
import uuid
from typing import List, Dict, Any
from pathlib import Path

from src.core.pdf_processor import PDFProcessor
from src.utils.image_processor import ImageProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class DocumentProcessor:
    def __init__(self, config):
        self.config = config
        self.pdf_processor = PDFProcessor(config)
        self.image_processor = ImageProcessor(config)
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Process document based on file type"""
        file_ext = Path(file_path).suffix.lower()
        filename = Path(file_path).name
        
        logger.info(f"Processing document: {filename} (type: {file_ext})")
        
        if file_ext == '.pdf':
            return self.pdf_processor.process_pdf(file_path, filename)
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            return self.image_processor.process_image(file_path, filename)
        elif file_ext == '.txt':
            return self.process_text_file(file_path, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    
    def process_text_file(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process plain text files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                logger.warning(f"Empty text file: {filename}")
                return []
            
            # Simple chunking strategy
            chunks = self._chunk_text(
                content, 
                chunk_size=self.config.get("processing.chunk_size", 1000),
                overlap=self.config.get("processing.chunk_overlap", 200)
            )
            
            documents = []
            for i, chunk in enumerate(chunks):
                documents.append({
                    "id": f"{filename}_{i}_{str(uuid.uuid4())[:8]}",
                    "content": chunk,
                    "metadata": {
                        "filename": filename,
                        "file_type": "text",
                        "chunk_index": i,
                        "total_chunks": len(chunks),
                        "source": "text_file"
                    }
                })
            
            logger.info(f"Created {len(documents)} chunks from text file: {filename}")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing text file {filename}: {e}")
            return []
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                for break_pos in range(end, start + chunk_size // 2, -1):
                    if text[break_pos] in ['.', '!', '?', '\n']:
                        end = break_pos + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            if end == len(text):
                break
                
            start = end - overlap
            if start < 0:
                start = 0
        
        return chunks