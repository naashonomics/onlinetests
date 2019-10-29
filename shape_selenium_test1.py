import sys, logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
def setup(path_to_chromedriver, timeout, page_to_test):
    driver = webdriver.Chrome(path_to_chromedriver)
    driver.implicitly_wait(timeout)
    driver.get(page_to_test)
    return driver

def test(driver, row_count_expected, xpath_start, xpath_end,length_req, find_longest):
    row_count_actual = len(driver.find_elements_by_xpath("/" + xpath_end))
    if row_count_actual != row_count_expected:
      logging.warning("Expected and actual row counts are different." + " Actual row count is %d. Check xpath." %row_count_actual)
    length_req_satisfied = False 
    len_max = 0 
    if find_longest:
      longest_words = [] 
    for i in range (1, row_count_actual+1):
        text_xpath = xpath_start + "[" + str(i) + "]" + xpath_end
        try:
            row_text = driver.find_element_by_xpath(text_xpath)
        except NoSuchElementException as e:
            print("No Such Element Exception when using xpath.\n%s" %e)
            driver.quit()
            sys.exit(1)
        if row_text.is_displayed():
          logging.info("Text in row %d is displayed." %i)
        else:
          logging.warning("Text in row %d is NOT displayed." %i)
        logging.info("The text in row %d is:\n%s" %(i, row_text.text))
        words = row_text.text.split()
        for word in words:
            word_len = len(word)
            if word_len < length_req and find_longest:
              if word_len > len_max:
                len_max = word_len
                longest_words = [ word ]
              elif word_len == len_max:
                longest_words.append( word )
            if word_len >= length_req:
              if (not length_req_satisfied):
                length_req_satisfied = True
                i_req_met = i
                word_req_met = word
              if find_longest:
                if word_len > len_max:
                  len_max = word_len
                  longest_words = [ word ]
                elif word_len == len_max:
                  longest_words.append( word )
              else:
                len_max = word_len  
                break
        if length_req_satisfied:
          if find_longest:
            continue
          else:
            break

    print ('========TEST! RESULTS============')
    if find_longest:
      print ("longest (%d characters) words on the page:" %len_max)
      print (longest_words)
    if length_req_satisfied:
      print("Test 1 Passed")
    else:
      print("Test 1 Failed")
      assert length_req_satisfied, "Minimum length of %d char is NOT found." %length_req
    return 1


def cleanup(driver):
    driver.quit()
    return 1

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    path_to_chromedriver = 'C:/Users/avin/Downloads/chrome/chromedriver.exe'
    timeout = 30 
    page_to_test = 'https://the-internet.herokuapp.com/dynamic_content'
    row_count_expected = 3 
    xpath_start = "//div[@class='row']" 
    xpath_end = "/div[@class='large-10 columns']" 
	#minimum lenth of word for test for passing 
    length_req = 10 
    find_longest = True 
    driver = setup(path_to_chromedriver, timeout, page_to_test)
    try:
        test(driver,row_count_expected,xpath_start,xpath_end,length_req,find_longest)
    except AssertionError as e:
        print(e)
    finally:
        cleanup(driver)