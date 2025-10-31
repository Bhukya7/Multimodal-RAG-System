"""
Image Processing with OCR
"""

import pytesseract
from PIL import Image
import io
import uuid
from typing import List, Dict, Any
from pathlib import Path
from src.utils.logger import setup_logger

# Configure tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logger = setup_logger(__name__)

class ImageProcessor:
    def __init__(self, config):
        self.config = config
    
    def process_image(self, file_path: str, filename: str) -> List[Dict[str, Any]]:
        """Process image files using OCR"""
        try:
            extracted_text = self.extract_text_from_image(file_path)
            
            if not extracted_text.strip():
                logger.warning(f"No text extracted from image: {filename}")
                return []
            
            documents = [{
                "id": f"{filename}_{str(uuid.uuid4())[:8]}",
                "content": extracted_text,
                "metadata": {
                    "filename": filename,
                    "file_type": "image",
                    "content_type": "ocr_text",
                    "source": "image_file"
                }
            }]
            
            logger.info(f"Processed image {filename}, extracted {len(extracted_text)} characters")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing image {filename}: {e}")
            return []
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image file using OCR"""
        try:
            image = Image.open(image_path)
            
            # Preprocess image for better OCR
            # Convert to grayscale if needed
            if image.mode != 'L':
                image = image.convert('L')
            
            # Use pytesseract to extract text
            text = pytesseract.image_to_string(image)
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image {image_path}: {e}")
            return ""
    
    def extract_text_from_image_bytes(self, image_data: bytes) -> str:
        """Extract text from image bytes using OCR"""
        try:
            image = Image.open(io.BytesIO(image_data))
            
            # Preprocess image for better OCR
            if image.mode != 'L':
                image = image.convert('L')
            
            text = pytesseract.image_to_string(image)
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image bytes: {e}")
            return ""