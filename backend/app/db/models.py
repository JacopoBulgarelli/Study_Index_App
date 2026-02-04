from sqlalchemy import Column, String, Integer, ForeignKey, Text, Vector
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector  # If using PostgreSQL + pgvector

class Section(Base):
    __tablename__ = "sections"
    
    id = Column(String, primary_key=True)
    doc_id = Column(String, ForeignKey("documents.id"))
    parent_id = Column(String, ForeignKey("sections.id"), nullable=True)
    title = Column(String, nullable=False)
    level = Column(Integer)  # 1 = Chapter, 2 = Section, 3 = Subsection, etc.
    page_start = Column(Integer)
    page_end = Column(Integer)
    content_summary = Column(Text)  # Preview from PageIndex range
    node_type = Column(String)  # 'chapter', 'section', 'subsection', etc.
    
    # Relationships
    parent = relationship("Section", remote_side=[id], backref="children")
    chunks = relationship("ContentChunk", back_populates="section", cascade="all, delete")
    document = relationship("Document", back_populates="sections")

class ContentChunk(Base):
    __tablename__ = "content_chunks"
    
    id = Column(String, primary_key=True)
    section_id = Column(String, ForeignKey("sections.id"))
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))  # Adjust dimension based on your model (OpenAI=1536)
    chunk_index = Column(Integer)  # Order within section
    char_start = Column(Integer)
    char_end = Column(Integer)
    
    section = relationship("Section", back_populates="chunks")