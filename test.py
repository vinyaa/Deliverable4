#!/usr/bin/env python
from selenium import webdriver
import unittest
import sys

testcenter_url = 'http://testcenter.duolingo.com/'
languages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")

def test_page_title():
    for language in languages:
        yield check_page_title, language, testcenter_url, "Duolingo Test Center"

def check_page_title(language, testcenter_url, title):
    pass

    #@unittest.skipIf(1 == 1, "skipped")
class CheckFrontPage(unittest.TestCase):

    # Default browser capabilities
    capabilities = { "browserName": "chrome", "platform": "VISTA" }

    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities)

    # Make sure the title of the site stays the same regardless of language. This is required for proper branding.
    def test_page_title(self):
        for language in languages:
            self.driver.get(testcenter_url + language)
            self.assertEqual(self.driver.title, "Duolingo Test Center")

    # Check the welcome text for each language as a sanity check to make sure the page is internationalized for the particular
    #def test_page_welcome(self):
    #    languages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")
    #    messages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")
    #    for (language, message) in (languages, messages):
    #        self.driver.get(testcenter_url + language)

    #def test_example2(self):
    #    self.driver.get("http://www.google.com")
    #    self.assertEqual(self.driver.title, "Google")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    CheckFrontPage.capabilities = {
      "browserName": sys.argv[1],
      "platform": sys.argv[2],
    }

    # The unit testing framework takes over the command line arguments, so removing ours to no cause trouble
    del sys.argv[1:]

    unittest.main(verbosity=1)
