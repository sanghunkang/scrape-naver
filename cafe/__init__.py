import os, sys, time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium

import config

# Define constants
SYSTEM = sys.platform

PATH_URLLIST = '.\\results\\urllist.txt'
PATH_ARTICLES = '.\\results\\articles.txt'
PATH_COMMENTS = '.\\results\\comments.txt'

SPLITER = '||SPLITER||'

# Import personal data to login
USER_ID	= config.USER_ID
USER_PW	= config.USER_PW

# Define functions without return
def initialize_file(path):
	with open(path, 'w', encoding='utf-8') as fw:
		pass

def append_to_file(path, str_input):
	with open(path, 'a', encoding='utf-8') as fw:
		fw.write(str_input)

def hard_trigger(elem):
	driver.execute_script("arguments[0].click();", elem);

def hard_input(id_elem, str_input):
	elem = driver.find_element_by_id(id_elem)
	actions = ActionChains(driver)
	actions.move_to_element(elem)
	actions.click()
	actions.send_keys(str_input)  # Replace with whichever keys you want.
	actions.perform()

# def chain_find_element(driver_current, seq_locator):
# 	locator = seq_locator.pop(0)

# Define functions with return
def generate_list_from_txt(path):
	ret = []
	with open(path, "r") as f:
		line_read = f.readline()
		while line_read:
			ret.append(line_read)
			line_read = f.readline()
	return ret

def wrap_entries(dict_entries, spliter):
	ret = ''
	for key in entries.keys():
		ret = ret + entries[key] + spliter
	ret = ret + '\n'
	return ret

# Run ########################################################################
# Initialise output files
initialize_file(PATH_ARTICLES)
initialize_file(PATH_COMMENTS)

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
# menulink = driver.find_element_by_id('menuLink59') #.click()
# driver.execute_script("arguments[0].click()", menulink)



# Move to the first article from the list
# article_board = driver.find_elements_by_class_name('article-board')[1]
# article_board.find_element_by_class_name('aaa').click()

indexlist = generate_list_from_txt(PATH_URLLIST)

for index in indexlist:
	
	# cur = driver.find_element_by_class_name('list-btn-nor2')
	# cur = cur.find_element_by_class_name('fl')
	# cur = cur.find_elements_by_class_name('btn2')[-1]
	# cur.click()

	try:
		driver.get(url_base + str(index))

		# Swith into inside iframe, where all relevant contents are
		main_area = driver.find_element_by_id('main-area')
		iframe = main_area.find_element_by_tag_name('iframe')
		driver.switch_to_frame(iframe)

		inbox = driver.find_element_by_class_name('inbox')

		# ART_ID
		# cur = inbox.find_element_by_class_name('etc-box')
		# cur = cur.find_element_by_class_name('fr')
		# cur = cur.find_element_by_class_name('filter-50')
		# ART_ID = cur.text.split('/')[-1]

		# ART_TITL
		cur = inbox.find_element_by_class_name('tit-box')
		cur = cur.find_element_by_class_name('fl')		
		cur_ART_TITL = cur.find_elements_by_class_name('m-tcol-c')[0]
		cur_BORADTYP = cur.find_elements_by_class_name('m-tcol-c')[-1]
		if "나의여행" not in cur_BORADTYP.text:
			raise selenium.common.exceptions.NoSuchElementException
		print(cur_BORADTYP.text)
		ART_TITL = cur.text
		
		# ART_ID
		ART_ID = str(index)

		# DATETIME
		cur = inbox.find_element_by_class_name('tit-box')
		cur = cur.find_element_by_class_name('fr')
		DATETIME  = cur.find_element_by_class_name('m-tcol-c').text

		# CONTENT
		CONTENT = inbox.find_element_by_id('tbody').text
		CONTENT = CONTENT.replace('\n', '&&\\n&&')

		# Create an entry dictonary which will be later wrapped by wrap_entries()
		entries = dict()
		entries['ART_ID'] = ART_ID
		entries['ART_TITL'] = ART_TITL
		entries['DATETIME'] = DATETIME
		entries['CONTENT'] = CONTENT

		entries_wrapped = wrap_entries(entries, SPLITER)

		# COMMENTS
		COMMENTS = ''
		seq_comment = inbox.find_elements_by_class_name('comm_body')
		for comment in seq_comment:
			comment_single = comment.text
			comment_single = comment_single.replace('\n', '&&\\n&&')
			print(comment.text)
			COMMENTS = COMMENTS + ART_ID + SPLITER + comment_single + '\n'

		print(COMMENTS)

		append_to_file(PATH_ARTICLES, entries_wrapped)
		append_to_file(PATH_COMMENTS, COMMENTS)

	except selenium.common.exceptions.UnexpectedAlertPresentException:
		print('Deleted or Non-existant page')
		driver.switch_to_alert().accept()

	except selenium.common.exceptions.NoSuchElementException:
		print('Expected elements not Found: NoSuchElementException')

# Write and save 

driver.close()
driver.quit()
	