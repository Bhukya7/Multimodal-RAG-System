"""
PDF Processing with mixed content handling
"""

import fitz  # PyMuPDF
import os
import uuid
from typing import List, Dict, Any
from pathlib import Path
from src.utils.image_processor import ImageProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class PDFProcessor:
    def __init__(self, config):
        self.config = config
        self.image_processor = ImageProcessor(config)
    
    def process_pdf(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process PDF files with mixed content"""
        documents = []
        
        try:
            doc = fitz.open(file_path)
            logger.info(f"Processing PDF: {filename} with {len(doc)} pages")
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Extract text
                text = page.get_text().strip()
                if text:
                    # Process text content with chunking
                    text_chunks = self._chunk_text(text)
                    for i, chunk in enumerate(text_chunks):
                        documents.append({
                            "id": f"{filename}_page{page_num+1}_text{i}_{str(uuid.uuid4())[:8]}",
                            "content": chunk,
                            "metadata": {
                                "filename": filename,
                                "file_type": "pdf_text",
                                "page_number": page_num + 1,
                                "chunk_index": i,
                                "content_type": "text",
                                "source": "pdf"
                            }
                        })
                
                # Extract and process images
                image_list = page.get_images()
                if image_list:
                    logger.info(f"Found {len(image_list)} images on page {page_num + 1}")
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Extract image
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)
                        
                        if pix.n - pix.alpha < 4:  # RGB or Grayscale
                            img_data = pix.tobytes("png")
                            
                            # Process image with OCR
                            image_text = self.image_processor.extract_text_from_image_bytes(img_data)
                            
                            if image_text.strip():
                                documents.append({
                                    "id": f"{filename}_page{page_num+1}_img{img_index}_{str(uuid.uuid4())[:8]}",
                                    "content": f"Image content: {image_text}",
                                    "metadata": {
                                        "filename": filename,
                                        "file_type": "pdf_image",
                                        "page_number": page_num + 1,
                                        "image_index": img_index,
                                        "content_type": "image_ocr",
                                        "source": "pdf"
                                    }
                                })
                                logger.info(f"Extracted text from image on page {page_num + 1}")
                        
                        pix = None  # Free pixmap memory
                        
                    except Exception as e:
                        logger.warning(f"Error processing image on page {page_num + 1}: {e}")
                        continue
            
            doc.close()
            logger.info(f"PDF processing completed: {len(documents)} chunks created from {filename}")
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {e}")
        
        return documents
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        chunk_size = self.config.get("processing.chunk_size", 1000)
        overlap = self.config.get("processing.chunk_overlap", 200)
        
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            
            # Try to break at paragraph or sentence boundary
            if end < len(text):
                # Look for paragraph breaks first
                for break_pos in range(end, start + chunk_size // 2, -1):
                    if text[break_pos:break_pos+2] == '\n\n':
                        end = break_pos + 2
                        break
                    elif text[break_pos] in ['.', '!', '?'] and break_pos + 1 < len(text) and text[break_pos+1] in [' ', '\n']:
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