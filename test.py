#!/usr/bin/env python
from selenium import webdriver
import unittest
import sys

class CheckFrontPage(unittest.TestCase):

    # Default browser capabilities
    capabilities = { "browserName": "chrome", "platform": "VISTA" }

    def setUp(self):
        self.driver = webdriver.Remote(desired_capabilities=self.capabilities)

    def test_example(self):
        self.driver.get("http://testcenter.duolingo.com")
        self.assertEqual(self.driver.title, "Duolingo Test Center")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    CheckFrontPage.capabilities = {
      "browserName": sys.argv[1],
      "platform": sys.argv[2],
    }

    # The unit testing framework takes over the command line arguments, so removing ours to no cause trouble
    del sys.argv[1:]

    unittest.main()
