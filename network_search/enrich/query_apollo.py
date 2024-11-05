#!/usr/bin/env python3
# -*- coding: utf-8 -*-

STOP. THE CODE DIDNT OUTPUT COMPANY NAME ON THE LAST RUN. 

import requests
import os
import pandas as pd
import time
from datetime import datetime


api_key = os.environ['APOLLO_API_KEY']
user_name = "tom_shapland" # this is used in file naming
user_dir = '/Users/tom/tmp/referral/' + user_name + '/'
input_filename = user_dir + 'email_index.csv'
output_filename = user_dir  + 'email_index_enriched.csv'

def get_last_processed_index():
    if os.path.exists(output_filename):
        df = pd.read_csv(output_filename)
        # Find the last row where 'short_description' is not null
        last_processed = df['short_description'].last_valid_index()
        return last_processed + 1 if last_processed is not None else 0
    return 0

def save_progress(df):
    df.to_csv(output_filename, index=False)

def get_company_description(email, api_key):
    url = "https://api.apollo.io/v1/people/match"
    params = {
        "api_key": api_key,
        "email": email
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("person"):
            person = data["person"]
            company = person.get("organization", {})
            return {
                "first_name": person.get("first_name"),
                "last_name": person.get("last_name"),
                "title": person.get("title"),
                "short_description": company.get("short_description"),
                "description": company.get("description"),
                "keywords": ','.join(company.get('keywords', [])),
                "num_employees": company.get("estimated_num_employees"),
                "industry": company.get("industry"),
                "industries": ','.join(company.get("industries", [])),
                "country": company.get("country"),
                "website_url": company.get("website_url")
            }
    return None

def process_batch(df, start_index, end_index):
    for i in range(start_index, end_index):
        if i >= len(df):
            break
        email = df.loc[i, 'Email']
        print(f"Processing email {i+1}/{len(df)}: {email}")
        try:
            company_details = get_company_description(email, api_key)
            if company_details:
                for key, value in company_details.items():
                    df.at[i, key] = value
                save_progress(df)
            else:
                print(f"No valid data for email: {email}")
        except Exception as e:
            print(f"Skipped a person due to an error: {e}")
    return df

def main():
    if os.path.exists(output_filename):
        df = pd.read_csv(output_filename)
    else:
        df = pd.read_csv(input_filename)
    
    last_processed_index = get_last_processed_index()
    
    while last_processed_index < len(df):
        start_index = last_processed_index
        end_index = min(start_index + 400, len(df))
        
        print(f"Processing batch from {start_index} to {end_index}")
        df = process_batch(df, start_index, end_index)
                
        last_processed_index = end_index
        
        if end_index < len(df):
            print(f"Waiting for 65 minutes before processing the next batch. Current time: {datetime.now()}")
            time.sleep(3900)  # Wait for 65 minutes (3900 seconds)

if __name__ == "__main__":
    main()