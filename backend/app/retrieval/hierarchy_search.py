# backend/app/retrieval/hierarchy_search.py
from sqlalchemy import text
from typing import List, Tuple

class HybridRetriever:
    def __init__(self, db_session):
        self.db = db_session
    
    async def retrieve(self, query: str, doc_id: str, k: int = 5) -> List[Dict]:
        """
        2-stage retrieval:
        1. Semantic search on chunks (find relevant content)
        2. Enrich with structural context (parent/children from PageIndex tree)
        """
        query_embedding = await self.llm.embed(query)
        
        # Stage 1: Vector similarity search (PostgreSQL pgvector example)
        sql = text("""
            SELECT cc.id, cc.content, cc.section_id, 
                   1 - (cc.embedding <=> :embedding) as similarity
            FROM content_chunks cc
            JOIN sections s ON cc.section_id = s.id
            WHERE s.doc_id = :doc_id
            ORDER BY cc.embedding <=> :embedding
            LIMIT :limit
        """)
        
        results = self.db.execute(sql, {
            "embedding": str(query_embedding),  # pgvector format
            "doc_id": doc_id,
            "limit": k * 2  # Get more candidates for re-ranking
        }).fetchall()
        
        # Stage 2: Enrich with hierarchy context from PageIndex structure
        enriched_results = []
        for row in results:
            chunk = self.db.query(ContentChunk).get(row.id)
            section = chunk.section
            
            # Get breadcrumb path using parent relationships
            path = await self._get_breadcrumb(section)
            
            # Get sibling chunks for context (previous/next paragraphs)
            context_chunks = self.db.query(ContentChunk).filter(
                ContentChunk.section_id == section.id,
                ContentChunk.chunk_index.between(
                    chunk.chunk_index - 1, 
                    chunk.chunk_index + 1
                )
            ).all()
            
            enriched_results.append({
                "content": chunk.content,
                "similarity": row.similarity,
                "section": {
                    "title": section.title,
                    "path": path,  # ["Chapter 1", "Section 1.2", "Subsection 1.2.3"]
                    "pages": f"{section.page_start}-{section.page_end}"
                },
                "context": [c.content for c in context_chunks if c.id != chunk.id]
            })
        
        return enriched_results
    
    async def _get_breadcrumb(self, section: Section) -> List[str]:
        """Build path from root to current section using PageIndex hierarchy"""
        path = []
        current = section
        while current:
            path.insert(0, current.title)
            current = current.parent
        return path