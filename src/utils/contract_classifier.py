from src.config import CONTRACT_TYPE_KEYWORDS

def classify_contract(text):
    """
    Identifies the type of contract based on content analysis.
    Uses keyword matching with scoring to handle mixed content.
    """
    text_lower = text.lower()
    
    scores = {}
    for contract_type, keywords in CONTRACT_TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[contract_type] = score
    
    # Return type with highest score
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    else:
        return "Service Agreement"  # Default fallback
