from config import STANDARD_CLAUSES
from difflib import SequenceMatcher
from llm import analyze_clause_differences

def compare_clause_to_standard(user_clause, clause_type):
    """
    Compares user's clause against the standard safe clause.
    Returns side-by-side comparison with AI-generated difference analysis.
    """
    
    if clause_type not in STANDARD_CLAUSES:
        return None
    
    standard_data = STANDARD_CLAUSES[clause_type]
    standard_clause = standard_data["safe"]
    
    # Calculate text similarity
    similarity_score = int(SequenceMatcher(None, 
                                          user_clause.lower(), 
                                          standard_clause.lower()).ratio() * 100)
    
    # Determine verdict based on similarity
    if similarity_score >= 70:
        verdict = "SAFE"
        verdict_color = "green"
    elif similarity_score >= 40:
        verdict = "REVIEW NEEDED"
        verdict_color = "orange"
    else:
        verdict = "RISKY"
        verdict_color = "red"
    
    # Get AI analysis of differences
    diff_analysis = analyze_clause_differences(user_clause, standard_clause)
    
    return {
        "user_clause": user_clause,
        "standard_clause": standard_clause,
        "standard_description": standard_data["description"],
        "similarity_score": similarity_score,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "differences": diff_analysis.get("differences", []),
        "recommendation": diff_analysis.get("recommendation", "Review with legal counsel")
    }


def check_similarity(clause_text, clause_type):
    """
    Returns similarity score and standard clause (backward compatibility).
    """
    if clause_type not in STANDARD_CLAUSES:
        return None, None
    
    standard = STANDARD_CLAUSES[clause_type]["safe"]
    ratio = SequenceMatcher(None, clause_text.lower(), standard.lower()).ratio()
    return int(ratio * 100), standard
