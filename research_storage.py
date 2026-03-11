import os
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from qdrant_client import QdrantClient

class LegalKnowledgeBase:
    def __init__(self, collection_name="legal_precedents"):
        self.collection_name = collection_name
        # Store data locally in a folder called 'qdrant_storage'
        self.client = QdrantClient(path="qdrant_storage")
        self.embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    def upload_documents(self, texts: list, metadatas: list = None):
        """Turn legal text into vectors and store them."""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        print(f"✅ Successfully uploaded {len(texts)} chunks to the knowledge base.")

    def search(self, query: str, limit: int = 3):
        """Search for the most relevant legal clauses."""
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embeddings
        )
        results = vector_store.similarity_search(query, k=limit)
        return results

# Test it out
if __name__ == "__main__":
    kb = LegalKnowledgeBase()
    
    # Example "Gold Standard" clauses
    kb.upload_documents([
        "Liability is limited to 1x the annual contract value.",
        "Governing law shall be the laws of India, specifically courts in Mumbai.",
        "Termination requires a 30-day written notice from either party."
    ])

    # Try searching
    query = "What is the policy on ending the contract?"
    found = kb.search(query)
    print(f"\n🔍 Search Result for '{query}':\n", found[0].page_content)