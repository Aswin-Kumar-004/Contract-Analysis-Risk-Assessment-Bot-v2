AMBIGUOUS_TERMS = [
    "reasonable",
    "best efforts",
    "as applicable",
    "from time to time",
    "subject to"
]

def detect_ambiguity(clause):
    found = []
    clause_lower = clause.lower()

    for term in AMBIGUOUS_TERMS:
        if term in clause_lower:
            found.append(term)

    return found
