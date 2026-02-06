import re
import streamlit as st

def extract_entities(text):
    """
    Enhanced NER: Extracts 12+ entity types from contracts using Regex Patterns.
    Pure Python implementation optimized for cloud deployment.
    """
    entities = {
        # Original 4 types
        "Parties (ORG)": set(),
        "Dates": set(),
        "Amounts": set(),
        "Jurisdiction (GPE)": set(),
        
        # NEW: 8+ additional types
        "Deliverables": set(),
        "Performance Metrics (SLAs)": set(),
        "Timeline Milestones": set(),
        "IP Ownership": set(),
        "Confidentiality Scope": set(),
        "Notice Periods": set(),
        "Termination Conditions": set(),
        "Liability Caps": set()
    }

    # Regex Extraction Logic
    
    # 1. Dates
    date_matches = re.findall(r"\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4}|\d{2}/\d{2}/\d{4}", text, re.IGNORECASE)
    entities["Dates"].update(date_matches)
    
    # 2. Amounts
    # Matches ₹ or Rs. followed by numbers
    amount_matches = re.findall(r"(?:Rs\.?|INR|₹|USD|\$)\s?[\d,]+(?:\.\d{2})?(?:/-)?(?:\s+(?:Lakh|Crore|Million|Billion))?", text, re.IGNORECASE)
    entities["Amounts"].update(amount_matches)

    # 3. Parties (Heuristic Capitalization)
    # Looking for "Between [X] and [Y]" patterns commonly found in contracts
    parties_pattern = r"BETWEEN\s+([A-Z][a-zA-Z0-9\s\.,]+?)\s+(?:AND|&)\s+([A-Z][a-zA-Z0-9\s\.,]+?)\s+(?:WHEREAS|dated|collected)"
    parties_match = re.search(parties_pattern, text, re.IGNORECASE)
    if parties_match:
         entities["Parties (ORG)"].add(parties_match.group(1).strip())
         entities["Parties (ORG)"].add(parties_match.group(2).strip())

    # 4. Jurisdiction
    jurisdiction_pattern = r"(?:subject to|governed by).*?jurisdiction.*?courts.*?in\s+([A-Z][a-zA-Z\s]+)"
    gpe_match = re.findall(jurisdiction_pattern, text, re.IGNORECASE)
    entities["Jurisdiction (GPE)"].update([g.strip() for g in gpe_match])

    # ===================================================================
    # NEW ENTITY EXTRACTIONS
    # ===================================================================
    
    # 1. Deliverables
    deliverable_patterns = [
        r"deliver(?:able)?s?:?\s+([^\.;]+)",
        r"(?:shall|will|must)\s+(?:provide|deliver|furnish)\s+([^\.;]+)",
        r"work product(?:\s+includes?)?:?\s+([^\.;]+)"
    ]
    for pattern in deliverable_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["Deliverables"].update([m.strip()[:100] for m in matches])  # Limit length
    
    # 2. Performance Metrics / SLAs
    sla_patterns = [
        r"(\d+%)\s+(?:uptime|availability)",
        r"(?:response time|turnaround time)(?:\s+of)?\s+(\d+\s+(?:hours?|days?|minutes?))",
        r"(?:SLA|service level):\s+([^\.;]+)",
        r"(\d+)\s+(?:business days?|working days?)"
    ]
    for pattern in sla_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            entities["Performance Metrics (SLAs)"].add(match if isinstance(match, str) else str(match))
    
    # 3. Timeline Milestones
    milestone_patterns = [
        r"milestone\s+\d+:?\s+([^\.;]+)",
        r"(?:phase|stage)\s+\d+:?\s+([^\.;]+)",
        r"within\s+(\d+\s+(?:days?|weeks?|months?))\s+of\s+([^\.;]+)",
        r"by\s+([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})"  # Specific dates like "March 15, 2024"
    ]
    for pattern in milestone_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                entities["Timeline Milestones"].add(f"{match[0]} - {match[1]}")
            else:
                entities["Timeline Milestones"].add(match[:80])
    
    # 4. IP Ownership
    ip_patterns = [
        r"(?:intellectual property|IP|copyright|patent|trademark)\s+(?:shall|will)\s+(?:vest in|belong to|be owned by)\s+([^\.;]+)",
        r"ownership of (?:work product|deliverables|IP):?\s+([^\.;]+)",
        r"(?:Client|Vendor|Company)\s+(?:owns|retains)\s+(?:all rights|ownership)(?:\s+to)?(?:\s+the)?\s+([^\.;]+)"
    ]
    for pattern in ip_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["IP Ownership"].update([m.strip()[:100] for m in matches])
    
    # 5. Confidentiality Scope
    confidentiality_patterns = [
        r"confidential information includes:?\s+([^\.;]+)",
        r"confidentiality period(?:\s+of)?\s+(\d+\s+years?)",
        r"(?:proprietary|confidential)\s+([^\.;]+?)\s+(?:shall|must)\s+(?:not|be kept)",
        r"non-disclosure(?:\s+of)?:?\s+([^\.;]+)"
    ]
    for pattern in confidentiality_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["Confidentiality Scope"].update([m.strip()[:100] for m in matches])
    
    # 6. Notice Periods
    notice_patterns = [
        r"(\d+)\s+(?:days?|months?)\s+(?:written\s+)?notice",
        r"notice period(?:\s+of)?\s+(\d+\s+(?:days?|months?))",
        r"(?:upon|with)\s+(\d+\s+(?:days?|months?))\s+prior notice"
    ]
    for pattern in notice_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            entities["Notice Periods"].add(f"{match} notice" if isinstance(match, str) else str(match))
    
    # 7. Termination Conditions
    termination_patterns = [
        r"terminat(?:e|ion)(?:\s+for)?:?\s+([^\.;]+?)\s+(?:if|upon|in case of)",
        r"(?:either party|Client|Vendor)\s+may terminate(?:\s+this agreement)?:?\s+([^\.;]+)",
        r"grounds for termination:?\s+([^\.;]+)"
    ]
    for pattern in termination_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["Termination Conditions"].update([m.strip()[:100] for m in matches])
    
    # 8. Liability Caps
    liability_patterns = [
        r"(?:maximum|aggregate)\s+liability(?:\s+shall)?(?:\s+not)?\s+exceed\s+((?:Rs\.?|INR|₹)\s?[\d,]+)",
        r"liability(?:\s+is)?\s+limited to\s+([^\.;]+)",
        r"cap(?:ped)?\s+at\s+((?:Rs\.?|INR|₹)\s?[\d,]+)"
    ]
    for pattern in liability_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        entities["Liability Caps"].update([m.strip() for m in matches])

    return {k: sorted(list(v)) for k, v in entities.items()}


def extract_entities_summary(entities_dict):
    """
    Generate a human-readable summary of extracted entities.
    Useful for UI display.
    """
    summary = []
    
    for entity_type, values in entities_dict.items():
        if values:
            summary.append(f"**{entity_type}:** {', '.join(values[:3])}" + (" and more..." if len(values) > 3 else ""))
    
    return "\n".join(summary) if summary else "No key entities extracted."

