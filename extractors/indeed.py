from  requests import get
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def get_page_count(keyword):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드

    browser = webdriver.Chrome()
    # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #크롬드라이버를 최신으로 유지해줍니다
    browser.get(f'https://ca.indeed.com/jobs?q={keyword}')

    soup = BeautifulSoup(browser.page_source,'html.parser')
    pagination = soup.find('nav', class_='ecydgvn0')
    pages = pagination.find_all('div', recursive=False)
    count = len(pages)

    if count == 0:
        return 1
    else:
        return count-1

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print('found', pages, 'pages')

    results =[]
    for page in range(pages):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드

        browser = webdriver.Chrome()
        # browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options) #크롬드라이버를 최신으로 유지해줍니다
        browser.get(f'https://ca.indeed.com/jobs?q={keyword}&start={page*10}')

        soup = BeautifulSoup(browser.page_source, 'html.parser')
        job_list = soup.find("ul", class_="css-zu9cdh")
        jobs = job_list.find_all('li', recursive = False)
        for job in jobs:

            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one('h2 a')
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find('span', class_='companyName')
                location = job.find('div', class_='companyLocation')

                job_data = {
                    'link': f'https://ca.indeed.com{link}',
                    'company' : company.string,
                    'location' : location.string,
                    'position' : title
                }

                for each in job_data:
                    if job_data[each] != None:
                        job_data[each] = job_data[each].replace(",", " ")

                results.append(job_data)
    return results
