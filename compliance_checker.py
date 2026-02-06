"""
Indian Legal Compliance Checker
Validates contract clauses against common Indian law requirements
"""

# Indian Contract Act, 1872 - Key Requirements
INDIAN_CONTRACT_ACT_PATTERNS = {
    "consideration": {
        "required": True,
        "patterns": ["consideration", "in consideration of", "for value"],
        "violation_message": "No explicit consideration mentioned (required under Indian Contract Act Sec 10)"
    },
    "free_consent": {
        "red_flags": ["coercion", "undue influence", "fraud", "misrepresentation"],
        "violation_message": "Potential consent issues detected"
    },
    "lawful_object": {
        "prohibited": ["illegal", "opposed to public policy", "immoral"],
        "violation_message": "Potentially unlawful contract object"
    }
}

# Consumer Protection Act, 2019 - Unfair Terms
CONSUMER_PROTECTION_UNFAIR_TERMS = [
    "exclude liability for negligence",
    "no refund under any circumstances",
    "bind consumer to arbitration without choice",
    "unilateral price change",
    "automatic renewal without notice"
]

# Arbitration & Conciliation Act, 1996
ARBITRATION_COMPLIANCE = {
    "valid_triggers": ["disputes arising out of", "any dispute in connection with"],
    "seat_requirements": ["seat of arbitration", "place of arbitration"],
    "invalid_patterns": ["arbitration at sole discretion", "one-party appointment"]
}

# Employment Contract - Minimum Compliance
EMPLOYMENT_LAW_REQUIREMENTS = {
    "notice_period": {
        "min_days": 30,
        "patterns": [r"(\d+)\s*days?\s*notice", r"notice period of (\d+)"],
        "violation": "Notice period less than minimum 30 days"
    },
    "termination_grounds": {
        "required": ["misconduct", "performance", "redundancy"],
        "violation": "Unclear termination grounds"
    }
}


def check_compliance(contract_text, contract_type, clauses):
    """
    Check contract for compliance with Indian laws using AI-driven analysis.
    This ensures that all feedback is strictly related to the document.
    """
    from llm import analyze_compliance_with_ai
    
    # 1. Get AI-driven dynamic compliance report
    compliance_report = analyze_compliance_with_ai(contract_text, contract_type)
    
    # 2. Add static baselines as supplementary (only if needed)
    # Most of the static logic is now superseded by the dynamic AI analysis
    # to meet the user's requirement for "no static response".
    
    # Ensure structure is correct if AI fails
    if not isinstance(compliance_report, dict):
        compliance_report = {
            "overall_status": "Unknown",
            "violations": [],
            "warnings": []
        }
    
    # Fallback to overall status check
    if not compliance_report.get("violations") and not compliance_report.get("warnings"):
        compliance_report["overall_status"] = "Compliant"
    
    return compliance_report


def generate_compliance_summary(compliance_report):
    """
    Generate human-readable summary.
    Maintained for backward compatibility with UI.
    """
    
    status = compliance_report.get("overall_status", "Unknown")
    violations = compliance_report.get("violations", [])
    warnings = compliance_report.get("warnings", [])
    
    summary = f"**Compliance Status:** {status}\n\n"
    
    if violations:
        summary += f"**{len(violations)} Violation(s) Found:**\n"
        for v in violations:
            summary += f"- ⚠️ **{v['law']}:** {v['issue']}\n"
            summary += f"  *Recommendation:* {v['recommendation']}\n\n"
    
    if warnings:
        summary += f"**{len(warnings)} Warning(s):**\n"
        for w in warnings:
            summary += f"- 🟡 **{w['law']}:** {w['issue']}\n"
            summary += f"  *Recommendation:* {w['recommendation']}\n\n"
    
    if not violations and not warnings:
        summary += "✅ No obvious compliance issues detected in the analysed text."
    
    return summary
