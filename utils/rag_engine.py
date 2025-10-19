import os
from typing import List, Dict, Tuple
import anthropic

class RAGEngine:
    """RAG engine using Claude for response generation"""
    
    def __init__(self, vector_store):
        """
        Initialize RAG engine
        
        Args:
            vector_store: SupabaseVectorStore instance
        """
        self.vector_store = vector_store
        
        # Initialize Claude client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable.")
        
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Claude Sonnet model
        self.max_tokens = 4096
    
    def query(self, question: str, top_k: int = 5) -> Tuple[str, List[Dict]]:
        """
        Query the RAG system
        
        Args:
            question: User's question
            top_k: Number of relevant documents to retrieve
            
        Returns:
            Tuple of (response text, list of source documents)
        """
        # Retrieve relevant documents
        relevant_docs = self.vector_store.search(question, top_k=top_k)
        
        if not relevant_docs:
            return (
                "I couldn't find any relevant documents to answer your question. "
                "Please try rephrasing your question or check if documents have been indexed.",
                []
            )
        
        # Build context from retrieved documents
        context = self._build_context(relevant_docs)
        
        # Generate response using Claude
        response = self._generate_response(question, context)
        
        # Format sources for display
        sources = self._format_sources(relevant_docs)
        
        return response, sources
    
    def _build_context(self, documents: List[Dict]) -> str:
        """
        Build context string from retrieved documents
        
        Args:
            documents: List of retrieved document chunks
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"[Document {i}: {doc['file_name']}]\n{doc['content']}\n"
            )
        
        return "\n".join(context_parts)
    
    def _generate_response(self, question: str, context: str) -> str:
        """
        Generate response using Claude
        
        Args:
            question: User's question
            context: Retrieved context
            
        Returns:
            Generated response
        """
        # Construct prompt
        system_prompt = """You are an intelligent document assistant for Wake Forest University. 
Your role is to help users find information from their documents accurately and helpfully.

Guidelines:
- Answer questions based ONLY on the provided document context
- If the answer isn't in the documents, clearly state that
- Cite specific documents when providing information
- Be concise but thorough
- Use a professional, academic tone appropriate for a university setting
- If the documents contain conflicting information, acknowledge this
- Always prioritize accuracy over speculation"""

        user_prompt = f"""Based on the following documents, please answer the question.

Documents:
{context}

Question: {question}

Please provide a clear, accurate answer based on the documents above. If the documents don't contain 
enough information to answer the question, please say so."""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Extract response text
            response_text = message.content[0].text
            return response_text
            
        except Exception as e:
            print(f"Error generating response with Claude: {str(e)}")
            return "I encountered an error generating a response. Please try again."
    
    def _format_sources(self, documents: List[Dict]) -> List[Dict]:
        """
        Format source documents for display
        
        Args:
            documents: List of retrieved document chunks
            
        Returns:
            List of formatted source dictionaries
        """
        sources = []
        seen_files = set()
        
        for doc in documents:
            file_id = doc['file_id']
            
            # Avoid duplicate file references
            if file_id not in seen_files:
                seen_files.add(file_id)
                
                # Get a snippet of the content
                content = doc['content']
                snippet = content[:200] + "..." if len(content) > 200 else content
                
                sources.append({
                    'title': doc['file_name'],
                    'url': doc.get('file_url', ''),
                    'snippet': snippet,
                    'type': doc.get('mime_type', 'unknown')
                })
        
        return sources
