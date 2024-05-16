import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Socure'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Cookies
	try:
		WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
			                            (By.XPATH, '//*[@id="onetrust-banner-sdk"]/div/div/div[1]/button'))).click()
	except:
		pass

	# Open positions
	pos = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
									(By.XPATH, '//*[@id="content"]/section[1]/div[2]/div/a'))).get_attribute('href')
	driver.get(pos)
	
	# Number of job postings
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'css-1q2dra3')))
	search_body = bs(driver.page_source, 'lxml')
	number_of_jobs = search_body.find('p', {'class':'css-12psxof'}).text.split(' ')[0]

	job_list = []
	url = 'https://socure.wd1.myworkdayjobs.com'

	while True:
		# Wait
		time.sleep(2)
		search_body = bs(driver.page_source, 'lxml')
		number_of_jobs = search_body.find('p', {'class':'css-12psxof'}).text.split(' ')[0]
		jobs = search_body.find_all('li', {'class':'css-1q2dra3'})

		if len(jobs) != 0:
			for job in jobs:
				link = url + job.find('a').get('href')
				role = job.find('a').text
				location = job.find('dd', {'class':'css-129m7dg'}).text
				team = 'N/A'
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})

			# Next page
			if (len(job_list)) <= int(number_of_jobs):
				try:
					driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/section/div[2]/nav/div/button[2]').click()
				except:
					try:
						driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[2]/section/div[2]/nav/div/button').click()
					except:
						break
			else:
				break
		else:
			print(company_name + ': No data obtained')
			break

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.reset_index(drop = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)	

	# time.sleep(2)
	# search_body = bs(driver.page_source, 'html.parser')
	# job_table = search_body.find('div', {'class':'career_job_container'})
	# jobs = job_table.find_all('div', {'class':'content'})

	# job_list = []
	# url = 'https://www.socure.com'

	# if len(jobs) != 0:
	# 	for job in jobs:
	# 		role = job.find('a').text.split(' | ')[0]
	# 		link = url + job.find('a').get('href')
	# 		location = job.find('div', {'class':'job_dt_loc'}).text.split(' | ')[1]
	# 		team = job.find('div', {'class':'job_dt_loc'}).text.split(' | ')[0]
	# 		company = company_name

	# 		job_list.append({'Company': company,
	# 						 'Role': role,
	# 						 'Team': team,
	# 						 'Location': location,
	# 						 'Job_URL': link})
	# else:
	# 	print(company_name + ': No data obtained')

	# df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	# df.drop_duplicates(inplace = True)
	# df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
    