"""
Vector Store Management using ChromaDB
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorStore:
    def __init__(self, config):
        self.config = config
        self.client = chromadb.PersistentClient(
            path=config.get("vector_db.path", "./data/vector_db")
        )
        
        # Initialize embedding model
        model_name = config.get("embedding.model", "sentence-transformers/all-MiniLM-L6-v2")
        logger.info(f"Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name=config.get("vector_db.collection_name", "multimodal_docs"),
            metadata={"description": "Multimodal document embeddings"}
        )
        
        logger.info("Vector store initialized successfully")
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to vector store"""
        if not documents:
            logger.warning("No documents to add")
            return
        
        ids = [doc["id"] for doc in documents]
        contents = [doc["content"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        # Generate embeddings
        logger.info(f"Generating embeddings for {len(contents)} documents...")
        embeddings = self.embedding_model.encode(contents).tolist()
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Successfully added {len(documents)} documents to vector store")
    
    def search(self, query: str, top_k: int = 5, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query]).tolist()
        
        # Search in vector database
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        # Format results
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                # Convert distance to similarity score
                score = 1 - distance
                
                if score >= threshold:
                    search_results.append({
                        "content": doc,
                        "metadata": metadata,
                        "score": score,
                        "document_type": metadata.get("file_type", "unknown")
                    })
        
        logger.info(f"Search returned {len(search_results)} results for query: {query}")
        return search_results
    
    def get_collection_stats(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()