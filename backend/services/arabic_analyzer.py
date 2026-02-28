"""
ArabicAnalyzer — Lightweight Arabic NLP analysis.
Works without CAMeL Tools installed; falls back to regex heuristics.
Provides: arabic ratio, dialect detection, formal/colloquial markers,
          technical term detection, sentence metrics.
"""

import re
from typing import Optional


# ── Arabic Unicode range ───────────────────────────────────
ARABIC_PATTERN = re.compile(r"[\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufeef]")

# ── Dialect keyword sets ───────────────────────────────────
DIALECT_MARKERS: dict[str, list[str]] = {
    "gulf": ["وش", "شلون", "ليش", "حاطط", "يبي", "وايد", "زين", "عاد", "هي", "اهواي"],
    "egyptian": ["إيه", "ازيك", "ده", "دي", "بتاع", "بتاعت", "عامل", "كويس", "صح", "يعني"],
    "levantine": ["شو", "كيفك", "هيك", "هلق", "رح", "عم", "متل", "لأ", "مش", "بدي"],
    "maghrebi": ["واش", "كيفاش", "بصح", "ديما", "بزاف", "نتا", "هو", "راه", "باه"],
    "iraqi": ["شكو", "ماكو", "هواية", "عدنا", "گلبي", "پاشا", "لو", "سدير"],
}

# ── Technical Arabic terms ────────────────────────────────
TECHNICAL_TERMS = [
    "خوارزمية", "تعلم آلي", "شبكة عصبية", "بيانات ضخمة",
    "ذكاء اصطناعي", "برمجة", "قاعدة بيانات", "واجهة برمجة",
    "حوسبة سحابية", "أمن معلومات", "تشفير", "معالجة لغة",
    "رؤية حاسوبية", "نموذج لغوي", "محول", "انتباه",
    "نقل تعلم", "ضبط دقيق", "بيانات التدريب",
]

# ── Formal Arabic markers ─────────────────────────────────
FORMAL_MARKERS = [
    "إن", "إذ", "حيث", "غير أن", "بيد أن",
    "علاوة على", "فضلاً عن", "ثمة", "لذلك", "وعليه",
    "مما يستوجب", "في ضوء", "استناداً",
]

SENTENCE_ENDINGS = re.compile(r"[.!?؟.،\n]+")


class ArabicAnalyzer:
    """
    Analyze Arabic text for linguistic quality metrics.
    All methods are synchronous and pure-Python for reliability.
    """

    def analyze(self, text: str, dialect: str = "msa") -> dict:
        """
        Return a full analysis dict for the given Arabic text.

        Args:
            text: The model response text.
            dialect: The expected dialect (for adherence scoring).

        Returns:
            A dict of linguistic metrics.
        """
        if not text or not text.strip():
            return self._empty()

        tokens = self._tokenize(text)
        sentences = self._split_sentences(text)
        detected = self._detect_dialect(text)

        return {
            "token_count": len(tokens),
            "arabic_token_count": sum(1 for t in tokens if self._is_arabic(t)),
            "arabic_char_ratio": self._arabic_ratio(text),
            "detected_dialect": detected,
            "dialect_match": detected == dialect or detected == "msa",
            "sentence_count": len(sentences),
            "avg_sentence_length_tokens": (
                len(tokens) / len(sentences) if sentences else 0
            ),
            "formal_marker_count": self._count_markers(text, FORMAL_MARKERS),
            "technical_term_count": self._count_markers(text, TECHNICAL_TERMS),
            "unique_word_ratio": (
                len(set(tokens)) / len(tokens) if tokens else 0
            ),
        }

    # ── Private helpers ────────────────────────────────────

    def _is_arabic(self, token: str) -> bool:
        return bool(ARABIC_PATTERN.search(token))

    def _arabic_ratio(self, text: str) -> float:
        chars = [c for c in text if not c.isspace()]
        if not chars:
            return 0.0
        arabic_count = sum(1 for c in chars if ARABIC_PATTERN.match(c))
        return round(arabic_count / len(chars), 3)

    def _tokenize(self, text: str) -> list[str]:
        return re.findall(r"[\u0600-\u06ff\w]+", text)

    def _split_sentences(self, text: str) -> list[str]:
        parts = SENTENCE_ENDINGS.split(text)
        return [p.strip() for p in parts if p.strip()]

    def _detect_dialect(self, text: str) -> str:
        scores: dict[str, int] = {d: 0 for d in DIALECT_MARKERS}
        lower = text.lower()
        for dialect, markers in DIALECT_MARKERS.items():
            for marker in markers:
                if marker in lower:
                    scores[dialect] += 1
        best_dialect = max(scores, key=scores.get)
        return best_dialect if scores[best_dialect] > 0 else "msa"

    def _count_markers(self, text: str, markers: list[str]) -> int:
        count = 0
        lower = text.lower()
        for m in markers:
            if m in lower:
                count += 1
        return count

    def _empty(self) -> dict:
        return {
            "token_count": 0,
            "arabic_token_count": 0,
            "arabic_char_ratio": 0.0,
            "detected_dialect": "unknown",
            "dialect_match": False,
            "sentence_count": 0,
            "avg_sentence_length_tokens": 0.0,
            "formal_marker_count": 0,
            "technical_term_count": 0,
            "unique_word_ratio": 0.0,
        }


# Module-level singleton
arabic_analyzer = ArabicAnalyzer()
