"""
Decision Engine - Transforms risk analysis into actionable business decisions.

This is the KEY differentiator: We don't just analyze - we tell SMEs what to DO.
"""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class ContractDecisionEngine:
    """
    Converts risk analysis into clear business recommendations.
    Answers the questions SMEs actually ask:
    - Should I sign this?
    - What will happen if I do?
    - What MUST I change?
    - What can I negotiate?
    """
    
    def __init__(self):
        self.decision_thresholds = {
            "sign_immediately": {"high_risks": 0, "medium_risks": 0, "red_flags": []},
            "negotiate_first": {"high_risks": [1, 2], "medium_risks": [0, 5], "red_flags": ["partial"]},
            "reject_or_major_revision": {"high_risks": [3, 999], "medium_risks": [0, 999], "red_flags": ["critical"]}
        }
    
    def generate_decision(self, analysis_results: Dict) -> Dict:
        """
        Main decision generation function.
        Returns: verdict, reasoning, action items, timeline, consequences
        """
        
        high_risk_count = analysis_results.get('high_risk_count', 0)
        medium_risk_count = analysis_results.get('medium_risk_count', 0)
        financial_impact = analysis_results.get('financial_impact', {})
        clauses = analysis_results.get('results', [])
        
        # Identify critical red flags
        red_flags = self._identify_red_flags(clauses)
        
        # Calculate decision score
        decision_score = self._calculate_decision_score(
            high_risk_count, 
            medium_risk_count, 
            financial_impact.get('penalty_amount', 0),
            red_flags
        )
        
        # Generate verdict
        verdict = self._determine_verdict(decision_score, high_risk_count, red_flags)
        
        # Build comprehensive decision package
        decision = {
            "verdict": verdict,
            "confidence": self._calculate_confidence(decision_score, high_risk_count),
            "decision_score": decision_score,  # 0-100, lower = safer
            
            "primary_reasoning": self._generate_primary_reasoning(verdict, high_risk_count, medium_risk_count, red_flags),
            
            "must_negotiate": self._extract_must_negotiate_clauses(clauses),
            "nice_to_negotiate": self._extract_nice_to_negotiate_clauses(clauses),
            
            "consequences_if_signed": self._simulate_signing_consequences(clauses, financial_impact),
            "consequences_if_rejected": self._simulate_rejection_consequences(analysis_results),
            
            "action_plan": self._create_action_plan(verdict, clauses),
            "timeline": self._estimate_negotiation_timeline(verdict, high_risk_count),
            
            "negotiation_leverage": self._assess_leverage(analysis_results),
            "walkaway_triggers": red_flags,
        }
        
        return decision
    
    def _identify_red_flags(self, clauses: List[Dict]) -> List[Dict]:
        """
        Red flags = absolute deal-breakers that require immediate attention.
        """
        red_flags = []
        
        critical_patterns = {
            "unlimited_liability": ["unlimited liability", "unlimited indemnity", "no liability cap"],
            "foreign_jurisdiction": ["courts in london", "courts at new york", "singapore", "arbitration in london"],
            "instant_termination": ["without notice", "without cause", "sole discretion"],
            "perpetual_obligations": ["perpetual", "irrevocable", "permanent"],
            "assignment_of_all_ip": ["all intellectual property", "all ip rights", "assigns all rights"]
        }
        
        for clause in clauses:
            if clause.get('risk') != 'High':
                continue
            
            clause_text = clause.get('text', '').lower()
            
            for flag_type, patterns in critical_patterns.items():
                for pattern in patterns:
                    if pattern in clause_text:
                        red_flags.append({
                            "type": flag_type,
                            "clause_id": clause.get('id'),
                            "clause_type": clause.get('type'),
                            "severity": "CRITICAL",
                            "why_dealbreaker": self._explain_red_flag(flag_type),
                            "text_excerpt": clause_text[:150]
                        })
                        break
        
        return red_flags
    
    def _explain_red_flag(self, flag_type: str) -> str:
        """Explains why each red flag is a deal-breaker."""
        explanations = {
            "unlimited_liability": "You could be sued for ANY amount - potentially bankrupting your business over a minor issue.",
            "foreign_jurisdiction": "Disputes in foreign courts cost ₹10-50 lakhs minimum. Practically impossible for SMEs.",
            "instant_termination": "They can end the contract tomorrow without warning. Zero business stability.",
            "perpetual_obligations": "These obligations last FOREVER - even after contract ends. Extremely dangerous.",
            "assignment_of_all_ip": "You lose ownership of your own intellectual property. Can't reuse your own work."
        }
        return explanations.get(flag_type, "This clause creates extreme business risk.")
    
    def _calculate_decision_score(self, high_risk: int, medium_risk: int, 
                                  penalty_amount: int, red_flags: List) -> int:
        """
        Decision score: 0 = perfectly safe, 100 = extremely dangerous
        """
        score = 0
        
        # High-risk clauses (each worth 20 points)
        score += high_risk * 20
        
        # Medium-risk clauses (each worth 5 points)
        score += medium_risk * 5
        
        # Financial impact (normalized)
        if penalty_amount > 500000:  # >5 lakhs
            score += 25
        elif penalty_amount > 200000:  # >2 lakhs
            score += 15
        
        # Red flags (each worth 15 points)
        score += len(red_flags) * 15
        
        # Cap at 100
        return min(score, 100)
    
    def _determine_verdict(self, score: int, high_risk: int, red_flags: List) -> str:
        """
        Three clear verdicts:
        1. SIGN - Safe to proceed
        2. NEGOTIATE - Fixable with changes
        3. REJECT - Too risky, walk away
        """
        
        # Instant reject conditions
        if len(red_flags) >= 3:
            return "REJECT"
        if high_risk >= 4:
            return "REJECT"
        if score >= 70:
            return "REJECT"
        
        # Sign conditions
        if score <= 20 and high_risk == 0:
            return "SIGN"
        
        # Default: negotiate
        return "NEGOTIATE"
    
    def _calculate_confidence(self, score: int, high_risk: int) -> str:
        """How confident are we in this recommendation?"""
        if (score <= 15 or score >= 80):
            return "High"
        elif high_risk == 0:
            return "High"
        else:
            return "Medium"
    
    def _generate_primary_reasoning(self, verdict: str, high: int, medium: int, flags: List) -> str:
        """
        One-sentence explanation of the verdict.
        """
        if verdict == "SIGN":
            return f"Contract appears safe with only {medium} minor concern(s). Standard terms for Indian SMEs."
        
        elif verdict == "NEGOTIATE":
            return f"Found {high} critical issue(s) and {medium} concern(s). Fixable through negotiation - don't sign as-is."
        
        else:  # REJECT
            critical_flags = [f["type"].replace("_", " ") for f in flags[:2]]
            flag_text = ", ".join(critical_flags) if critical_flags else "multiple critical issues"
            return f"CONTRACT IS DANGEROUS. {high} high-risk clauses including {flag_text}. Recommend finding a different vendor/client."
    
    def _extract_must_negotiate_clauses(self, clauses: List[Dict]) -> List[Dict]:
        """
        Clauses you MUST change before signing.
        These are non-negotiable from a business safety perspective.
        """
        must_fix = []
        
        for clause in clauses:
            if clause.get('risk') == 'High':
                must_fix.append({
                    "clause_id": clause.get('id'),
                    "title": clause.get('type'),
                    "current_problem": clause.get('explanation', '')[:200],
                    "what_to_request": clause.get('suggestion', '')[:200],
                    "fallback_position": self._generate_fallback(clause)
                })
        
        return must_fix
    
    def _extract_nice_to_negotiate_clauses(self, clauses: List[Dict]) -> List[Dict]:
        """
        Clauses that would be good to improve but aren't deal-breakers.
        """
        nice_to_fix = []
        
        for clause in clauses:
            if clause.get('risk') == 'Medium':
                nice_to_fix.append({
                    "clause_id": clause.get('id'),
                    "title": clause.get('type'),
                    "improvement": clause.get('suggestion', '')[:150]
                })
        
        return nice_to_fix[:3]  # Limit to top 3 to avoid overwhelming
    
    def _generate_fallback(self, clause: Dict) -> str:
        """
        If they won't accept your ideal change, what's the minimum acceptable?
        """
        clause_type = clause.get('type', '').lower()
        
        fallbacks = {
            "termination": "Minimum: 30-day notice period + payment for work completed",
            "indemnity": "Minimum: Cap liability at contract value",
            "governing law": "Minimum: Arbitration in India (not foreign court)",
            "payment": "Minimum: Payment within 45 days (not 60-90)",
            "non-compete": "Minimum: Limit to 1 year and same city only"
        }
        
        for key, fallback in fallbacks.items():
            if key in clause_type:
                return fallback
        
        return "Minimum: Add reasonable limits and mutual obligations"
    
    def _simulate_signing_consequences(self, clauses: List[Dict], financial: Dict) -> Dict:
        """
        What happens if you sign THIS contract as-is?
        Concrete, scary, specific consequences.
        """
        consequences = {
            "immediate_risks": [],
            "month_1_3": [],
            "month_3_12": [],
            "long_term": [],
            "worst_case_scenario": ""
        }
        
        # Immediate risks
        for clause in clauses:
            if clause.get('risk') == 'High':
                clause_type = clause.get('type', '').lower()
                
                if 'termination' in clause_type:
                    consequences["immediate_risks"].append(
                        "They can terminate tomorrow without warning. You lose all recurring revenue instantly."
                    )
                elif 'payment' in clause_type:
                    consequences["month_1_3"].append(
                        "You'll be waiting 60-90 days for payment. Cash flow crisis likely."
                    )
        
        # Financial consequences
        penalty = financial.get('penalty_amount', 0)
        if penalty > 0:
            consequences["month_3_12"].append(
                f"If contract disputes arise, you face ₹{penalty:,.0f} in penalties and legal fees."
            )
        
        # Long-term
        if any('jurisdiction' in c.get('type', '').lower() for c in clauses if c.get('risk') == 'High'):
            consequences["long_term"].append(
                "Any legal dispute will cost ₹10-50 lakhs in foreign legal fees. Practically unwinnable."
            )
        
        # Worst case
        high_risk_types = [c.get('type') for c in clauses if c.get('risk') == 'High']
        if len(high_risk_types) >= 2:
            consequences["worst_case_scenario"] = (
                f"Combination of {', '.join(high_risk_types[:2])} clauses could lead to "
                f"business closure, bankruptcy, or ₹{penalty + 500000:,.0f}+ in total losses."
            )
        
        return consequences
    
    def _simulate_rejection_consequences(self, analysis: Dict) -> Dict:
        """
        What happens if you DON'T sign / walk away?
        """
        return {
            "short_term_impact": "Need to find alternative vendor/client. Could take 2-6 weeks.",
            "cost": "Time investment in new search. Possible delay in project/revenue.",
            "benefit": "Avoid massive legal and financial risks. Better to restart than sign dangerous contract.",
            "recommendation": "If they won't negotiate the critical issues, walking away is the smart business decision."
        }
    
    def _create_action_plan(self, verdict: str, clauses: List[Dict]) -> List[Dict]:
        """
        Step-by-step plan for what to do next.
        """
        if verdict == "SIGN":
            return [
                {"step": 1, "action": "Review one final time with stakeholders", "timeline": "Today"},
                {"step": 2, "action": "Sign and keep copy for records", "timeline": "Today"},
                {"step": 3, "action": "Set calendar reminders for key dates (renewal, termination notice deadlines)", "timeline": "This week"}
            ]
        
        elif verdict == "NEGOTIATE":
            high_risk_clauses = [c for c in clauses if c.get('risk') == 'High']
            
            return [
                {"step": 1, "action": f"Schedule call with other party. Topic: 'Concerns about {len(high_risk_clauses)} contract clauses'", "timeline": "Within 3 days"},
                {"step": 2, "action": "Send this report + list of required changes (see 'Must Negotiate' section)", "timeline": "Before call"},
                {"step": 3, "action": "In negotiation, focus on the 'Must Negotiate' clauses. Be firm but professional.", "timeline": "During call"},
                {"step": 4, "action": "If they agree to changes: Get revised draft and re-analyze it with this tool", "timeline": "Within 1 week"},
                {"step": 5, "action": "If they refuse to negotiate: Reconsider the partnership (see 'Consequences if Rejected')", "timeline": "Decision point"}
            ]
        
        else:  # REJECT
            return [
                {"step": 1, "action": "DO NOT SIGN this contract", "timeline": "Immediate", "critical": True},
                {"step": 2, "action": "Email them: 'After legal review, we need major revisions to proceed. Can we discuss?'", "timeline": "Today"},
                {"step": 3, "action": "If they're willing to rewrite the dangerous clauses completely: Request new draft", "timeline": "Within 3 days"},
                {"step": 4, "action": "If they refuse or push back: Start looking for alternative vendors/clients", "timeline": "Immediately"},
                {"step": 5, "action": "Remember: It's better to walk away than to sign a contract that could destroy your business", "timeline": "Always"}
            ]
    
    def _estimate_negotiation_timeline(self, verdict: str, high_risk: int) -> Dict:
        """How long will this take to resolve?"""
        
        if verdict == "SIGN":
            return {
                "estimate": "1-2 days",
                "explanation": "Quick final review and signing"
            }
        
        elif verdict == "NEGOTIATE":
            days = 7 + (high_risk * 3)  # More issues = longer negotiation
            return {
                "estimate": f"{days}-{days+7} days",
                "explanation": f"Negotiating {high_risk} major clause(s) + revisions + re-review"
            }
        
        else:  # REJECT
            return {
                "estimate": "2-6 weeks",
                "explanation": "If they agree to major rewrite: 2-3 weeks. If you find new vendor: 4-6 weeks"
            }
    
    def _assess_leverage(self, analysis: Dict) -> Dict:
        """
        How much negotiating power do you have?
        This helps SMEs understand their position.
        """
        
        # Simplified leverage assessment
        contract_type = analysis.get('contract_type', '')
        
        leverage_map = {
            "Vendor Contract": {
                "position": "Moderate",
                "reason": "As a vendor, you can negotiate but may have less power than client",
                "tips": "Focus on limiting liability and ensuring fair payment terms"
            },
            "Service Agreement": {
                "position": "Moderate-High",
                "reason": "Service contracts are typically more negotiable",
                "tips": "Push for mutual obligations and reasonable termination clauses"
            },
            "Employment Agreement": {
                "position": "Low-Moderate",
                "reason": "Employers usually have more leverage, but key clauses are negotiable",
                "tips": "Focus on non-compete scope, IP ownership, and notice periods"
            },
            "Lease Agreement": {
                "position": "Low",
                "reason": "Property owners typically have stronger position",
                "tips": "Negotiate on rent escalation, maintenance, and security deposit"
            }
        }
        
        return leverage_map.get(contract_type, {
            "position": "Moderate",
            "reason": "Most contract terms are negotiable for businesses",
            "tips": "Be professional but firm on critical safety clauses"
        })


# Convenience function
def make_decision(analysis_results: Dict) -> Dict:
    """
    Simple wrapper for external use.
    """
    engine = ContractDecisionEngine()
    return engine.generate_decision(analysis_results)
