from src.config import CLAUSE_TYPES

def classify_clause(text):
    """
    Classifies a clause based on content keywords.
    Enhanced with more comprehensive keyword matching.
    """
    text_lower = text.lower()
    
    # Termination
    if any(kw in text_lower for kw in ["terminate", "termination", "cancel", "cancellation", "end this agreement"]):
        return "Termination"
    
    # Indemnity
    if any(kw in text_lower for kw in ["indemn", "hold harmless", "hold the", "defend and protect"]):
        return "Indemnity"
    
    # Limitation of Liability
    if any(kw in text_lower for kw in ["limitation of liability", "liability cap", "total liability", "shall not exceed", "maximum liability"]):
        return "Limitation of Liability"
    
    # Intellectual Property
    if any(kw in text_lower for kw in ["intellectual property", "ip rights", "copyright", "trademark", "patent", "proprietary rights", "work product"]):
        return "Intellectual Property"
    
    # Payment
    if any(kw in text_lower for kw in ["payment", "pay", "fee", "invoice", "compensation", "remuneration", "consideration"]):
        return "Payment"
    
    # Confidentiality
    if any(kw in text_lower for kw in ["confidential", "proprietary information", "non-disclosure", "trade secret"]):
        return "Confidentiality"
    
    # Governing Law / Jurisdiction
    if any(kw in text_lower for kw in ["governing law", "jurisdiction", "courts", "arbitration", "dispute resolution"]):
        return "Governing Law"
    
    # Non-Compete
    if any(kw in text_lower for kw in ["non-compete", "non compete", "not compete", "exclusivity", "exclusive"]):
        return "Non-Compete"
    
    # Force Majeure
    if any(kw in text_lower for kw in ["force majeure", "act of god", "beyond reasonable control"]):
        return "Force Majeure"
    
    # Warranties
    if any(kw in text_lower for kw in ["warrant", "warranty", "guarantee", "represent and warrant"]):
        return "Warranties"
    
    return "Other"
