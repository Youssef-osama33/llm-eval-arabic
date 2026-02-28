"""Unit tests for ArabicAnalyzer."""

import pytest
from app.services.arabic_analyzer import ArabicAnalyzer


@pytest.fixture
def analyzer():
    return ArabicAnalyzer()


class TestArabicRatio:
    def test_pure_arabic(self, analyzer):
        text = "مرحباً بالعالم العربي الجميل"
        result = analyzer.analyze(text)
        assert result["arabic_char_ratio"] > 0.7

    def test_pure_english(self, analyzer):
        text = "Hello world this is English text"
        result = analyzer.analyze(text)
        assert result["arabic_char_ratio"] < 0.1

    def test_mixed_text(self, analyzer):
        text = "The model (النموذج) uses deep learning (تعلم عميق)"
        result = analyzer.analyze(text)
        assert 0.1 < result["arabic_char_ratio"] < 0.9

    def test_empty_text(self, analyzer):
        result = analyzer.analyze("")
        assert result["arabic_char_ratio"] == 0.0
        assert result["token_count"] == 0


class TestDialectDetection:
    def test_gulf_detection(self, analyzer):
        text = "وش رأيك في هذا الموضوع؟ وايد زين"
        result = analyzer.analyze(text)
        assert result["detected_dialect"] == "gulf"

    def test_egyptian_detection(self, analyzer):
        text = "إيه رأيك في ده؟ ده موضوع كويس"
        result = analyzer.analyze(text)
        assert result["detected_dialect"] == "egyptian"

    def test_levantine_detection(self, analyzer):
        text = "شو رأيك بهيك موضوع؟ هلق رح نبدأ"
        result = analyzer.analyze(text)
        assert result["detected_dialect"] == "levantine"

    def test_msa_default(self, analyzer):
        text = "إن الذكاء الاصطناعي يمثل ثورة تقنية حقيقية"
        result = analyzer.analyze(text)
        assert result["detected_dialect"] == "msa"


class TestTechnicalTerms:
    def test_finds_technical_terms(self, analyzer):
        text = "تعتمد خوارزمية التعلم الآلي على شبكة عصبية متعددة الطبقات"
        result = analyzer.analyze(text)
        assert result["technical_term_count"] >= 2

    def test_no_technical_terms(self, analyzer):
        text = "ذهبت إلى السوق واشتريت تفاحاً وبرتقالاً"
        result = analyzer.analyze(text)
        assert result["technical_term_count"] == 0


class TestSentenceMetrics:
    def test_sentence_count(self, analyzer):
        text = "هذه جملة أولى. وهذه جملة ثانية. وهذه جملة ثالثة."
        result = analyzer.analyze(text)
        assert result["sentence_count"] >= 2

    def test_unique_word_ratio(self, analyzer):
        # Repeated words → low ratio
        text = "كلمة كلمة كلمة كلمة كلمة كلمة"
        result = analyzer.analyze(text)
        assert result["unique_word_ratio"] < 0.3
