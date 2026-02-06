import re

def segment_clauses(text):
    """
    Segments contract text into clauses based on legal numbering and formatting.
    Heuristic: Looks for patterns like "1.", "1.1.", "(a)", or double newlines.
    """
    # Regex for common legal numbering: 1., 1.1, (a), (i), [1], Article I
    clause_pattern = r"(?:\n\s*\(?[a-zA-Z0-9]+\)[\.\)]|\n\s*\d+\.\d+|\n\s*ARTICLE\s+[IVX]+|\n\s*SECTION\s+\d+)"
    
    # Split pattern but keep delimiters to reattach them
    chunks = re.split(f"({clause_pattern})", text)
    
    clauses = []
    current_clause = ""

    for chunk in chunks:
        if not chunk.strip():
            continue
            
        # If it looks like a new clause start, save the previous one and start new
        if re.match(clause_pattern, "\n" + chunk.strip()): # minor hack to match our pattern
             if current_clause:
                 clauses.append(current_clause.strip())
             current_clause = chunk
        else:
             current_clause += chunk

    if current_clause:
        clauses.append(current_clause.strip())
        
    # Fallback: if fewer than 3 clauses detected, might be bad formatting. 
    # Use simple paragraph/sentence splitting.
    if len(clauses) < 3:
        # Regex to split by sentence boundaries (approximate)
        # Matches period/question/exclamation followed by space and capital letter or newline
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\s*\n'
        raw_sentences = re.split(sentence_pattern, text)
        
        current_chunk = ""
        for sent in raw_sentences:
            current_chunk += sent + " "
            # Group into chunks of ~80 words
            if len(current_chunk.split()) >= 80:
                clauses.append(current_chunk.strip())
                current_chunk = ""
        if current_chunk.strip():
            clauses.append(current_chunk.strip())

    return clauses
