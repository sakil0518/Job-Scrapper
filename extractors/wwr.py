from  requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="

    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't reqeuest the website")
    else:
        results = []
        soup = BeautifulSoup(response.text, 'html.parser')

        jobs = soup.find_all('section', class_='jobs')
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a')
                anchor = anchors[1]

                link = anchor['href']

                company, kind, location = anchor.find_all('span', class_='company')
                title = anchor.find('span', class_='title')
                job_data = {
                    'link': f"https://weworkremotely.com{link}",
                    'company': company.string,
                    'location' : location.string,
                    'position': title.string
                }

                for each in job_data:
                    if job_data[each] != None:
                        job_data[each] = job_data[each].replace(",", " ")
                        
                results.append(job_data)
        # for result in results:
        #     print(result)
        #     print('=================')
        return results
