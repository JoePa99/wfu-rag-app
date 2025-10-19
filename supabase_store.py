import os
from typing import List, Dict, Tuple
import openai
from supabase import create_client, Client
import numpy as np
from datetime import datetime
import hashlib

class SupabaseVectorStore:
    """Handles vector storage and retrieval using Supabase with pgvector"""
    
    def __init__(self):
        """Initialize Supabase client and OpenAI for embeddings"""
        # Initialize Supabase
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_SERVICE_KEY')
        
        if not supabase_url or not supabase_key:
            raise ValueError(
                "Supabase credentials not found. Please set SUPABASE_URL and "
                "SUPABASE_SERVICE_KEY environment variables."
            )
        
        self.supabase: Client = create_client(supabase_url, supabase_key)
        
        # Initialize OpenAI for embeddings
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        
        openai.api_key = openai_key
        
        # Embedding model configuration
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dimension = 1536
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for text using OpenAI
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            response = openai.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error creating embedding: {str(e)}")
            return [0.0] * self.embedding_dimension
    
    def create_chunks(self, text: str, file_info: Dict) -> List[Dict]:
        """
        Split text into chunks with metadata
        
        Args:
            text: Text to chunk
            file_info: File metadata from Google Drive
            
        Returns:
            List of chunk dictionaries with metadata
        """
        # Simple chunking by characters with overlap
        chunks = []
        text = text.strip()
        
        if not text:
            return chunks
        
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk_text = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > self.chunk_size * 0.5:  # Only break if we're past halfway
                    chunk_text = chunk_text[:break_point + 1]
                    end = start + break_point + 1
            
            # Create chunk metadata
            chunk = {
                'content': chunk_text.strip(),
                'file_id': file_info['id'],
                'file_name': file_info['name'],
                'file_url': file_info.get('webViewLink', ''),
                'chunk_id': chunk_id,
                'mime_type': file_info.get('mimeType', ''),
                'modified_time': file_info.get('modifiedTime', ''),
            }
            
            chunks.append(chunk)
            chunk_id += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap if end < len(text) else end
        
        return chunks
    
    def add_documents(self, chunks: List[Dict]) -> None:
        """
        Add document chunks to Supabase with embeddings
        
        Args:
            chunks: List of chunk dictionaries
        """
        for chunk in chunks:
            try:
                # Create embedding
                embedding = self.create_embedding(chunk['content'])
                
                # Create unique ID for chunk
                chunk_hash = hashlib.md5(
                    f"{chunk['file_id']}_{chunk['chunk_id']}".encode()
                ).hexdigest()
                
                # Prepare data for insertion
                data = {
                    'id': chunk_hash,
                    'content': chunk['content'],
                    'embedding': embedding,
                    'file_id': chunk['file_id'],
                    'file_name': chunk['file_name'],
                    'file_url': chunk['file_url'],
                    'chunk_id': chunk['chunk_id'],
                    'mime_type': chunk['mime_type'],
                    'modified_time': chunk['modified_time'],
                    'created_at': datetime.utcnow().isoformat(),
                }
                
                # Upsert to Supabase (insert or update if exists)
                self.supabase.table('documents').upsert(data).execute()
                
            except Exception as e:
                print(f"Error adding chunk to Supabase: {str(e)}")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents using vector similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of matching documents with metadata
        """
        try:
            # Create query embedding
            query_embedding = self.create_embedding(query)
            
            # Call Supabase RPC function for vector similarity search
            # This requires setting up a custom function in Supabase
            results = self.supabase.rpc(
                'match_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.5,
                    'match_count': top_k
                }
            ).execute()
            
            return results.data if results.data else []
            
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []
    
    def clear_all_documents(self) -> None:
        """Clear all documents from the vector store"""
        try:
            self.supabase.table('documents').delete().neq('id', '').execute()
            print("All documents cleared from vector store")
        except Exception as e:
            print(f"Error clearing documents: {str(e)}")
