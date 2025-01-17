import requests
import csv
import json

# Function to send a POST request and save the JSON response to CSV
def download_workday_job_data(api_url: str, job_uri: str, company_name: str, csv_filename: str, headers: dict = None):
    try:
        # List to store extracted job data
        jobs_data = []
        # total number of data item
        total = 0
        # page size, work day limit the page size to 20, do not change it to be more than 20
        page_size = 20
        # At least one page
        page_count = 1
        
        # index of the page
        i = 0
        while i < page_count: 
            print(f"Get data for page {i+1}")
            
            # Prepare the payload for POST call
            payload = {
                "appliedFacets":{},
                "limit":20,
                "offset":i * 20,
                "searchText":""
            } 
            # Send the POST request to the API
            response = requests.post(api_url, json=payload, headers=headers)

            # Check if the request was successful
            response.raise_for_status()

            # Parse the response JSON content
            response_data = response.json()
            
            if total == 0:
                total = response_data['total']
                page_count = int(total / page_size) if total % page_size == 0 else int(total / page_size ) + 1
        
            jobs = response_data['jobPostings']
            
            # prepare to get next page
            i = i + 1
            
            for item in jobs:
                job_title = item['title']
                job_location = item['locationsText']
                job_link = job_uri + item['externalPath']
                job_department = "N/A"
                # Append job details to the list
                jobs_data.append([company_name.strip(), job_title.strip(), job_location.strip(), job_department, job_link])    

        print(f"finished downloading all jobs for company {company_name}")
                
        # Open the CSV file for writing
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            # Create a CSV writer object
            writer = csv.writer(file)
            
            # Write header row
            writer.writerow(['Company', 'Job Title', 'Location', 'Function', 'Job Link'])
            # Write job rows
            writer.writerows(jobs_data)

        print(f"Data successfully saved to {csv_filename}")
    
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed when fetching page {i}, error: {e} ")
    except Exception as e:
        print(f"An error occurred: {e}")
        

# Example Usage
if __name__ == "__main__":
      
    # API endpoint URL
    api_url = "https://linklogistics.wd5.myworkdayjobs.com/wday/cxs/linklogistics/link/jobs"
    job_uri = "https://linklogistics.wd5.myworkdayjobs.com/en-US/link"
    company = "Link Logistics"

    api_url = "https://g6hospitality.wd5.myworkdayjobs.com/wday/cxs/g6hospitality/G6_job_Openings/jobs"
    job_uri = "https://g6hospitality.wd5.myworkdayjobs.com/en-US/G6_job_Openings"
    company = "G6 Hospitality"
    
    api_url = "https://qtsdatacenters.wd5.myworkdayjobs.com/wday/cxs/qtsdatacenters/qts/jobs"
    job_uri = "https://qtsdatacenters.wd5.myworkdayjobs.com/en-US/qts"
    company = "QTS"
    # API request headers
    headers = {
        "Content-Type": "application/json",
    }

    # CSV filename where data will be saved
    csv_filename = 'workday_jobs_data.csv'
    
    

    # Call the function to post the request and save the CSV
    download_workday_job_data(api_url, job_uri, company, csv_filename, headers)
