from config import RISK_KEYWORDS, RISK_EXPLANATIONS
import re

RISK_SCORE_MAP = {
    "Low": 1,
    "Medium": 2,
    "High": 5
}

def assess_risk_with_explanation(clause):
    """
    Returns risk level + exact phrases that triggered it + explanations.
    This provides transparency into why a clause is risky.
    """
    clause_lower = clause.lower()
    triggers = []
    
    # Check High Risk keywords first
    for kw in RISK_KEYWORDS["High"]:
        if kw in clause_lower:
            # Find the actual phrase with context
            start_idx = clause_lower.find(kw)
            context_start = max(0, start_idx - 30)
            context_end = min(len(clause), start_idx + len(kw) + 30)
            context = clause[context_start:context_end]
            
            triggers.append({
                "keyword": kw,
                "context": context.strip(),
                "severity": "High",
                "explanation": RISK_EXPLANATIONS["High"].get(kw, "This term creates significant risk.")
            })
    
    # Check Medium Risk keywords (now always checked to provide complete profile)
    for kw in RISK_KEYWORDS["Medium"]:
        if kw in clause_lower:
            start_idx = clause_lower.find(kw)
            context_start = max(0, start_idx - 30)
            context_end = min(len(clause), start_idx + len(kw) + 30)
            context = clause[context_start:context_end]
            
            triggers.append({
                "keyword": kw,
                "context": context.strip(),
                "severity": "Medium",
                "explanation": RISK_EXPLANATIONS["Medium"].get(kw, "This term may need clarification.")
            })
    
    if triggers:
        # Return highest severity found
        highest_severity = "High" if any(t["severity"] == "High" for t in triggers) else "Medium"
        return {
            "risk": highest_severity,
            "triggers": triggers,
            "summary": f"Found {len(triggers)} risk indicator(s)",
            "trigger_count": len(triggers)
        }
    
    return {
        "risk": "Low",
        "triggers": [],
        "summary": "No major risk indicators detected",
        "trigger_count": 0
    }


def assess_risk(clause):
    """
    Simple risk assessment (backward compatibility).
    Returns just the risk level string.
    """
    result = assess_risk_with_explanation(clause)
    return result["risk"]


def contract_risk_score(results):
    """
    Calculates overall contract risk based on clause-level risks.
    Enhanced with more nuanced scoring.
    """
    if not results:
        return "Low"
    
    scores = [RISK_SCORE_MAP.get(r.get("risk", "Low"), 1) for r in results]
    total_clauses = len(results)
    avg_score = sum(scores) / total_clauses
    
    # Count high and medium risk clauses
    high_count = sum(1 for r in results if r.get("risk") == "High")
    medium_count = sum(1 for r in results if r.get("risk") == "Medium")
    
    # Decision logic
    if high_count >= 3:
        return "High"  # Multiple critical issues
    elif high_count >= 2 or avg_score >= 2.5:
        return "High"  # Two critical issues or very high average
    elif high_count == 1 and medium_count >= 3:
        return "High"  # One critical + several medium = overall high risk
    elif high_count == 1 or avg_score >= 1.5:
        return "Medium"  # One critical or elevated average
    elif medium_count >= 4:
        return "Medium"  # Many medium-risk items add up
    else:
        return "Low"  # Mostly clean contract


def calculate_financial_risk(results, entities):
    """
    Estimates financial exposure from contract terms.
    Returns penalty amounts and business disruption estimates.
    """
    penalty_exposure = 0
    disruption_days = 0
    risk_factors = []
    
    # Extract amounts from entities
    amounts = entities.get('Amounts', [])
    parsed_amounts = [parse_indian_currency(amt) for amt in amounts]
    contract_value = max(parsed_amounts) if parsed_amounts else 100000  # Default 1 lakh
    
    for result in results:
        clause_text = result.get('text', '').lower()
        risk_level = result.get('risk', 'Low')
        
        if risk_level == 'High':
            # Penalty clauses
            if 'penalty' in clause_text or 'liquidated damages' in clause_text:
                # Try to extract penalty amount
                penalty_amounts = re.findall(r'[₹Rs\.]*\s*[\d,]+', result.get('text', ''))
                if penalty_amounts:
                    penalty = parse_indian_currency(penalty_amounts[0])
                    penalty_exposure += penalty
                    risk_factors.append(f"Penalty clause: ₹{penalty:,.0f}")
                else:
                    # Estimate as 10-20% of contract value
                    estimated_penalty = contract_value * 0.15
                    penalty_exposure += estimated_penalty
                    risk_factors.append(f"Penalty clause: ~₹{estimated_penalty:,.0f} (estimated)")
            
            # Unlimited indemnity/liability
            if 'unlimited' in clause_text and ('indemnity' in clause_text or 'liability' in clause_text):
                # This is extremely risky - use 5x contract value as exposure estimate
                unlimited_exposure = contract_value * 5
                penalty_exposure += unlimited_exposure
                risk_factors.append(f"Unlimited liability: ₹{unlimited_exposure:,.0f} exposure")
            
            # Termination clauses
            if 'termination' in result.get('type', '').lower():
                # Business disruption from sudden termination
                disruption_days += 30  # Time to find replacement client/vendor
                risk_factors.append("Termination risk: 30 days disruption")
            
            # Foreign jurisdiction
            if any(loc in clause_text for loc in ['london', 'singapore', 'new york']):
                # Cost of foreign legal proceedings
                foreign_legal_cost = 1000000  # 10 lakhs minimum for foreign arbitration
                penalty_exposure += foreign_legal_cost
                risk_factors.append(f"Foreign jurisdiction: ₹{foreign_legal_cost:,.0f} legal costs")
    
    # Default estimates if no specific risks found
    if penalty_exposure == 0 and any(r.get('risk') == 'High' for r in results):
        # Scale litigation costs based on contract value
        if contract_value > 10000000:  # > 1 Crore
            litigation_est = 1500000  # 15 lakhs
        elif contract_value > 1000000:  # > 10 Lakhs
            litigation_est = 500000   # 5 lakhs
        else:
            litigation_est = 200000   # 2 lakhs
        
        penalty_exposure = litigation_est
        risk_factors.append(f"Contextual litigation risk: ₹{litigation_est:,.0f} (based on contract size)")
    
    return {
        'penalty_amount': int(penalty_exposure),
        'disruption_days': disruption_days,
        'risk_factors': risk_factors,
        'contract_value': int(contract_value)
    }


def parse_indian_currency(amount_str):
    """
    Extract number from Indian currency strings like '₹2,00,000/-' or 'Rs. 50,000'.
    Handles lakhs and crores notation.
    """
    if not amount_str:
        return 0
    
    # Remove currency symbols and common suffixes, but preserve 'lakh' and 'crore' for further processing
    cleaned = str(amount_str).lower()
    cleaned = re.sub(r'[₹rs\.\s/\-inr]', '', cleaned)
    
    # Handle lakhs/crores
    if 'lakh' in amount_str.lower():
        number = float(re.sub(r'[^\d\.]', '', cleaned))
        return int(number * 100000)
    elif 'crore' in amount_str.lower():
        number = float(re.sub(r'[^\d\.]', '', cleaned))
        return int(number * 10000000)
    
    # Regular number with commas
    cleaned = cleaned.replace(',', '')
    try:
        return int(float(cleaned))
    except ValueError:
        return 0
