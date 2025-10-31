"""
Retrieval Engine for handling different query types
"""

from typing import List, Dict, Any, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class RetrievalEngine:
    """Handles different query types and retrieval strategies"""
    
    def __init__(self, vector_store, config):
        self.vector_store = vector_store
        self.config = config
    
    def search(self, query: str, top_k: Optional[int] = None, threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """Main search method with query analysis"""
        if top_k is None:
            top_k = self.config.get("retrieval.default_top_k", 5)
        if threshold is None:
            threshold = self.config.get("retrieval.similarity_threshold", 0.5)
        
        # Analyze query type
        query_type = self._analyze_query_type(query)
        logger.info(f"Query type: {query_type} - '{query}'")
        
        # Perform search
        results = self.vector_store.search(query, top_k, threshold)
        
        # Apply query-type specific filtering if needed
        if query_type == "factual":
            results = self._filter_factual_results(results)
        elif query_type == "exploratory":
            results = self._boost_exploratory_results(results)
        elif query_type == "cross_modal":
            results = self._boost_cross_modal_results(results)
        
        return results
    
    def _analyze_query_type(self, query: str) -> str:
        """Analyze query to determine type"""
        query_lower = query.lower()
        
        # Factual queries (specific questions)
        factual_indicators = ["what is", "who is", "when did", "where is", "how many", "how much", "which"]
        if any(indicator in query_lower for indicator in factual_indicators):
            return "factual"
        
        # Exploratory queries (vague, broad)
        exploratory_indicators = ["find", "show me", "tell me about", "explain", "summary", "information about"]
        if any(indicator in query_lower for indicator in exploratory_indicators):
            return "exploratory"
        
        # Cross-modal queries (mentioning visual elements)
        cross_modal_indicators = ["chart", "graph", "image", "picture", "diagram", "photo", "visual", "figure"]
        if any(indicator in query_lower for indicator in cross_modal_indicators):
            return "cross_modal"
        
        return "general"
    
    def _filter_factual_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter results for factual queries - prefer text content"""
        # Boost text documents for factual queries
        text_results = [r for r in results if r.get('document_type') in ['text', 'pdf_text']]
        other_results = [r for r in results if r not in text_results]
        
        return text_results + other_results
    
    def _boost_exploratory_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Boost diverse content types for exploratory queries"""
        # For exploratory queries, maintain diversity
        return results
    
    def _boost_cross_modal_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Boost image-related content for cross-modal queries"""
        # Boost image-related content
        image_results = [r for r in results if r.get('document_type') in ['image', 'pdf_image']]
        other_results = [r for r in results if r not in image_results]
        
        return image_results + other_results