CLAUSE_TYPES = [
    "Termination",
    "Indemnity",
    "Limitation of Liability",
    "Intellectual Property",
    "Payment",
    "Confidentiality",
    "Governing Law",
    "Dispute Resolution",
    "Force Majeure",
    "Non-Compete",
    "Warranties",
    "Other"
]

RISK_KEYWORDS = {
    "High": [
        "sole discretion", 
        "unlimited liability", 
        "without notice", 
        "without cause",
        "penalty", 
        "liquidated damages",
        "indemnify and hold harmless",
        "unilateral termination",
        "entire agreement",
        "arbitration in london",
        "arbitration in singapore",
        "courts at new york",
        "courts in london",
        "exclusive jurisdiction of",
        "perpetual",
        "irrevocable",
        "waive all claims",
        "no liability cap",
        "unlimited indemnity",
        "intellectual property shall transfer",
        "ip shall vest in",
        "all rights shall belong to",
        "ownership of all work product"
    ],
    "Medium": [
        "may terminate", 
        "reasonable efforts", 
        "subject to",
        "automatically renew",
        "auto-renewal",
        "non-compete",
        "exclusivity",
        "stamp duty",
        "jurisdiction at delhi",
        "jurisdiction at mumbai",
        "as applicable",
        "from time to time",
        "best efforts",
        "lock-in period",
        "minimum term of",
        "shall not terminate for",
        "renews automatically unless",
        "evergreen clause"
    ],
}

# Detailed explanations for each risk keyword
RISK_EXPLANATIONS = {
    "High": {
        "sole discretion": "The other party can make decisions without consulting you. You have no say in critical matters affecting your business.",
        "unlimited liability": "You could be sued for ANY amount - even beyond the contract value. This could bankrupt your business.",
        "without notice": "The contract can be terminated immediately with no warning. You'll lose revenue overnight and have no time to prepare.",
        "without cause": "Termination can happen for any reason or no reason at all. Your business relationship has no stability.",
        "penalty": "You'll be charged extra fees beyond actual damages. These can be excessive and unfair.",
        "liquidated damages": "Pre-determined damages that may far exceed actual losses. Often used to trap small vendors.",
        "indemnify and hold harmless": "You must pay for all their losses, including their legal mistakes. Extremely risky for SMEs.",
        "unilateral termination": "Only one party can end the contract. You're locked in while they can leave anytime.",
        "entire agreement": "All prior discussions and promises are void. Only what's written in the contract counts - dangerous if you relied on verbal assurances.",
        "arbitration in london": "Disputes must be resolved in London, UK. Cost of flying there + foreign lawyers = ₹10-50 lakhs minimum.",
        "arbitration in singapore": "Singapore arbitration costs ₹15-60 lakhs. Impossible for most Indian SMEs to afford.",
        "courts at new york": "US court jurisdiction means US lawyers, US travel, US legal costs. Virtually impossible for small businesses.",
        "courts in london": "UK court means UK lawyers at £400-800/hour. Total cost could exceed your entire contract value.",
        "exclusive jurisdiction of": "You can ONLY sue in their chosen location. No option for your local courts.",
        "perpetual": "This clause lasts forever - even after the contract ends. Very difficult to escape.",
        "irrevocable": "Cannot be changed or cancelled, even if circumstances change drastically.",
        "waive all claims": "You're giving up your legal rights to sue for damages. Extremely dangerous.",
        "no liability cap": "Same as unlimited liability - they can be sued for infinite amounts.",
        "unlimited indemnity": "You must pay for ALL their losses without any limit. Could exceed your business's net worth.",
        "intellectual property shall transfer": "All IP you create (even using your own tools) transfers to them. You lose ownership of your work forever.",
        "ip shall vest in": "IP ownership automatically goes to them. You can't reuse anything you built, even your own code/designs.",
        "all rights shall belong to": "Complete transfer of all rights - you retain nothing. Extremely unfavorable for vendors/freelancers.",
        "ownership of all work product": "They own everything you create during the project. May prevent you from offering similar services to others."
    },
    "Medium": {
        "may terminate": "Gives termination rights but usually with some conditions. Check the notice period carefully.",
        "reasonable efforts": "Vague obligation - what's 'reasonable'? Can lead to disputes about whether you fulfilled your duties.",
        "subject to": "Creates conditional obligations. Make sure you understand what conditions apply.",
        "automatically renew": "Contract renews without your action. You might forget to cancel and be locked in for another term.",
        "auto-renewal": "Same as automatically renew. Set a calendar reminder before renewal date.",
        "non-compete": "Restricts your ability to work with competitors. Check the duration and geographic scope - is it reasonable?",
        "exclusivity": "You can ONLY work with this client/vendor. Limits your business growth opportunities.",
        "stamp duty": "You may have to pay registration taxes. In some states, this is 3-7% of contract value.",
        "jurisdiction at delhi": "All disputes go to Delhi courts. Fine if you're in Delhi, expensive if you're in Chennai or Guwahati.",
        "jurisdiction at mumbai": "Mumbai jurisdiction. Travel and legal costs add up if you're based elsewhere.",
        "as applicable": "Vague phrase - when does it apply and when doesn't it? Causes confusion later.",
        "from time to time": "Gives them right to change terms occasionally. How often? With what notice? Get clarity.",
        "best efforts": "Similar to 'reasonable efforts' - legally vague. What's 'best' for a small business vs. large corporation?",
        "lock-in period": "You cannot terminate for a fixed period (often 1-3 years). Trapped even if service is terrible or your needs change.",
        "minimum term of": "Similar to lock-in. You're committed for this period even if the relationship isn't working.",
        "shall not terminate for": "Prevents termination for a specified duration. Make sure it's reasonable (12 months max recommended).",
        "renews automatically unless": "Auto-renewal. You must actively cancel or you're locked in for another full term. Set calendar reminders!",
        "evergreen clause": "Contract continues indefinitely until someone cancels. Easy to forget and be locked in for years."
    }
}

