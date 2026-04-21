import pytest
from app.core.intent import Intent, classify

@pytest.mark.parametrize("text,expected", [
    ("Hello there", Intent.CASUAL),
    ("Hi", Intent.CASUAL),
    ("Tell me about coding courses", Intent.COURSE_QUERY),
    ("What are the fees for AI?", Intent.COURSE_QUERY),
    ("How much is it?", Intent.COURSE_QUERY),
    ("I want to enroll", Intent.LEAD_CAPTURE),
    ("Help me join", Intent.LEAD_CAPTURE),
    ("What is the job outlook?", Intent.CAREER_QUERY),
    ("Will I get a job?", Intent.CAREER_QUERY),
    ("What is nova?", Intent.DOUBT),
    ("safasfgsg", Intent.FALLBACK)
])
def test_intent_classification(text, expected):
    assert classify(text) == expected
