#!/usr/bin/env python
from selenium import webdriver
import unittest
import sys
import nose

testcenter_url = 'http://testcenter.duolingo.com/'
languages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")

browserName = sys.argv[1]
systemPlatform = sys.argv[2]

capabilities = {
  "browserName": browserName,
  "platform": systemPlatform,
}

# Setup a browser session for the chosen OS/browser combination
def setUpModule():
    global driver
    driver = webdriver.Remote(desired_capabilities=capabilities)

def check_page_title(language, testcenter_url, title):
    driver.get(testcenter_url + language)
    assert (driver.title == "Duolingo Test Center")

def test_page_title():
    for language in languages:
        yield check_page_title, language, testcenter_url, "Duolingo Test Center"

# Check the welcome text for each language as a sanity check to make sure the page is internationalized for the particular
#def test_page_welcome(self):
#    languages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")
#    messages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")
#    for (language, message) in (languages, messages):
#        self.driver.get(testcenter_url + language)

#def test_example2(self):
#    self.driver.get("http://www.google.com")
#    self.assertEqual(self.driver.title, "Google")

def tearDownModule():
    driver.quit()

if __name__ == "__main__":

    print "TESTING: " + browserName + " on " + systemPlatform
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

    # The unit testing framework takes over the command line arguments, so removing ours to no cause trouble
    del sys.argv[1:]

    #unittest.main(verbosity=1)
    nose.runmodule(argv=[__file__, '-v'])
