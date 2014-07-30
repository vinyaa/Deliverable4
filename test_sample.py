# Tests workflow for sample testing questions

# Test that user can access sample test -- 2
# Sample questions button is present @ testcenter_url
def test_sample_questions_exists():
    driver.get(testcenter_url)
    sample_label = driver.find_element_by_class_name("sample-questions").text.strip()
    assert (sample_label == "Sample Questions")

# Clicking sample button @ testcenter_url starts sample questions
def test_sample_questions_works():
    driver.get(testcenter_url)
    sample_button = driver.find_element_by_class_name("sample-questions").click()
    sample_url = driver.current_url
    assert (sample_url == "https://testcenter.duolingo.com/sample")


# Test splash page options -- 2
# Clicking quit button @ sample questions returns to testcenter_url
def test_quit_sample_splash(self):
    driver.get(testcenter_url + "sample")
    quit_button = driver.find_element_by_class_name("left")
    quit_button.click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)

# Clicking start button @ sample questions begins listen challenge
def test_start_sample(self):
    driver.get(testcenter_url + "sample")
    start_button = driver.find_element_by_class_name("right")
    start_button.click()
    try: 
        driver.find_element_by_class_name("listen-challenge")
        assert True
    except:
        assert False


# Test listening module
# Type "She is not old." and press enter, advance to speak challenge
def test_listen_module(self):
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

# Test speech module
# Click record-button, wait 2 seconds, click stop-button, click class="btn right btn-lg btn-primary btn-submit btn-success"
def test_speak_module(self):
    # Advance to the right module
    driver.get(testcenter_url + "sample")
    start_button = driver.find_element_by_class_name("right")
    start_button.click()
    listening = driver.find_element_by_xpath("//div[@id ='challenge']/div[1]/div[2]/input[1]")
    listening.send_keys("She is not old")
    listening.send_keys(Keys.RETURN)
    
    # Start test
    mic = driver.find_element_by_id("record-button")
    mic.click()
    time.sleep(2)
    mic.click()
    submit = driver.find_element_by_xpath("//footer/button[1]")
    submit.click()
    try:
        driver.find_element_by_class_name()

# Test vocab module
# Click the buttons that say [fine good easy bag walk both may], click submit button
def test_vocab_module(self):
    #Advance to the right module
    driver.get(testcenter_url + "sample")
    start_button = driver.find_element_by_class_name("right")
    start_button.click()
    listening = driver.find_element_by_xpath("//div[@id ='challenge']/div[1]/div[2]/input[1]")
    listening.send_keys("She is not old")
    listening.send_keys(Keys.RETURN)
    mic = driver.find_element_by_id("record-button")
    mic.click()
    time.sleep(2)
    mic.click()
    submit = driver.find_element_by_xpath("//footer/button[1]")
    
    #Start test
    vocab_buttons = driver.find_elements_by_class_name("btn")
    vocab_options = ["fine", "good", "easy", "bag", "walk", "both", "may"]
    for button in vocab_buttons:
        my_text = button.innerHTML
        if my_text in vocab_options:
            button.click()

# Test dropdown module
# [has were was became swam] & submit -- class="step bg-certificate" heading2 should say "Sample questions complete!"
def test_dropdown_module(self):
    select_1 = driver.find_element_by_xpath("//div[@id='dropout-f84b22d51ba03e7c198a1dd22ad7a88e']/select[1]")
    select_2 = driver.find_element_by_xpath("//div[@id='dropout-f84b22d51ba03e7c198a1dd22ad7a88e']/select[2]")
    select_3 = driver.find_element_by_xpath("//div[@id='dropout-f84b22d51ba03e7c198a1dd22ad7a88e']/select[3]")
    select_4 = driver.find_element_by_xpath("//div[@id='dropout-f84b22d51ba03e7c198a1dd22ad7a88e']/select[4]")
    select_5 = driver.find_element_by_xpath("//div[@id='dropout-f84b22d51ba03e7c198a1dd22ad7a88e']/select[5]")
    
    select_1.select_by_value("has")
    select_2.select_by_value("were")
    select_3.select_by_value("was")
    select_4.select_by_value("became")
    select_5.select_by_value("swam")
    submit = driver.find_element_by_xpath("//footer/button[1]")
    
    complete_message = driver.find_element_by_tag_name('h2')
    expected_message = "Sample questions complete!"
    assert (complete_message == expected_message)
    
    
# Test options post-completion -- 2
# Clicking back to home button @ Complete returns to testcenter_url
def test_back_to_home(self):
    back_to_home = driver.find_element_by_class_name("left")
    back_to_home.click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)
    
# Clicking take test button @ Complete starts test
def test_take_real_test(self):
    real_test = driver.find_element_by_class_name("right")
    real_test.click()
    new_url = driver.current_url
    test_url = "https://testcenter.duolingo.com/test/"
    assert (new_url == test_url)


# Test quit menu options -- 2
# Clicking quit, then cancel returns to sample questions
def test_quit_cancel(self):
    driver.get(testcenter_url + "sample")
    driver.find_element_by_class_name("right").click()
    driver.find_element_by_class_name("leave-exam").click()
    # Click cancel to return to test
    driver.find_element_by_xpath("//button[2]").click()
    new_url = driver.current_url
    assert (new_url == testcenter_url + "sample")
    
# Clicking quit, then ok returns "You left this test". Click ok and return to testcenter_url and camera off
def test_quit_test(self):
    driver.get(testcenter_url + "sample")
    driver.find_element_by_class_name("right").click()
    driver.find_element_by_class_name("leave-exam").click()
    # Click ok to quit
    driver.find_element_by_xpath("//button[1]").click()
    # Click ok to leave test
    driver.find_element_by_xpath("//button[1]").click()
    new_url = driver.current_url
    assert (new_url == testcenter_url)
    
