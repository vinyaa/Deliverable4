#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose.plugins.skip import Skip, SkipTest
import unittest
import sys
import nose
import time

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
    driver.implicitly_wait(30)
    driver.maximize_window()

# Make sure that the page title is the same for each language.
# This not only makes branding consistent, but is also a sanity
# check that a page renders for every language.
def check_page_title(language, testcenter_url, title):
    driver.get(testcenter_url + language)
    assert (driver.title == title)

# Generate an individual page title test for each language
def test_page_title():
    for language in languages:
        yield check_page_title, language, testcenter_url, "Duolingo Test Center"

# Make sure that the primary action button is translated properly for the top 3 language markets
def test_action_button_translation():
    topLanguages = languages[0:3]
    messages = ("Try it while it's free", "Inténtelo mientras es gratis", "Essaie pendant que c'est gratuit")
    for topLanguage, message in zip(topLanguages, messages):
        yield check_action_button_translation, topLanguage, testcenter_url, message

def check_action_button_translation(language, testcenter_url, message):
    driver.get(testcenter_url + language)
    buttonText = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[1]/div[1]/div/div').text.encode('utf8')
    assert (buttonText == message)

# Make sure that the users are taken to the Google play page and are presented the installation for the Testcenter app
def test_android_app_link():
    driver.get(testcenter_url + 'en')
    androidLink = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[1]/div[1]/div/ul/li[1]/a').get_attribute('href')
    driver.get(androidLink)
    installButton = driver.find_element_by_xpath('//*[@id="body-content"]/div[1]/div[1]/div[2]/div[4]/span/button/span[2]').text
    assert (installButton == "Install")

def test_chrome_app_link():

    # The web driver for Safari does not yet support the move_to_element method
    if (driver.capabilities['browserName'] == "safari"):
        raise SkipTest

    driver.get(testcenter_url + 'en')
    button = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[1]/div[1]/div/div')
    hoverButton = ActionChains(driver).move_to_element(button)
    hoverButton.perform()
    loginBox = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[2]/p')
    chromeLink = driver.find_element_by_css_selector('.start-chrome')
    wait = WebDriverWait(driver, 30)
    wait.until(EC.visibility_of(chromeLink))
    if chromeLink.is_displayed():
        chromeLink.click()

    # Users are redirected to a user creation page if they are not currently logged in when using Chrome
    # If they are using other browsers, they are redirected to a Chrome download page
    if driver.capabilities['browserName'] == 'chrome':
        wait = WebDriverWait(driver, 30)
        wait.until(EC.visibility_of(loginBox))
        loginText = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[2]/p').text.strip()
        assert (loginText == "You need a Duolingo account to save your test results.")
    else:
        try:
            elem = driver.find_element_by_xpath("//*[contains(.,'Download Chrome')]")
            assert True
        except:
            assert False

# Make sure the user gets an error message when trying to login with an invalid user account
def testInvalidLogin():
    driver.get(testcenter_url + 'en')
    driver.find_element_by_id('sign-in-btn').click()
    usernameForm = driver.find_element_by_id('top_login')
    usernameForm.send_keys("alskdjlksjdlffei392j32hf2kd")
    passwordForm = driver.find_element_by_id('top_password')
    passwordForm.send_keys("alskdjlksjdlffei392j32hfdsdf2kd")
    driver.find_element_by_id('login-button').click()

    errorText = driver.find_element_by_xpath('/html/body/div[3]/div/div/p').text.strip()
    assert (errorText == "ERROR: Failed login")

def tearDownModule():
    driver.quit()

if __name__ == "__main__":

    print "TESTING: " + browserName + " on " + systemPlatform
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

    # The unit testing framework takes over the command line arguments, so removing ours to no cause trouble
    del sys.argv[1:]

    nose.runmodule(argv=[__file__, '-v'])
