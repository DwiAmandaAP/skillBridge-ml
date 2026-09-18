import re
import logging
from services.preprocessing import clean_text
from services.taxonomy import taxonomy
from services.fallback_skills import get_fallback_skills

logger = logging.getLogger("skill_matcher")


def extract_skills_from_text(text: str, title: str = "") -> list[str]:
    """
    1. Coba exact/substring match terhadap taxonomy (nama + alias).
    2. Kalau tidak ketemu sama sekali, pakai fallback dictionary
       berdasarkan title (sesuai keputusan: manual rule, bukan algoritma).
    """
    matched_codes = _match_against_taxonomy(text)

    if not matched_codes:
        fallback = get_fallback_skills(title)
        if fallback:
            logger.info(f"Fallback dipakai untuk title='{title}' -> {fallback}")
            return fallback
        else:
            logger.info(f"Tidak ada match sama sekali (taxonomy maupun fallback) untuk title='{title}'")

    return matched_codes


def _match_against_taxonomy(text: str) -> list[str]:
    cleaned = clean_text(text)
    matched_codes: set[str] = set()

    terms_sorted = taxonomy.get_all_terms_sorted_by_length()

    for term, code in terms_sorted:
        if code in matched_codes:
            continue  # skill ini sudah ketemu lewat term/alias lain

        if _contains_term(cleaned, term):
            matched_codes.add(code)

    return sorted(matched_codes)


def _contains_term(text: str, term: str) -> bool:
    """
    Whole-word/whole-phrase match memakai word boundary regex, supaya
    'r' tidak match ke tengah kata 'developer', tapi tetap match term
    yang punya simbol seperti 'c#', 'node.js', 'c++'.
    """
    escaped = re.escape(term)
    pattern = r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])"

    return bool(re.search(pattern, text))