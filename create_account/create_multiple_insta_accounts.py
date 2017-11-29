from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
from settings import password

emails = [] #read from emails.txt
with open('emails.txt', 'r') as f:
	for line in f:
		emails.append(line.strip())

print('\n\n')
print('----------------------------------------------------')
print('This program will create multiple instagram accounts')
print('----------------------------------------------------')
print('\n{} email addresses found!'.format(len(emails)))
print('Starting in 30 seconds...')
time.sleep(30)

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)

for email in emails:
	driver.get("http://www.instagram.com")
	time.sleep(random.randint(8,12))
	element = driver.find_element_by_name("emailOrPhone")
	element.send_keys(email.split(',')[0].strip())
	time.sleep(random.randint(4,8))
	element = driver.find_element_by_name("fullName")
	element.send_keys(email.split(',')[1].strip())
	time.sleep(random.randint(4,8))
	element = driver.find_element_by_name("username")
	element.clear() #clearing instagram suggestion
	time.sleep(random.randint(4,8))
	element.send_keys(email.split('@')[0].strip())
	time.sleep(random.randint(12,24))
	element = driver.find_element_by_name("password")
	element.send_keys(password)
	time.sleep(random.randint(4,8))
	element.send_keys(Keys.RETURN)
	time.sleep(random.randint(12,24))
	driver.get("http://www.instagram.com")
	driver.quit()
	time.sleep(random.randint(12,24))