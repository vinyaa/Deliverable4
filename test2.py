from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import sys
import time

global testcenter_url
testcenter_url = "https://testcenter.duolingo.com/"
loginID = "maxtp"
loginPass = "rage$duolingo"

class DuolingoTestCase(unittest.TestCase):
    
    def setUp(self):
        global driver
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.maximize_window()
        
    def test_valid_login(self):
        driver.get(testcenter_url + 'en')
        driver.find_element_by_id('sign-in-btn').click()
        usernameForm = driver.find_element_by_id('top_login')
        usernameForm.send_keys(loginID)
        passwordForm = driver.find_element_by_id('top_password')
        passwordForm.send_keys(loginPass)
        driver.find_element_by_id('login-button').click()
        
        driver.get(testcenter_url + "sample")
        start_button = driver.find_element_by_class_name("right")
        start_button.click()
        listening = driver.find_element_by_xpath("//input")
        listening.send_keys("She is not old")
        listening.send_keys(Keys.RETURN)
        try:
            driver.find_element_by_class_name("speak-challenge")
            assert True
        except:
            assert False 
        
        
    def tearDown(self):
        driver.close()

if __name__ == "__main__":
    unittest.main()
