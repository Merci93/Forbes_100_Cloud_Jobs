import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Netlify'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	# Wait
	wait_path = '//*[@id="main"]/form/div/div[2]/table/tbody/tr[1]/td[2]'
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, wait_path)))

	search_body = bs(driver.page_source, 'lxml')
	job_table = search_body.find('table', {'class':'careers-results'})
	jobs = job_table.find_all('tr')

	job_list = []

	if len(jobs) != 0:
		for job in jobs:
			try:
				link = job.find('a').get('href')
				role = job.find('a').text
				team = job.find_all('a')[1].text
				location = job.find('td', {'data-tablefilter':'keyword'}).text.replace('Location ', '')
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			except:
				continue
	else:
		print(company_name + ': No data obtained')

	columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL']
	df = pd.DataFrame(job_list, columns = columns)

	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()

