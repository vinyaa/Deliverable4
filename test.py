#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from nose.plugins.skip import Skip, SkipTest
import unittest
import sys
import nose
import time

# Primary Test Center address
testcenter_url = 'https://testcenter.duolingo.com/'

# All of the supported languages in Test Center
languages = ("en", "es", "fr", "de", "it", "pt", "ru", "hi", "hu", "tr")

# Duolingo account credentials for the site. 
# Change them to the appropriate values, but don't check them in!
loginID = "maxtp"
loginPass = "rage$duo7"

# Command-line arguments for the browser and platform respectively
# Supported browsers: "internet explorer", "firefox", "safari", and "chrome"
# Supported platforms: MAC, VISTA, WIN8
browserName = sys.argv[1]
systemPlatform = sys.argv[2]

capabilities = {
  "browserName": browserName,
  "platform": systemPlatform,
}

# Setup a browser session for the chosen OS/browser combination
def setup_module():
    global driver
    driver = webdriver.Remote(desired_capabilities=capabilities)
    driver.implicitly_wait(30)
    driver.maximize_window()

# Make sure that the page title is the same for each language.
# This not only makes branding consistent, but is also a sanity
# check that a page renders for every supported language.
def check_page_title(language, testcenter_url, title):
    driver.get(testcenter_url + language)
    assert (driver.title == title)

# Generate an individual page title test for each language
# The title of each page should be "Duolingo Test Center"
def test_page_title():
    for language in languages:
        yield check_page_title, language, testcenter_url, "Duolingo Test Center"

# Generate tests to check that the primary action button is translated properly for the top 3 language markets
def test_action_button_translation():
    topLanguages = languages[0:3]
    messages = ("Try it while it's free", "Inténtelo mientras es gratis", "Essaie pendant que c'est gratuit")
    for topLanguage, message in zip(topLanguages, messages):
        yield check_action_button_translation, topLanguage, testcenter_url, message

# The actual test for the top 3 language translations
def check_action_button_translation(language, testcenter_url, message):
    driver.get(testcenter_url + language)
    buttonText = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[1]/div[1]/div/div').text.encode('utf8')
    assert (buttonText == message)

# Make sure that the users are taken to the Google play page and are presented the installation button for 
# the Test Center Android application
def test_android_app_link():
    driver.get(testcenter_url + 'en')
    androidLink = driver.find_element_by_xpath('//div[@id="app"]/section[1]/div[1]/div[1]/div[1]/div/ul/li[1]/a').get_attribute('href')
    driver.get(androidLink)
    installButton = driver.find_element_by_xpath('//*[@id="body-content"]/div[1]/div[1]/div[2]/div[4]/span/button/span[2]').text
    assert (installButton == "Install")

# Hover over the button labeled "Try it while it's free", click the link for the Test Center Chrome web application,
# If the browser is Chrome, an unauthenticated user should get a dialog to create an account
# If the browser is anything else, the user should be taken to a page where he/she can download Chrome
def test_chrome_app_link():
    # The web driver for Safari does not yet support the move_to_element method so this test will not function properly
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
def test_invalid_login():
    driver.get(testcenter_url + 'en')
    driver.find_element_by_id('sign-in-btn').click()
    usernameForm = driver.find_element_by_id('top_login')
    usernameForm.send_keys("alskdjlksjdlffei392j32hf2kd")
    passwordForm = driver.find_element_by_id('top_password')
    passwordForm.send_keys("alskdjlksjdlffei392j32hfdsdf2kd")
    driver.find_element_by_id('login-button').click()
    errorText = driver.find_element_by_xpath('/html/body/div[3]/div/div/p').text.strip()
    assert (errorText == "ERROR: Failed login")

# If the user clicks on the "Forgot password" link, the user should be redirected to a page where
# the password can be reset by providing an e-mail address
def test_forgotten_password():
    driver.get(testcenter_url + 'en')
    driver.find_element_by_id('sign-in-btn').click()
    driver.find_element_by_xpath('//*[@id="login-form"]/li[8]/a').click()

    # Make sure the user is redirected to the reset password page where they can type in their e-mail address
    try:
        driver.find_element_by_id('email')
        assert True
    except:
        assert False

