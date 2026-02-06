
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Check if model is cached to avoid reloading
@st.cache_resource
def load_embedding_model():
    # Multilingual model for Zero-Shot Hindi Analysis
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

class VectorKnowledgeBase:
    def __init__(self):
        self.model = load_embedding_model()
        self.documents = []
        self.vectors = None
        self.metadata = []
        
        # Initialize with some Gold Standard / Bad Clauses for RAG
        self._initialize_knowledge_base()
        
        # Risk Anchors for Zero-Shot Analysis
        self.risk_anchors = {
            "Unilateral Termination": "One party can terminate the agreement at any time without cause or notice.",
            "Unlimited Indemnity": "The vendor shall indemnify the client for all losses without any limit or cap.",
            "Foreign Jurisdiction": "Any dispute shall be subject to the exclusive jurisdiction of courts in London, UK or Singapore.",
            "Unreasonable Payment Terms": "Payment shall be made within 90 days or more from the date of invoice."
        }
        self.risk_vectors = self.model.encode(list(self.risk_anchors.values()))
    
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
        self.vectors = self.model.encode(self.documents)

    def search(self, query, top_k=3):
        """
        Semantic search for the most similar knowledge base entries.
        """
        query_vector = self.model.encode([query])
        similarities = cosine_similarity(query_vector, self.vectors)[0]
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            results.append({
                "text": self.documents[idx],
                "score": float(similarities[idx]),
                "metadata": self.metadata[idx]
            })
            
        return results

    def analyze_multilingual_risk(self, clause_text, threshold=0.55):
        """
        Zero-Shot checks if a (Hindi/English) clause matches known High Risk concepts.
        """
        clause_vector = self.model.encode([clause_text])
        similarities = cosine_similarity(clause_vector, self.risk_vectors)[0]
        
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score > threshold:
            risk_type = list(self.risk_anchors.keys())[best_idx]
            return {
                "risk": "High",
                "type": risk_type,
                "score": float(best_score),
                "reason": f"Semantic match to high-risk concept: '{risk_type}' (Confidence: {best_score:.2f})"
            }
        return {"risk": "Low", "type": "Safe", "score": float(best_score), "reason": "No high-risk concepts detected."}

    def get_embedding(self, text):
        return self.model.encode([text])[0]

@st.cache_resource
def get_vector_kb():
    return VectorKnowledgeBase()
