import anthropic
import os
import json

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    timeout=60.0  # Increased timeout for batch processing
)

def analyze_all_clauses_batch(clauses_with_types):
    """
    BATCH PROCESSING: Analyze all clauses in a single Claude API call.
    This is 5-10x faster than analyzing clauses one-by-one.
    
    Args:
        clauses_with_types: List of dicts with 'text' and 'type' keys
    
    Returns:
        List of analysis results matching the order of input clauses
    """
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        # Return fallback for all clauses
        return [{
            "risk_level": "Unknown",
            "business_consequences": ["⚠️ API key not configured"],
            "specific_issues": [],
            "plain_english": "API configuration required",
            "standard_alternative": "Configure API key",
            "negotiation_script": "",
            "mitigation_strategies": []
        } for _ in clauses_with_types]
    
    # Build batch prompt
    clauses_text = ""
    for idx, item in enumerate(clauses_with_types, 1):
        clauses_text += f"\n\n---CLAUSE {idx}---\nTYPE: {item['type']}\nTEXT: {item['text']}\n"
    
    prompt = f"""You are a business advisor for Indian SMEs. Analyze ALL the following contract clauses in ONE response.

{clauses_text}

Respond with ONLY valid JSON array (no markdown, no code blocks):
[
  {{
    "clause_number": 1,
    "risk_level": "Low|Medium|High",
    "business_consequences": ["specific scenario that could happen"],
    "mitigation_strategies": [
      {{
        "name": "Short label",
        "action": "Exactly what to do",
        "clause_example": "Reworded clause snippet",
        "timeline": "When to act",
        "priority": "Critical|High|Medium"
      }}
    ],
    "specific_issues": [
      {{
        "phrase": "exact problematic phrase",
        "why_dangerous": "business reason",
        "example_scenario": "realistic example"
      }}
    ],
    "plain_english": "Two sentences explaining this clause simply",
    "standard_alternative": "Better version of this clause",
    "negotiation_script": "Exact words to request changes"
  }},
  ... (one object per clause)
]

CRITICAL: Return exactly {len(clauses_with_types)} analysis objects in the array, one per clause, in order."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,  # Larger for batch
            temperature=0.2,
            system="You are a business advisor. Respond ONLY with valid JSON array. Analyze each clause for business impact.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # Extract JSON array
        if "[" in response_text and "]" in response_text:
            start = response_text.find("[")
            end = response_text.rfind("]") + 1
            json_str = response_text[start:end]
            results = json.loads(json_str)
        else:
            raise ValueError("No JSON array found")
        
        # Ensure we have results for all clauses
        while len(results) < len(clauses_with_types):
            results.append({
                "risk_level": "Unknown",
                "business_consequences": ["Analysis incomplete"],
                "specific_issues": [],
                "plain_english": "Analysis incomplete for this clause",
                "standard_alternative": "Review manually",
                "negotiation_script": "",
                "mitigation_strategies": []
            })
        
        return results[:len(clauses_with_types)]  # Trim if too many
        
    except Exception as e:
        print(f"Batch analysis error: {e}")
        # Return fallback for all clauses
        return [{
            "risk_level": "Medium",
            "business_consequences": [f"Batch analysis failed: {str(e)}"],
            "specific_issues": [],
            "plain_english": "Analysis unavailable",
            "standard_alternative": "Review manually",
            "negotiation_script": "",
            "mitigation_strategies": []
        } for _ in clauses_with_types]


def analyze_clause_with_reasoning(clause_text, clause_type):
    """
    SINGLE clause analysis (kept for backwards compatibility).
    For new code, use analyze_all_clauses_batch() instead.
    """
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "risk_level": "Unknown",
            "business_consequences": ["⚠️ API key not configured. Set ANTHROPIC_API_KEY environment variable."],
            "specific_issues": [],
            "plain_english": "API configuration required for AI analysis.",
            "standard_alternative": "Configure API key to get recommendations.",
            "negotiation_script": "",
            "mitigation_strategies": []
        }
    
    prompt = f"""You are a business advisor for Indian SMEs, not just a legal analyst.

CLAUSE TO ANALYZE:
{clause_text}

CLAUSE TYPE: {clause_type}

Your job: Help the business owner understand the BUSINESS CONSEQUENCES of this clause and provide specific, actionable MITIGATION STRATEGIES.

