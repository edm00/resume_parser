import requests
from bs4 import BeautifulSoup
import re

# Function to extract job descriptions from LinkedIn
# def extract_linkedin_jobs(job_role, location="United States"):
#     """
#     Extracts job descriptions from LinkedIn based on job role and location.
#     """
#     base_url = "https://www.linkedin.com/jobs/search/"
#     params = {
#         "keywords": job_role,
#         "location": location,
#     }
#     try:
#        response = requests.get(base_url, params=params)
#        soup = BeautifulSoup(response.text, "html.parser")
#        print(soup.prettify())
#     except:
#        print("Failed to retrieve the page. Status code: {response.status_code}")
#        return None
    
#     job_descriptions = []
#     for d in soup.find_all("div",id_="job-details"):
#          for s in d.find_all("div", class_="mt4"):
             
        
#         job_descriptions.append({
#             "title": title,
#             "company": company,
#             "location": location,
#             "description": description,
#             "link": link
#         })
        

#     for job in soup.find_all("div", class_="result-card"):
#         title = job.find("h3", class_="result-card__title").text.strip()
#         company = job.find("h4", class_="result-card__subtitle").text.strip()
#         location = job.find("span", class_="job-result-card__location").text.strip()
#         link = job.find("a", class_="result-card__full-card-link")["href"]
        
#         # Fetch job description from the job posting page
#         job_page = requests.get(link)
#         job_soup = BeautifulSoup(job_page.text, "html.parser")
#         description = job_soup.find("div", class_="description__text").text.strip()
        
#         job_descriptions.append({
#             "title": title,
#             "company": company,
#             "location": location,
#             "description": description,
#             "link": link
#         })
    
#     return job_descriptions

import requests
from bs4 import BeautifulSoup

def extract_linkedin_jobs(job_role, location):
    base_url = "https://www.linkedin.com/jobs/search/"
    params = {
        "keywords": job_role,
        "location": location,
    }
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
            
            for li in job_detail.find_all('li'):
                for a in li.find_all('a'):
                     href = a.get('href')
                     if '/jobs/view' in href:
                        description.append(href)
            print(description[:2],len(description))

        # print(job_descriptions)
        return job_descriptions
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# # Example usage
# job_role = "Data Scientist"
# location = "India"
# job_descriptions = extract_job_details(job_role, location)
# for jd in job_descriptions:
#     print(jd[:200])  # Print first 200 characters of each job description


# Function to extract job descriptions from Indeed
def extract_indeed_jobs(job_role, location="United States"):
    """
    Extracts job descriptions from Indeed based on job role and location.
    """
    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": job_role,
        "l": location,
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    
    job_descriptions = []
    for job in soup.find_all("div", class_="job_seen_beacon"):
        title = job.find("h2", class_="jobTitle").text.strip()
        company = job.find("span", class_="companyName").text.strip()
        location = job.find("div", class_="companyLocation").text.strip()
        link = "https://www.indeed.com" + job.find("a")["href"]
        
        # Fetch job description from the job posting page
        job_page = requests.get(link)
        job_soup = BeautifulSoup(job_page.text, "html.parser")
        description = job_soup.find("div", id="jobDescriptionText").text.strip()
        
        job_descriptions.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "link": link
        })
    
    return job_descriptions

# Function to extract job descriptions from a generic website
def extract_generic_jobs(website_url, job_role):
    """
    Extracts job descriptions from a generic website.
    """
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    job_descriptions = []
    # Customize this based on the website's HTML structure
    for job in soup.find_all("div", class_="job-listing"):  # Update class name as needed
        title = job.find("h2").text.strip()
        company = job.find("span", class_="company").text.strip()
        location = job.find("span", class_="location").text.strip()
        link = job.find("a")["href"]
        
        # Fetch job description from the job posting page
        job_page = requests.get(link)
        job_soup = BeautifulSoup(job_page.text, "html.parser")
        description = job_soup.find("div", class_="job-description").text.strip()
        
        job_descriptions.append({
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "link": link
        })
    
    return job_descriptions

# Main function to extract job descriptions
def extract_job_descriptions(website, job_role, location="United States"):
    """
    Extracts job descriptions based on the specified website and job role.
    """
    if website.lower() == "linkedin":
        return extract_linkedin_jobs(job_role, location)
    elif website.lower() == "indeed":
        return extract_indeed_jobs(job_role, location)
    else:
        return extract_generic_jobs(website, job_role)

# Example usage
example_input = { 'website': 'LinkedIn', 'job_role': 'Data Scientist', 'location': 'India' }

if __name__ == "__main__":
    # website = input("Enter the website (LinkedIn, Indeed, or a custom URL): ")
    # job_role = input("Enter the job role: ")
    # location = input("Enter the location (default: United States): ") or "United States"
    
    # jobs = extract_job_descriptions(website, job_role, location)

    jobs = extract_job_descriptions(example_input['website'], example_input['job_role'], example_input['location'])
    
    # for i, job in enumerate(jobs, 1):
    #     print(f"\nJob {i}:")
    #     print(f"Title: {job['title']}")
    #     print(f"Company: {job['company']}")
    #     print(f"Location: {job['location']}")
    #     print(f"Description: {job['description'][:200]}...")  # Print first 200 characters
    #     print(f"Link: {job['link']}")