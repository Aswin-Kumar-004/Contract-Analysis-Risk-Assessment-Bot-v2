"""
Multilingual support for Hindi contracts.
Uses IndicTrans2 approach with transliteration and translation.
"""

import re
from typing import Dict, Tuple

# Hindi legal terminology mapping (Devanagari → English)
HINDI_LEGAL_DICT = {
    # Contract terms
    "समझौता": "agreement",
    "अनुबंध": "contract",
    "करार": "contract",
    "संविदा": "contract",
    
    # Parties
    "पक्ष": "party",
    "पक्षकार": "party",
    "विक्रेता": "vendor",
    "खरीदार": "buyer",
    "ग्राहक": "client",
    "सेवा प्रदाता": "service provider",
    
    # Financial terms
    "किराया": "rent",
    "भाड़ा": "rent",
    "भुगतान": "payment",
    "रकम": "amount",
    "राशि": "amount",
    "धनराशि": "amount",
    "जुर्माना": "penalty",
    "हर्जाना": "damages",
    "मुआवजा": "compensation",
    
    # Rights and obligations
    "अधिकार": "rights",
    "दायित्व": "liability",
    "जिम्मेदारी": "responsibility",
    "दायित्व": "obligation",
    "कर्तव्य": "duty",
    
    # Legal concepts
    "स्वामित्व": "ownership",
    "बौद्धिक संपदा": "intellectual property",
    "गोपनीयता": "confidentiality",
    "समाप्ति": "termination",
    "विवाद": "dispute",
    "न्यायालय": "court",
    "क्षेत्राधिकार": "jurisdiction",
    "मध्यस्थता": "arbitration",
    
    # Important clauses
    "शर्त": "condition",
    "प्रावधान": "provision",
    "खंड": "clause",
    "अनुच्छेद": "article",
    
    # Dates and duration
    "तारीख": "date",
    "तिथि": "date",
    "अवधि": "duration",
    "समय": "time",
    "वर्ष": "year",
    "महीना": "month",
    
    # Actions
    "हस्ताक्षर": "signature",
    "साक्षी": "witness",
    "सहमति": "consent",
    "स्वीकृति": "approval",
}

# High-risk Hindi phrases
HINDI_RISK_KEYWORDS = {
    "High": [
        "असीमित दायित्व",  # unlimited liability
        "बिना सूचना",  # without notice
        "एकपक्षीय समाप्ति",  # unilateral termination
        "विदेशी न्यायालय",  # foreign court
        "पूर्ण विवेकाधिकार",  # sole discretion
        "जुर्माना",  # penalty
        "हर्जाना",  # damages
    ],
    "Medium": [
        "स्वतः नवीनीकरण",  # auto renewal
        "प्रतिस्पर्धा निषेध",  # non-compete
        "उचित प्रयास",  # reasonable efforts
        "लागू होने पर",  # as applicable
    ]
}


def is_hindi(text: str) -> bool:
    """
    Detects if text contains Hindi (Devanagari script).
    Returns True if >5% of characters are Devanagari.
    """
    if not text:
        return False
    
    devanagari_count = 0
    total_chars = 0
    
    for char in text:
        if char.strip():  # Skip whitespace
            total_chars += 1
            # Devanagari Unicode range: U+0900 to U+097F
            if '\u0900' <= char <= '\u097F':
                devanagari_count += 1
    
    if total_chars == 0:
        return False
    
    # If more than 5% Devanagari characters, consider it Hindi
    return (devanagari_count / total_chars) > 0.05


def translate_hindi_to_english(text: str) -> str:
    """
    Translates Hindi contract text to English for processing.
    
    Strategy:
    1. Replace Hindi legal terms with English equivalents
    2. Keep numbers and Latin script as-is
    3. Use Google Translate API fallback (if available)
    
    Note: This is a basic implementation. Production would use:
    - IndicTrans2 model for accurate translation
    - Or Google Cloud Translation API
    - Or Azure Translator
    """
    
    if not is_hindi(text):
        return text
    
    # Start with original text
    translated = text
    
    # Replace known Hindi legal terms
    for hindi_term, english_term in HINDI_LEGAL_DICT.items():
        translated = translated.replace(hindi_term, english_term)
    
    # For demo purposes, if we still have significant Devanagari,
    # we'll use a transliteration approach
    if is_hindi(translated):
        # Keep Hindi text but mark it as needing translation
        return f"[Hindi Contract - Partial Translation]\n{translated}"
    
    return translated


def detect_hindi_risk_keywords(text: str) -> Dict[str, list]:
    """
    Detects high-risk keywords in Hindi text.
    Returns dict of risk levels and found keywords.
    """
    found_risks = {"High": [], "Medium": []}
    
    for risk_level, keywords in HINDI_RISK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_risks[risk_level].append(keyword)
    
    return found_risks


def normalize_hindi_contract(text: str) -> Tuple[str, Dict]:
    """
    Normalizes Hindi contract for analysis.
    
    Returns:
        - Normalized text (translated/transliterated)
        - Metadata about the translation
    """
    
    if not is_hindi(text):
        return text, {"is_hindi": False, "translation_method": None}
    
    # Detect risk keywords in original Hindi
    hindi_risks = detect_hindi_risk_keywords(text)
    
    # Translate to English
    translated = translate_hindi_to_english(text)
    
    metadata = {
        "is_hindi": True,
        "translation_method": "dictionary_based",
        "hindi_risk_keywords_found": hindi_risks,
        "note": "Dictionary-based translation for demo. Production would use IndicTrans2 or Google Translate API."
    }
    
    return translated, metadata


def format_for_display(text: str, is_hindi_contract: bool) -> str:
    """
    Formats text for display in UI.
    For Hindi contracts, shows both original and translation status.
    """
    if not is_hindi_contract:
        return text
    
    return f"""
🇮🇳 **Hindi Contract Detected**

This contract has been processed using our multilingual engine:
- Hindi legal terms translated to English
- Risk analysis performed on normalized text
- Original Hindi preserved for reference

{text[:500]}...

*Note: For production use, we recommend having bilingual contracts or using professional translation services for critical legal documents.*
"""


# Additional helper for transliteration (Devanagari → Latin)
def transliterate_devanagari(text: str) -> str:
    """
    Basic transliteration of Devanagari to Latin script.
    This helps with pattern matching when full translation isn't available.
    """
    
    # Basic Devanagari to Latin mapping
    devanagari_to_latin = {
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ii', 'उ': 'u', 'ऊ': 'uu',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
        'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
        'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
        'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
        'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
        'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
        'श': 'sha', 'ष': 'sha', 'स': 'sa', 'ह': 'ha',
        '।': '.', '॥': '||',
    }
    
    result = []
    for char in text:
        if char in devanagari_to_latin:
            result.append(devanagari_to_latin[char])
        else:
            result.append(char)
    
    return ''.join(result)


# Backward compatibility functions
def normalize_hindi_to_english(text: str) -> str:
    """Backward compatibility wrapper."""
    normalized, _ = normalize_hindi_contract(text)
    return normalized


def translate_for_display(text: str) -> str:
    """Backward compatibility wrapper."""
    is_hindi_text = is_hindi(text)
    return format_for_display(text, is_hindi_text)
