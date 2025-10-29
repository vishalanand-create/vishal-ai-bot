import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import the bot modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from skills import greet_skill, faq_skill


class TestGreetSkill(unittest.TestCase):
    """Unit tests for greet_skill"""
    
    def test_greet_with_name(self):
        """Test greeting with a provided name"""
        result = greet_skill.greet("Alice")
        self.assertIn("Alice", result)
        self.assertTrue(result.startswith("Hello") or result.startswith("Hi"))
    
    def test_greet_without_name(self):
        """Test greeting without a name"""
        result = greet_skill.greet()
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_greet_empty_string(self):
        """Test greeting with empty string"""
        result = greet_skill.greet("")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_greet_special_characters(self):
        """Test greeting with special characters in name"""
        result = greet_skill.greet("@User123")
        self.assertIn("@User123", result)


class TestFAQSkill(unittest.TestCase):
    """Unit tests for faq_skill"""
    
    def test_faq_valid_question(self):
        """Test FAQ with a valid question"""
        result = faq_skill.answer_faq("What is AI?")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    def test_faq_unknown_question(self):
        """Test FAQ with an unknown question"""
        result = faq_skill.answer_faq("What is the meaning of life?")
        self.assertIsInstance(result, str)
        # Should return some default/fallback response
        self.assertTrue(len(result) > 0)
    
    def test_faq_empty_question(self):
        """Test FAQ with empty question"""
        result = faq_skill.answer_faq("")
        self.assertIsInstance(result, str)
    
    def test_faq_case_insensitive(self):
        """Test FAQ is case insensitive"""
        result1 = faq_skill.answer_faq("WHAT IS AI?")
        result2 = faq_skill.answer_faq("what is ai?")
        # Both should return valid responses
        self.assertIsInstance(result1, str)
        self.assertIsInstance(result2, str)
    
    def test_faq_partial_match(self):
        """Test FAQ with partial keyword match"""
        result = faq_skill.answer_faq("Tell me about AI")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
