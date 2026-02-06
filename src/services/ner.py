import spacy
import re

import streamlit as st

@st.cache_resource
def load_nlp_model():
    try:
        # Robust loading: Try to import as a module first (Best for Streamlit Cloud)
        import en_core_web_sm
        nlp = en_core_web_sm.load()
    except ImportError:
        # Fallback: standard spacy loading
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Last resort: download
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    return nlp

def extract_entities(text):
    """
    Enhanced NER: Extracts 12+ entity types from contracts.
    Backward compatible - returns same structure as before but with more entities.
    """
    try:
        nlp = load_nlp_model()
    except OSError:
        # Fallback if download failed
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = load_nlp_model()
        
    doc = nlp(text)

    entities = {
        # Original 4 types (backward compatible)
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

    # SpaCy extraction (original)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["Parties (ORG)"].add(ent.text)
        elif ent.label_ == "DATE":
            entities["Dates"].add(ent.text)
        elif ent.label_ == "MONEY":
            entities["Amounts"].add(ent.text)
        elif ent.label_ == "GPE":
            entities["Jurisdiction (GPE)"].add(ent.text)

    # Regex Fallback for original types
    if not entities["Dates"]:
         date_matches = re.findall(r"\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s+\d{4}|\d{2}/\d{2}/\d{4}", text, re.IGNORECASE)
         entities["Dates"].update(date_matches)
    
    if not entities["Amounts"]:
         # Matches ₹ or Rs. followed by numbers
         amount_matches = re.findall(r"(?:Rs\.?|INR|₹)\s?[\d,]+(?:\.\d{2})?(?:/-)? ", text)
         entities["Amounts"].update(amount_matches)

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