# Login with a previously-known valid username and password
# After a sucessful login, the user should have a hover menu in the top right corner of the screen
# labeled with their username
def test_valid_login():
    driver.get(testcenter_url + 'en')
    driver.find_element_by_id('sign-in-btn').click()
    usernameForm = driver.find_element_by_id('top_login')
    usernameForm.send_keys(loginID)
    passwordForm = driver.find_element_by_id('top_password')
    passwordForm.send_keys(loginPass)
    driver.find_element_by_id('login-button').click()
    try:
        # Find the user's name in the top right corner of the page to indicate that the login was successful
        username = driver.find_element_by_class_name('name').text.strip().lower()
        assert (username == loginID.lower())
    except:
        assert False

# 
# Note that the following sequence of tests are only supported in the Chrome browser. 
# These tests will be skipped for other platforms
# 

# Make sure that the sample test button is available to authenticated Chrome users
def test_chrome_sample_test_visible():
    # This feature only works for the Chrome browser with a physical camera available
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    try:
        # Make sure the sample test option is available for a Chrome user
        sample_label = driver.find_element_by_class_name('sample-questions').text.strip()
        assert (sample_label == "Sample Questions")
    except:
        assert False

# Make sure that the certified test button is available to authenticated Chrome users
def test_chrome_certified_test_visible():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    try:
        # The certified test option should be available 
        driver.find_element_by_class_name('certified-exam')
        assert True
    except:
        assert False

# Clicking the sample questions button should start sample questions by redirecting to the "sample" page
def test_sample_questions_works():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    driver.get(testcenter_url)
    sample_button = driver.find_element_by_class_name("sample-questions").click()
    sample_url = driver.current_url
    assert (sample_url == "https://testcenter.duolingo.com/sample")

# Clicking quit button on the sample questions page should return the user to the main Test Center page
def test_quit_sample_splash():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    driver.get(testcenter_url + "sample")
    quit_button = driver.find_element_by_class_name("left")
    quit_button.click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)

# Clicking start button on the sample questions page starts the language listening challenge
def test_start_sample():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    driver.get(testcenter_url + "sample")
    start_button = driver.find_element_by_class_name("right")
    start_button.click()
    try: 
        driver.find_element_by_class_name("listen-challenge")
        assert True
    except:
        assert False

# During the listening challenge, the user types what is heard from a voice recording
# To test this module,  type "She is not old.", press enter, and advance to the speaking challenge
def test_listen_module():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    driver.get(testcenter_url + "sample")
    start_button = driver.find_element_by_class_name("right")
    start_button.click()
    listening = driver.find_element_by_xpath("//div[@id ='challenge']/div[1]/div[2]/input[1]")
    listening.send_keys("She is not old")
    listening.send_keys(Keys.RETURN)
    try:
        driver.find_element_by_class_name("speak-challenge")
        assert True
    except:
        assert False

# During the speaking challenge, the user is prompted to speak the phrase displayed on the screen
# To test this module,  click the  record-button, wait 2 seconds, click the stop button, and submit the answers
# This should take you to the next challenge: vocabulary selection
def test_speak_module():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    # Start recording voice
    mic = driver.find_element_by_id("record-button")
    mic.click()
    time.sleep(2)
    stop = driver.find_element_by_id("stop-button")
    stop.click()
    submit = driver.find_element_by_xpath("//footer/button[1]")
    submit.click()
    try:
        # Find a work on the vocab test (the next test) so that we know we have passed this one
        driver.find_element_by_xpath("//*[contains(.,'both')]")
        assert True
    except:
        assert False

# The user is asked to select the valid English words out of a set of labeled buttons
# To test this module, click the buttons that say [fine good easy bag walk both may], and click the submit button
def test_vocab_module():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    vocab_buttons = driver.find_elements_by_class_name("btn")
    vocab_options = ["fine", "good", "easy", "bag", "walk", "both", "may"]
    for button in vocab_buttons:
        my_text = button.text.strip()
        if my_text in vocab_options:
            button.click()
    submit = driver.find_element_by_xpath("//footer/button[1]")
    submit.click()

