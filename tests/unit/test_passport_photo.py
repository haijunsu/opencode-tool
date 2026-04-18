import unittest
from unittest.mock import patch
import os

from opencode_tool.passport_photo import PHOTO_PROFILES, generate_passport_photo, create_print_layout, check_dependencies

class TestPassportPhoto(unittest.TestCase):
    def test_profiles_defined(self):
        """Test that the core profiles are defined."""
        self.assertIn('cn_passport', PHOTO_PROFILES)
        self.assertIn('us_passport', PHOTO_PROFILES)
        self.assertIn('us_visa', PHOTO_PROFILES)
        
    def test_invalid_profile(self):
        """Test that generating a photo with an invalid profile fails."""
        with self.assertRaises(SystemExit):
            generate_passport_photo("dummy.jpg", "dummy_out.jpg", profile_type='invalid_profile')
            
    def test_invalid_layout_profile(self):
        """Test that layout generation fails gracefully with an invalid profile."""
        with self.assertRaises(SystemExit):
            create_print_layout("dummy.jpg", "dummy_out.jpg", profile_type='invalid_profile')

if __name__ == '__main__':
    unittest.main()