Respond with ONLY valid JSON (no markdown, no code blocks):
{{
  "risk_level": "Low|Medium|High",
  
  "business_consequences": [
    "If you sign this as-is: [specific scenario that could happen to their business]",
    "If this clause is triggered: [concrete financial/operational impact]",
    "Long-term effect: [how this affects business 6-12 months from now]"
  ],
  
  "mitigation_strategies": [
    {{
      "name": "Short label for the fix",
      "action": "Exactly what the business owner should do or ask for",
      "clause_example": "A snippet of how the clause should be reworded to be safer",
      "timeline": "When this action should be taken (e.g., 'Before signing', 'Within 30 days')",
      "priority": "Critical|High|Medium"
    }}
  ],
  
  "specific_issues": [
    {{
      "phrase": "exact problematic phrase",
      "why_dangerous": "specific business reason (not legal jargon)",
      "example_scenario": "realistic example of when this could hurt them"
    }}
  ],
  
  "plain_english": "Two sentences explaining this clause to someone with zero legal knowledge",
  
  "standard_alternative": "Better version of this clause that protects both parties",
  
  "negotiation_script": "Exact words to say when asking them to change this: 'Hi [name], after reviewing the contract, I have concerns about [specific issue]. Would you be open to changing it to [specific request]? This would be more balanced for both of us.'"
}}

CRITICAL: Everything must be DYNAMIC and based ONLY on the provided clause. Do not provide generic legal advice. Focus on concrete BUSINESS IMPACT and ACTIONABLE fixes. Use rupee amounts when possible."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.2,
            system="You are a business advisor for Indian SMEs. Respond ONLY with valid JSON. Focus on document-specific business consequences and actionable mitigation, not legal jargon.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        
        # Robust JSON extraction
        if "{" in response_text and "}" in response_text:
            try:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                json_str = response_text[start:end]
                result = json.loads(json_str)
            except json.JSONDecodeError:
                if response_text.startswith("```"):
                    response_text = response_text.split("```")[1]
                    if response_text.startswith("json"):
                        response_text = response_text[4:]
                result = json.loads(response_text.strip())
        else:
            raise ValueError("No JSON object found in response")
        
        # Ensure all required fields exist
        if "business_consequences" not in result:
            result["business_consequences"] = ["Analysis completed"]
        if "mitigation_strategies" not in result:
            result["mitigation_strategies"] = []
        if "negotiation_script" not in result:
            result["negotiation_script"] = "Discuss this clause with the other party"
            
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {
            "risk_level": "Medium",
            "business_consequences": ["Unable to parse AI response"],
            "specific_issues": [],
            "plain_english": "This clause requires careful review",
            "standard_alternative": "Consult with a legal professional",
            "negotiation_script": "Let's discuss this clause",
            "mitigation_strategies": []
        }
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return {
            "risk_level": "Unknown",
            "business_consequences": [f"API error: {str(e)}"],
            "specific_issues": [],
            "plain_english": "Unable to analyze clause",
            "standard_alternative": "Please try again",
            "negotiation_script": "",
            "mitigation_strategies": []
        }