# The dropdown sentence selection challenge presents the user with an incomplete sentence and the user must select the most
# valid words for the particular context from a dropdown menu
# To test this module, select [has were was became swam] and submit. The next page should display "Sample questions complete!"
def test_dropdown_module():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    # Find all of the dropdown word selectors
    select_1 = driver.find_element_by_xpath('//*[@id="dropout-f84b22d51ba03e7c198a1dd22ad7a88e"]/p/label[1]/select')
    select_2 = driver.find_element_by_xpath('//*[@id="dropout-f84b22d51ba03e7c198a1dd22ad7a88e"]/p/label[2]/select')
    select_3 = driver.find_element_by_xpath('//*[@id="dropout-f84b22d51ba03e7c198a1dd22ad7a88e"]/p/label[3]/select')
    select_4 = driver.find_element_by_xpath('//*[@id="dropout-f84b22d51ba03e7c198a1dd22ad7a88e"]/p/label[4]/select')
    select_5 = driver.find_element_by_xpath('//*[@id="dropout-f84b22d51ba03e7c198a1dd22ad7a88e"]/p/label[5]/select')
    
    Select(select_1).select_by_value("has")
    Select(select_2).select_by_value("were")
    Select(select_3).select_by_value("was")
    Select(select_4).select_by_value("became")
    Select(select_5).select_by_value("swam")
    submit = driver.find_element_by_xpath("//footer/button[1]")
    submit.click()

    complete_message = driver.find_element_by_tag_name('h2').text.strip()
    expected_message = "Sample questions complete!"
    assert (complete_message == expected_message)

# Clicking the back to home button when the sample test is complete should return the user to the main Test Center page
def test_back_to_home():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    back_to_home = driver.find_element_by_class_name("left")
    back_to_home.click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)

# Clicking the take test button after the simple test is complete takes the user to the actual certification exam
def test_take_real_test():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    # Take the test all over again
    test_start_sample()
    test_listen_module()
    test_speak_module()
    test_vocab_module()
    test_dropdown_module()

    # Make sure we end up on the real test page
    real_test = driver.find_element_by_class_name("right")
    real_test.click()
    new_url = driver.current_url
    test_url = "https://testcenter.duolingo.com/test"
    assert (new_url == test_url)

# Clicking the quit button (the (X) in the upper-right corner of the page) during the sample exam, 
# and then clicking cancel returns the user to the sample questions
def test_quit_cancel():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    # Start exam
    test_start_sample()

    driver.find_element_by_class_name("leave-exam").click()
    # Click cancel to return to test
    driver.find_element_by_xpath("//button[2]").click()
    new_url = driver.current_url
    assert (new_url == testcenter_url + "sample")

# Clicking quit, then ok returns "You left this test". Click ok and return to testcenter_url and camera off
# Clicking the quit button during the sample exam, and then clicking ok displays "You left this test"
# to the user and redirects him/her to the main Test Center page
def test_quit_test():
    if (driver.capabilities['browserName'] != "chrome" or driver.capabilities['platform'] != "MAC"):
        raise SkipTest

    # Start exam
    test_start_sample()

    driver.find_element_by_class_name("leave-exam").click()
    # Click ok to quit
    driver.find_element_by_xpath("/html/body/div[3]/div/div/button[2]").click()
    # Click ok to leave test
    driver.find_element_by_xpath("/html/body/div[3]/div/div/button").click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)

# Make sure a user can properly logout of Testcenter by hovering over his/her username
# The user should be taken back to the Test Center front page
def test_logout():
    # The web driver for Safari does not yet support the move_to_element method so this test will not function properly
    if (driver.capabilities['browserName'] == "safari"):
        raise SkipTest

    driver.get(testcenter_url)
    username = driver.find_element_by_class_name('name')
    hoverButton = ActionChains(driver).move_to_element(username)
    hoverButton.perform()
    logoutButton = driver.find_element_by_id("header_userdrop_logout").click()
    # Look for text that is expected to be on the front page
    try:
        expectedText = driver.find_element_by_xpath('//*[@id="app"]/section[1]/div[1]/div[1]/div[1]/h1').text.strip()
        assert (expectedText == "Certify your language proficiency")
    except:
        assert False

# Close the browser session
def teardown_module():
    driver.quit()

if __name__ == "__main__":

    print "TESTING: " + browserName + " on " + systemPlatform
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

    # The unit testing framework takes over the command line arguments, so removing ours to not cause trouble
    del sys.argv[1:]

    nose.runmodule(argv=[__file__, '-v'])
