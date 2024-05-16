import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs

def scrape():
	company_name = 'Razorpay'
	forbes_100_list = pd.read_csv('forbes_100_cloud.csv')
	company_url = list(forbes_100_list[forbes_100_list['name'] == company_name]['careers_url'])[0]
	options = Options()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options = options)
	driver.get(company_url)
	driver.maximize_window()

	job_list = []

	while True:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located(
										(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]')))
		search_body = bs(driver.page_source, 'lxml')
		job_table = search_body.find('div', {'class':'col-md-12 mt-0'})
		jobs = job_table.find_all('a')

		if len(jobs) != 0:
			for i in range(1, len(jobs) + 1):
				link = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/a['
											+ str(i) + ']').get_attribute('href')
				role = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/a['
											+ str(i) + ']/div[1]/span').text
				team = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/a['
											+ str(i) + ']/div[2]/span').text
				location = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/a['
												+ str(i) + ']/div[3]/span').text.split('/')[0]
				company = company_name

				job_list.append({'Company': company,
								 'Role': role,
								 'Team': team,
								 'Location': location,
								 'Job_URL': link})
			# Next page
			# Try multiple times
			try:
				time.sleep(2)
				driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/div/ul/li[9]/div').click()
			except:
				try:
					time.sleep(2)
					driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/div/ul/li[9]/div').click()
				except:
					try:
						time.sleep(2)
						driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div/div[4]/div/ul/li[9]/div').click()
					except:
						break
		else:
			print(company_name + ': No data obtained')

	df = pd.DataFrame(job_list, columns = ['Company', 'Role', 'Team', 'Location', 'Job_URL'])
	df.drop_duplicates(inplace = True)
	df.to_csv('Jobs/' + company_name + '_Jobs.csv', index = False)

if __name__ == '__main__':
    scrape()
