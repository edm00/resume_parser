import requests
from bs4 import BeautifulSoup

def extract_job_description(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # This part may need to be customized based on the website's structure
    job_description = soup.find('div', class_='job-description')
    
    if job_description:
        return job_description.get_text(strip=True)
    else:
        print("Job description not found.")
        return None

if __name__ == "__main__":
    url = "https://example.com/job-posting-url"
    job_description = extract_job_description(url)
    if job_description:
        print("Job Description:")
        print(job_description)