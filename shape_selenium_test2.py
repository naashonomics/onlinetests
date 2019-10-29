import sys, logging, os, shutil, sys, urllib, json , urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def setup(path_to_chromedriver, timeout, page_to_test):
    driver = webdriver.Chrome(path_to_chromedriver)
    driver.implicitly_wait(timeout)
    driver.get(page_to_test)
    return driver
	
def cleanup(driver):
    driver.quit()
    return 1

def test2(driver, row_count_expected, xpath_avatars, punisher,known_avatars, assign_names):

    page_avatars = []  
    punisher_not_here = True  
    avatars = driver.find_elements_by_xpath(xpath_avatars)
    row_count_actual = len(avatars)  
    if row_count_actual != row_count_expected:
      logging.warning("Expected and actual row counts are different." + " Actual row count is %d. Check xpath." %row_count_actual)

    for n,av in enumerate(avatars, start = 1):
        url = av.get_attribute('src')
        logging.info("Avatar(row %d) URL is: %s" %(n,url))
        f_name = 'row' + str(n) + 'av.jpg'
        logging.info("Avatar(row %d) image downloaded as %s file" %(n,f_name))
        with urllib.request.urlopen(url) as resp, open(f_name, 'wb') as out_f:
            shutil.copyfileobj(resp, out_f)
        size = os.path.getsize(f_name)
        logging.info("Avatar(row %d) file size is %d bytes" %(n,size))
        if assign_names:
            url_m = False
            size_m = False
            for known_av in known_avatars:
                if known_av['url'] == url:
                    url_m = True
                if known_av['size'] == size:
                    size_m = True
                if url_m or size_m:
                    break
            if url_m and size_m:
                if size == punisher['size']:
                    punisher_not_here = False
                    punisher_row = n
                page_avatars.append(known_av)
            else:
                name = url[-12:-4]
                new_av = {
                    'name': name,
                    'url' : url,
                    'size' : size
                }
                known_avatars.append(new_av)
                page_avatars.append(new_av)
                if url_m or size_m:
                    logging.warning('Only size or URL matches a known ' + 'avatar in row %d' %n)
                logging.info(known_avatars)
        else:
            if size == punisher['size'] and url == punisher['url']:
                punisher_not_here = False
                punisher_row = n
                break
    print ('========TEST2============')
	
    if assign_names:
        print("q: Give names to each avatar that can appear on the page and print out each avatars name")
        print("%d avatars found on the page:" %len(page_avatars))
        for av in page_avatars:
            print(av['name'])
        f = open("known_avatars.json", "w")
        json.dump(known_avatars, f)
        f.close()
    assert punisher_not_here, "Test Passed:Punisher was last found in row %d. " %punisher_row
    print("Test Failed:Punisher not found in Avatar list")
    return 1

if __name__ == '__main__':
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
	path_to_chromedriver = 'C:/Users/avin/Downloads/chrome/chromedriver.exe'
	timeout = 30
	page_to_test='https://the-internet.herokuapp.com/dynamic_content'
	row_count_expected = 3 
	xpath_avatars = "//div[@class='large-2 columns']/img" 
	name_p = 'Punisher'  
	url_p = 'https://the-internet.herokuapp.com/img/avatars/Original-' + 'Facebook-Geek-Profile-Avatar-3.jpg' 
	size_p = 12817      
	punisher = {       
		'name': name_p,
		'url' : url_p,
		'size' : size_p
	}
	if os.path.exists("known_avatars.json"):
		known_avatars = json.load(open("known_avatars.json"))
	else:
		known_avatars  = [punisher]
	assign_names = True  
	driver = setup(path_to_chromedriver, timeout, page_to_test)
	try:
		test2(driver, row_count_expected, xpath_avatars, punisher, known_avatars, assign_names)
	except AssertionError as e:
		print(e)
	finally:
		cleanup(driver)