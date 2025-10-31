@echo off
echo Installing Multimodal RAG System Dependencies...
py -m pip install --upgrade pip
py -m pip install chromadb sentence-transformers pymupdf pytesseract pydantic rich tqdm aiofiles python-dotenv pyyaml numpy pillow
echo.
echo Installation completed!
pause