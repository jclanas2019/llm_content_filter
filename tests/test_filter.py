# tests/test_filter.py

import unittest
from llm_content_filter.filter import LLMContentFilter

class TestLLMContentFilter(unittest.TestCase):

    def setUp(self):
        """Set up a default LLMContentFilter instance for use in tests."""
        self.default_filter = LLMContentFilter()
        self.custom_filter = LLMContentFilter(
            banned_words=["spam", "scam"],
            banned_words_file=None
        )
    
    def test_is_appropriate_default_words(self):
        """Test the is_appropriate method with default banned words."""
        self.assertTrue(self.default_filter.is_appropriate("This is a friendly text"))
        self.assertFalse(self.default_filter.is_appropriate("This text promotes violence"))
        self.assertFalse(self.default_filter.is_appropriate("This text contains hate speech"))
    
    def test_is_appropriate_custom_words(self):
        """Test the is_appropriate method with custom banned words."""
        self.assertTrue(self.custom_filter.is_appropriate("This is a friendly text"))
        self.assertFalse(self.custom_filter.is_appropriate("This text is a scam"))
        self.assertFalse(self.custom_filter.is_appropriate("This text is full of spam"))

    def test_filter_text_default_replacement(self):
        """Test the filter_text method with default replacement."""
        self.assertEqual(self.default_filter.filter_text("This text promotes violence"), "this text promotes [REDACTED]")
        self.assertEqual(self.default_filter.filter_text("This is a friendly text"), "this is a friendly text")

    def test_filter_text_custom_replacement(self):
        """Test the filter_text method with a custom replacement."""
        self.assertEqual(self.custom_filter.filter_text("This text is a scam", replacement="[CENSORED]"), "this text is a [CENSORED]")
        self.assertEqual(self.custom_filter.filter_text("This is spam", replacement="[CENSORED]"), "this is [CENSORED]")

    def test_synonyms_handling(self):
        """Test the is_appropriate and filter_text methods with synonyms."""
        filter_with_synonyms = LLMContentFilter(banned_words_file="custom_banned_words.json")
        self.assertFalse(filter_with_synonyms.is_appropriate("This text is full of brutality"))
        self.assertEqual(filter_with_synonyms.filter_text("This text contains aggression"), "this text contains [REDACTED]")

    def test_load_banned_words_from_file(self):
        """Test loading banned words from a JSON file."""
        filter_from_file = LLMContentFilter(banned_words_file="custom_banned_words.json")
        self.assertFalse(filter_from_file.is_appropriate("This text promotes violence"))
        self.assertFalse(filter_from_file.is_appropriate("This text is offensive"))

    def test_save_banned_words_to_file(self):
        """Test saving banned words to a JSON file."""
        self.custom_filter.save_banned_words_to_file("test_banned_words.json")
        # Load the saved file and test
        filter_loaded = LLMContentFilter(banned_words_file="test_banned_words.json")
        self.assertFalse(filter_loaded.is_appropriate("This text is a scam"))
        self.assertTrue(filter_loaded.is_appropriate("This is a friendly text"))
    
    def test_normalize_text(self):
        """Test the text normalization to handle accents and special characters."""
        self.assertTrue(self.default_filter.is_appropriate("This is a friendly text"))
        self.assertFalse(self.default_filter.is_appropriate("This text promotes violénce"))  # Testing accent handling

if __name__ == "__main__":
    unittest.main()