def generate_decision_summary(full_text, decision_data, risk_profile):
    """
    NEW: Decision-focused summary that answers "What should I do?"
    Not just "here's what's in it" but "here's your action plan"
    """
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        return "⚠️ API key not configured. Set ANTHROPIC_API_KEY to generate decision summaries."
    
    verdict = decision_data.get('verdict', 'UNKNOWN')
    must_negotiate = decision_data.get('must_negotiate', [])
    consequences = decision_data.get('consequences_if_signed', {})
    
    prompt = f"""You are a business advisor speaking directly to an Indian SME owner who needs to make a DECISION.

CONTRACT SITUATION:
- Overall Risk: {risk_profile.get('overall_risk', 'Unknown')}
- High-Risk Clauses: {len(must_negotiate)}
- RECOMMENDATION: {verdict}

MUST FIX THESE CLAUSES:
{json.dumps(must_negotiate[:3], indent=2) if must_negotiate else "None"}

CONSEQUENCES IF SIGNED AS-IS:
{json.dumps(consequences, indent=2)}

Write a DECISION-FOCUSED summary in this format:

**🎯 Bottom Line:**
[One clear sentence: Should they sign, negotiate, or reject?]

**⚠️ Critical Issues:**
[2-3 bullet points of the most dangerous problems]

**💰 Financial Exposure:**
[Specific rupee amounts they could lose]

**✅ What You Must Do Next:**
[3 specific action items with timeline]

**🔥 Worst Case Scenario:**
[One paragraph: What's the absolute worst that could happen if they sign this as-is?]

**🛡️ How to Protect Yourself:**
[Specific negotiation points - exact language to request]

Write like you're their co-founder who's looking out for them. Be direct. Use "you" and "your business". 
If it's dangerous, be scary. If it's safe, be reassuring. Give them confidence to act."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            temperature=0.3,
            system="You are a business advisor. Write decision-focused summaries that tell SME owners exactly what to do.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"⚠️ Error generating summary: {str(e)}"


def analyze_clause_differences(user_clause, standard_clause):
    """Uses Claude to identify semantic differences between user's clause and standard clause."""
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "differences": [{
                "aspect": "Missing API Key",
                "impact": "API key not configured. Cannot perform comparison analysis.",
                "business_impact": "API key not configured."
            }],
            "recommendation": "Configure API key for comparison analysis"
        }
    
    prompt = f"""Compare these clauses and explain the BUSINESS IMPACT of the differences:

YOUR CLAUSE:
{user_clause}

STANDARD SAFE CLAUSE:
{standard_clause}

JSON format:
{{
  "differences": [
    {{
      "aspect": "what's different",
      "your_version": "what yours says",
      "standard_version": "what the safe version says",
      "impact": "how this difference affects their business (be specific and concrete)"
    }}
  ],
  "recommendation": "Clear action: 'Change X to Y' or 'This is acceptable as-is'"
}}

Focus on material differences that create business risk. Skip formatting differences."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0.2,
            system="Business advisor for SMEs. Respond with valid JSON only.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        if "```" in response_text:
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        
        return json.loads(response_text.strip())
        
    except Exception as e:
        return {
            "differences": [{"aspect": "Analysis unavailable", "impact": str(e)}],
            "recommendation": "Manual review recommended"
        }


# Backward compatibility
def generate_contract_summary(full_text, entities, risk_profile):
    """Legacy function - redirects to new decision-focused version"""
    decision_data = {"verdict": "UNKNOWN", "must_negotiate": [], "consequences_if_signed": {}}
    return generate_decision_summary(full_text, decision_data, risk_profile)

def ask_llm(system_prompt, user_prompt):
    """Legacy simple LLM wrapper"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        return "⚠️ API key not configured"
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ AI Service Unavailable: {str(e)}"

def analyze_compliance_with_ai(contract_text, contract_type):
    """
    AI-driven compliance checker that looks for document-specific violations
    of Indian law based on the actual contract language.
    """
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        return {
            "overall_status": "Unknown",
            "violations": [],
            "warnings": []
        }
    
    prompt = f"""You are an Indian legal compliance expert. 
Analyze the following contract for compliance with Indian laws (Contract Act 1872, Consumer Protection Act 2019, Arbitration Act 1996, etc.).

CONTRACT TYPE: {contract_type}

CONTRACT TEXT (EXCERPT):
{contract_text[:8000]}

Your job is to identify SPECIFIC violations or risks in THIS document. No generic advice.

Respond with ONLY valid JSON:
{{
  "overall_status": "Compliant|Needs Review|Non-Compliant",
  "violations": [
    {{
      "law": "Specific Indian Law & Section",
      "issue": "What exactly is wrong in this document",
      "severity": "High|Medium",
      "recommendation": "Specific fix for this document"
    }}
  ],
  "warnings": [
    {{
      "law": "Related Law",
      "issue": "A potential risk or missing best practice",
      "severity": "Medium|Low",
      "recommendation": "Specific suggestion"
    }}
  ]
}}

CRITICAL: Only identify violations and warnings that actually appear in this text. If it is fully compliant, say so."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            temperature=0.2,
            system="Indian legal compliance expert. Respond with valid JSON only.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        if "{" in response_text and "}" in response_text:
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            return json.loads(response_text[start:end])
        return json.loads(response_text)
        
    except Exception as e:
        print(f"Compliance AI Error: {e}")
        return {"overall_status": "Unknown", "violations": [], "warnings": []}
