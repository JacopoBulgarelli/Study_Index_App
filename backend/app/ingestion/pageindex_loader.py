from pageindex import PageIndexClient
import pageindex.utils as utils
from typing import List, Dict, Any, Optional
import pdfplumber  # Better for structured text than PyPDF2
from app.db.models import Section, Document, ContentChunk
from app.llm.client import LLMClient  # Your embedding client
from sqlalchemy.orm import Session
import uuid
from app.core.config import PAGEINDEX_API_KEY

# Get your PageIndex API key from https://dash.pageindex.ai/api-keys
pi_client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

class PageIndexLoader:
    def __init__(self, db_session: Session,llm_client: LLMClient):
        self.llm_client = llm_client
        self.db_session = db_session
        self.pi_client = pi_client

    async def ingest_document(self, file_path: str, doc_name:str) -> Document:
        """
        Pipeline:
        PageIndex (structure) → PDF Extraction (content) → Embeddings (retrieval)
        """
        # Step 1: Use PageIndex to get structured data
        print('Extracting document structure with PageIndex...')
        structure = self.pi_client.index_document(file_path)

        #Step 2: Create document record
        doc = Document(name = doc_name, file_path=file_path, total_pages=structure.total_pages)
        self.db.add(doc)
        self.db.flush()  # To get doc.id

        # Step 3: Extract text content for each section based on PageIndex page ranges
        section_maps = {} #pageindex section id -> Section

        with pdfplumber.open(file_path) as pdf:
            for node in structure.nodes:
                if node.type in structure.nodes: # Flattened tree from PageIndex
                    section = await self.process_node(node, doc.id, pdf, section_maps)
                    section_maps[node.id] = section
        self.db.commit() # Permanently saves all database changes (the doc record + all processed sections)
        return doc
    
    async def process_node(self, node: Dict, doc_id: int, pdf, section_map: Dict) -> Section:
        """
        Process a single node from PageIndex output
        node structure: {
            'id': 'uuid',
            'level': 1, 
            'title': 'Chapter 1', 
            'page_range': [0, 15],  # 0-indexed
            'parent_id': None,
            'type': 'chapter'
        }
        """
        #Extract text from specified page range
        start_page, end_page = node['page_range']
        text_content = ""

        for page_num in range(start_page, min(end_page + 1, len(pdf))):
            page = pdf.pages[page_num]
            text_content += page.extract_text() + "\n"
        
        # Create Section (structural unit)
        parent_section = sections_map.get(node.get('parent_id')) if node.get('parent_id') else None
        
        section = Section(
            id=str(uuid.uuid4()),
            doc_id=doc_id,
            title=node['title'],
            level=node['level'],
            page_start=start_page,
            page_end=end_page,
            parent_id=parent_section.id if parent_section else None,
            content_summary=text_content[:1000] + "...",  # First 1000 chars as preview
            node_type=node.get('type', 'section')
        )
        
        self.db.add(section)
        self.db.flush()
        
        # Step 4: Chunk and embed for retrieval (only for leaf nodes or all nodes?)
        await self._create_embeddings(section, text_content)
        
        return section
    
    async def _create_embeddings(self, section: Section, full_text: str):
        """
        Strategy: Break section into chunks, embed separately, but keep section_id reference
        This allows retrieval of specific chunks with section context
        """
        # Simple chunking strategy (can be smarter with overlap)
        chunk_size = 1000
        overlap = 200
        chunks = []
        
        for i in range(0, len(full_text), chunk_size - overlap):
            chunk_text = full_text[i:i + chunk_size]
            if len(chunk_text) < 100:  # Skip tiny chunks
                continue
                
            embedding = await self.llm.embed(chunk_text)
            
            content_chunk = ContentChunk(
                id=str(uuid.uuid4()),
                section_id=section.id,
                content=chunk_text,
                embedding=embedding,
                chunk_index=i // (chunk_size - overlap),
                char_start=i,
                char_end=i + len(chunk_text)
            )
            chunks.append(content_chunk)
        
        # Bulk insert for performance
        self.db.bulk_save_objects(chunks)