# Standard safe clauses for comparison
STANDARD_CLAUSES = {
    "Termination": {
        "safe": "Either party may terminate this Agreement by providing 30 days' prior written notice to the other party. Upon termination, the Client shall pay for all services rendered up to the date of termination, and the Vendor shall return all Client materials within 7 days.",
        "description": "Mutual termination rights with notice period",
        "benefits": [
            "Reduces unilateral power (both parties have equal rights)",
            "Gives you 30 days to find new revenue sources",
            "Ensures you get paid for work already done"
        ]
    },
    "Indemnity": {
        "safe": "Each party agrees to indemnify the other only for direct damages caused by that party's gross negligence or willful misconduct. The total liability under this indemnity shall not exceed the total fees paid under this Agreement in the 12 months preceding the claim.",
        "description": "Capped, mutual indemnity for gross negligence only",
        "benefits": [
            "Protects you from infinite financial liability",
            "Limits responsibility to your own major mistakes only",
            "Prevents minor errors from bankrupting your business"
        ]
    },
    "Limitation of Liability": {
        "safe": "Neither party's total liability under this Agreement shall exceed the fees paid in the 12 months preceding the claim. Neither party shall be liable for indirect, consequential, or punitive damages.",
        "description": "Reasonable cap with exclusions for consequential damages",
        "benefits": [
            "Caps your maximum risk to a known amount (contract value)",
            "Protects you from massive 'consequential' logic damages",
            "Standardizes risk for both parties"
        ]
    },
    "Payment": {
        "safe": "The Client shall pay the Vendor within 30 days of receiving a valid invoice. Late payments shall incur interest at 1% per month. If payment is more than 60 days overdue, the Vendor may suspend services after written notice.",
        "description": "Standard 30-day payment terms with clear consequences",
        "benefits": [
            "Ensures predictable cash flow (Net 30)",
            "Gives you leverage to stop work if not paid",
            "Adds a penalty for late payments to encourage speed"
        ]
    },
    "Confidentiality": {
        "safe": "Both parties agree to keep all proprietary information confidential for the term of this Agreement and for 2 years thereafter. This does not apply to information that becomes publicly available or is independently developed.",
        "description": "Mutual confidentiality with time limit and standard exceptions",
        "benefits": [
            "Reduces perpetual liability (ends after 2 years)",
            "Protects your trade secrets too, not just theirs",
            "Clarifies that public info is not confidential"
        ]
    },
    "Governing Law": {
        "safe": "This Agreement shall be governed by the laws of India. Any disputes shall be subject to the jurisdiction of courts where the Defendant resides, or by mutual agreement, resolved through arbitration in accordance with the Arbitration and Conciliation Act, 1996.",
        "description": "Indian law with defendant-location jurisdiction (fair to both parties)",
        "benefits": [
            "Avoids expensive foreign courts (UK/US/Singapore)",
            "Ensures you are sued in your home city, not theirs",
            "Lowers legal defense costs significantly"
        ]
    },
    "Intellectual Property": {
        "safe": "All work product created specifically for this project shall be owned by the Client upon full payment. The Vendor retains ownership of all pre-existing IP and tools used to create the deliverables.",
        "description": "Client owns new work; Vendor keeps pre-existing tools/IP",
        "benefits": [
            "Prevents you from losing your core tools/libraries",
            "Conditioning ownership on 'full payment' protects your fees",
            "Clarifies exactly what they own vs. what you keep"
        ]
    },
    "Non-Compete": {
        "safe": "During the term of this Agreement, the Vendor shall not provide substantially similar services to direct competitors of the Client within the same city/region. This restriction does not apply after termination.",
        "description": "Limited non-compete during contract term only, reasonable geographic scope",
        "benefits": [
            "Allows you to work with others after the contract ends",
            "Limits restrictions to a specific location only",
            "Prevents them from blocking your entire livelihood"
        ]
    }
}

# Contract type detection keywords
CONTRACT_TYPE_KEYWORDS = {
    "Employment Agreement": [
        "employment agreement", "offer letter", "employee", "employer",
        "salary", "probation period", "annual leave", "resignation"
    ],
    "Lease Agreement": [
        "lease agreement", "rent agreement", "tenancy", "lessor", "lessee",
        "premises", "rent", "security deposit", "lease period"
    ],
    "Vendor Contract": [
        "vendor", "supplier", "purchase order", "delivery of goods",
        "service provider", "contractor", "subcontractor"
    ],
    "Partnership Deed": [
        "partnership deed", "partners", "profit sharing", "capital contribution",
        "partnership firm", "mutual agreement between partners"
    ],
    "Non-Disclosure Agreement (NDA)": [
        "non-disclosure", "confidentiality", "nda", "proprietary information",
        "confidential information", "trade secrets"
    ],
    "Service Agreement": [
        "service agreement", "services", "deliverables", "scope of work",
        "statement of work", "professional services"
    ]
}

# Ambiguous terms that need clarification
AMBIGUOUS_TERMS = [
    "reasonable",
    "best efforts",
    "as applicable",
    "from time to time",
    "subject to",
    "appropriate",
    "satisfactory",
    "promptly",
    "substantial",
    "material"
]
