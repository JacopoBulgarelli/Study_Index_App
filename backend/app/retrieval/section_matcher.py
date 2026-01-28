from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SectionMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.section_vectors = None
        self.sections = []
    
    def add_sections(self, sections: List[Dict]):
        """Add sections for matching"""
        self.sections = sections
        texts = [s['content'] for s in sections]
        self.section_vectors = self.vectorizer.fit_transform(texts)
    
    def find_best_match(self, query: str, top_k: int = 3) -> List[Tuple[int, float]]:
        """Find best matching sections for a query"""
        if not self.sections:
            return []
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.section_vectors).flatten()
        
        # Get top k matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        results = [(self.sections[i]['section_id'], similarities[i]) 
                  for i in top_indices if similarities[i] > 0.1]
        
        return results