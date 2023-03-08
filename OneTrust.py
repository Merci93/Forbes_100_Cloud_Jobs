import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'OneTrust'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Close cookies
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
			                           (By.XPATH, '//*[@id="onetrust-reject-all-handler"]'))).click()
	except:
		pass

	# Open positions
	WebDriverWait(driver, 10).until(EC.presence_of_element_located(
		                           (By.LINK_TEXT, 'View Open Positions'))).click()

	# Load all data
	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located(
				                           (By.XPATH, '//*[@id="load"]'))).click()
		except:
			break

	search_body = bs(driver.page_source, 'html.parser')
	jobs = search_body.find_all('tr', {'class':'job-row active'})

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			role = job.find('td', {'class':'job-name'}).text 
			team = job.find('td', {'class':'department'}).text.split('|')[0]
			location = job.find('td', {'class':'location'}).text 
			link = job.find('a', {'class':'apply-link'}).get('href')
			company = company_name

			job_list.append({'Company': company,
							 'Role': role,
							 'Team': team,
							 'Location': location,
							 'Job_URL': link})
	else:
		print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
    