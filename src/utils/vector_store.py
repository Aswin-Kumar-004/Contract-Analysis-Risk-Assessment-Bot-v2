

# from sentence_transformers import SentenceTransformer (Removed for Lite Mode)
# from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Lite Mode: No heavy embedding models
@st.cache_resource
def load_embedding_model():
    return None

class VectorKnowledgeBase:
    def __init__(self):
        # self.model = load_embedding_model()
        self.documents = []
        self.metadata = []
        
        # Initialize with static data only (no vectors)
        self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self):
        # Data: (Text, Type, Analysis)
        kb_data = [
            ("The Vendor shall indemnify the Client against all claims, unlimited in amount.", "Indemnity", "Risk: High. Unlimited liability can bankrupt a small vendor."),
            ("The Vendor's liability shall be capped at the total contract value.", "Indemnity", "Standard: Safe. Liability is limited to a reasonable amount."),
            ("This Agreement may be terminated by the Client at any time without notice.", "Termination", "Risk: High. Unilateral termination without notice creates business uncertainty."),
            ("Either party may terminate this Agreement with 30 days prior written notice.", "Termination", "Standard: Safe. Mutual termination with notice period."),
            ("Any dispute shall be subject to the exclusive jurisdiction of the courts in London, UK.", "Jurisdiction", "Risk: High. Foreign jurisdiction is expensive and impractical for Indian SMEs."),
            ("Disputes shall be resolved by arbitration in New Delhi under the Indian Arbitration Act.", "Jurisdiction", "Standard: Safe. Local arbitration is cost-effective."),
            ("The Client owns all Intelligent Property created by the Vendor during this engagement.", "IP", "Neutral. Standard for 'work for hire' but ensure you retain pre-existing IP."),
            ("Payment shall be made within 90 days of invoice receipt.", "Payment", "Risk: Medium. 90 days is a long cycle for SMEs; negotiate for 30-45 days.")
        ]
        
        self.documents = [item[0] for item in kb_data]
        self.metadata = [{"type": item[1], "analysis": item[2]} for item in kb_data]
        # self.vectors = self.model.encode(self.documents)

    def search(self, query, top_k=3):
        """
        Lite Mode: Keyword-based fallback search.
        """
        results = []
        query_words = set(query.lower().split())
        
        scores = []
        for i, doc in enumerate(self.documents):
            doc_words = set(doc.lower().split())
            vocab = query_words.union(doc_words)
            # Simple Jaccard similarity as fallback
            intersection = query_words.intersection(doc_words)
            score = len(intersection) / len(vocab) if vocab else 0
            scores.append((score, i))
            
        # Sort by score
        scores.sort(key=lambda x: x[0], reverse=True)
        top_indices = [idx for score, idx in scores[:top_k] if score > 0]
        
        for idx in top_indices:
            results.append({
                "text": self.documents[idx],
                "score": 0.5, # Dummy score
                "metadata": self.metadata[idx]
            })
            
        return results

    def analyze_multilingual_risk(self, clause_text, threshold=0.55):
        """
        Lite Mode: Returns neutral result as vector analysis is disabled.
        """
        return {"risk": "Low", "type": "Safe", "score": 0.0, "reason": "Vector analysis disabled in Lite Mode."}

    def get_embedding(self, text):
        return [0.0] * 384 # Dummy vector

@st.cache_resource
def get_vector_kb():
    return VectorKnowledgeBase()
