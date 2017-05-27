import os, sys, time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium

# Define constants
SYSTEM = sys.platform

def get_config(system):
	ret = {}
	if "win" in system:
		path_config = "..\\.config\\Scrape_CafeNaver\\config"
	else:
		path_config = "../.config/Scrape_CafeNaver/config"

	with open(path_config) as f:
		ret["USER_ID"] = f.readline().strip()
		ret["USER_PW"] = f.readline().strip()		
	return ret

# Import personal data to login
USER_ID	= get_config(SYSTEM)["USER_ID"]
USER_PW	= get_config(SYSTEM)["USER_PW"]

PATH_URLLIST = '.\\results\\urllist.txt'


# Define functions without return
def initialize_file(path):
	with open(path, 'w', encoding='utf-8') as fw:
		pass

def append_to_file(path, str_input):
	with open(path, 'a', encoding='utf-8') as fw:
		fw.write(str_input)

def hard_input(id_elem, str_input):
	elem = driver.find_element_by_id(id_elem)
	actions = ActionChains(driver)
	actions.move_to_element(elem)
	actions.click()
	actions.send_keys(str_input)  # Replace with whichever keys you want.
	actions.perform()

# def hard_trigger(elem):

# def chain_find_element(driver_current, seq_locator):
# 	locator = seq_locator.pop(0)

# Define functions with return
def wrap_entries(dict_entries, spliter):
	ret = ''
	for key in entries.keys():
		ret = ret + entries[key] + spliter
	ret = ret + '\n'
	return ret

# Run ########################################################################
# Initialise output files
initialize_file(PATH_URLLIST)

# Launch the webdriver
driver = webdriver.Chrome()

# Attempt login
driver.get('https://nid.naver.com/nidlogin.login')

# Locate to account and password input boxes and enter account
hard_input('id_area', USER_ID)
hard_input('pw_area', USER_PW)

# Trigger the submit button
driver.find_element_by_class_name('btn_global').click()

# Move to Eurang
url_base = 'http://cafe.naver.com/firenze/'
driver.get('http://cafe.naver.com/firenze')

# Move to Reviewboard
menulink = driver.find_element_by_id('menuLink59') #.click()
driver.execute_script("arguments[0].click()", menulink)

# Swith into inside iframe, where all relevant contents are
main_area = driver.find_element_by_id('main-area')
iframe = main_area.find_element_by_tag_name('iframe')
driver.switch_to_frame(iframe)

# print(len(btns))
i = 1
while True:
	i += 1

	str_write = "" 
	cnts = driver.find_elements_by_class_name("list-count")
	for cnt in cnts:
		str_write = str_write + cnt.text + "\n"

	cur = driver.find_element_by_class_name("prev-next")
	btns = cur.find_elements_by_tag_name("a")
	
	elem = btns[i]
	driver.execute_script("arguments[0].click();", elem);

	if i == 11:
		i = 1

	# Write and save
	append_to_file(PATH_URLLIST, str_write)

# Close and kill process
driver.close()
driver.quit()



