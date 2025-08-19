import requests
from bs4 import BeautifulSoup

def extract_linkedin_jobs(job_role, location):
    base_url = "https://www.linkedin.com/jobs/search/"
    params = {
        "keywords": job_role,
        "location": location,
    }
    links=[]
    try:
        response = requests.get(base_url, params=params)
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup.prettify())
        print(response.url)
        # Extract job descriptions
        job_descriptions = []
        # print('soup ',soup.find_all('ul', class_='jobs-search__results-list'))
        soupss = soup.find_all('ul', class_='jobs-search__results-list')
        with open("linkedin_jobs_response.html", "w", encoding="utf-8") as file:
                 file.write(str(soupss))
        for job_detail in soupss:
            # print(job_detail)
            description = []
            print(len(job_detail.find_all('li')))
            links_= []
            for li in job_detail.find_all('li'):
                for a in li.find_all('a'):
                     href = a.get('href')
                     if '/jobs/view' in href:
                        description.append(href)
                        # res = requests.get(href)
                        links.append(href)
                        # soup2 = BeautifulSoup(res.text, "html.parser")
                        # print(soup2.prettify())
                        
                        # with open("link_jobs_response.html", "a", encoding="utf-8") as file:
                        #     file.write(soup2.prettify())
            print(description[:2],len(description))
        
            

            # if job_description:
            #     job_descriptions.append(job_description.get_text(strip=True))
            # else:
            #     print("Job description not found.")

        # print(job_descriptions)
        return job_descriptions,links
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_links(links):
        jd =[]
        for link in links:
            res = requests.get(link)
            soup2 = BeautifulSoup(res.text, "html.parser")
            divs = soup2.find('div', class_='description__text')
            description = ''
            if divs is None:
                continue
            for p in divs.find_all('p'):
                # print(p.get_text())
                
                description += p.get_text() + '  \n'
            jd.append(description)
        return jd
              



if __name__ == "__main__":
    job_role = "Machine Learning Engineer"
    location = "India"
    jddd,links = extract_linkedin_jobs(job_role, location)
    jd = extract_links(links)
    file_name = f"{job_role.replace(' ', '_')}_jobs.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(str(jd))
    print(jd[:2],len(jd))