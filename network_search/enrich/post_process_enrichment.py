#!/usr/bin/env python3
# -*- coding: utf-8 -*-

user_name = "tom_shapland" # this is used in file naming
user_dir = '/Users/tom/tmp/referral/' + user_name + '/'
input_filename = user_dir + 'email_index_enriched.csv'
optional_input_filename = user_dir + 'email_index_manually_enriched.csv'
output_filename = user_dir  + 'email_index_enriched_cleaned.csv'

import pandas as pd
import os
from urllib.parse import urlparse

def add_company_column(df):
    # Check if 'company' column exists
    if 'company' not in df.columns:
        # Check if 'website_url' column exists
        if 'website_url' not in df.columns:
            raise ValueError("DataFrame must contain a 'website_url' column if 'company' column is not present.")
        
        # Function to extract company name from URL
        def extract_company(url):
            if pd.isna(url) or not isinstance(url, str):
                return None  # Return None for NaN or non-string values
            try:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                # Remove 'www.' if present
                if domain.startswith('www.'):
                    domain = domain[4:]
                # Split by '.' and take the first part
                company = domain.split('.')[0]
                return company
            except:
                return None  # Return None if there's any error in parsing
        
        # Apply the function to create the 'company' column
        df['company'] = df['website_url'].apply(extract_company)
    
    return df

# read the data
df = pd.read_csv(input_filename)  

# if the file 'optional_input_filename' exists, then read it in and append it to the end of df
if os.path.exists(optional_input_filename):
    new_data = pd.read_csv(optional_input_filename)
    df = pd.concat([df, new_data], ignore_index=True)

# if company is missing, use the url to guess it
df = add_company_column(df)
    
# Sometimes short_description is NaN, but apollo still returns industry.
# If short_description is NaN and industry or industries exist, replace short_description with the industry and industries
df.loc[df['short_description'].isna() & (df['industry'].notna() | df['industries'].notna()), 'short_description'] = df['company'].fillna('') + ", " + df['industry'].fillna('') + ', ' + df['industries'].fillna('')

# Gmail contacts generally don't have short_description. But sometimes they have titles and company.
# Set the short_description to unknown so they get persisted.
df.loc[(df['Email'].str.endswith('@gmail.com', na=False)) & (df['short_description'].isna()), 'short_description'] = 'unknown'

# if 'Organization Short Description' is NaN, then drop the row from the df
df = df.dropna(subset=['short_description'])

# Create a unique identifier for each contact
df['user_name_uid'] = df['First Name'] + '_' + df['Last Name']

# Identify duplicates
duplicates = df[df.duplicated(subset='user_name_uid', keep=False)]

# For duplicates, keep the one with the highest Count
duplicates_highest_count = duplicates.sort_values('Count', ascending=False).drop_duplicates(subset='user_name_uid', keep='first')

# Get the non-duplicates
non_duplicates = df[~df.duplicated(subset='user_name_uid', keep=False)]

# Combine non-duplicates with the highest-count duplicates
df = pd.concat([non_duplicates, duplicates_highest_count]).sort_index()

# Reset the index
df = df.reset_index(drop=True)

# To drop the column named 'name' from the DataFrame df
df = df.drop('user_name_uid', axis=1)

# resort by last name
df = df.sort_values('Last Name', ascending=True)

# Evaluate response likelihood
def evaluate_number(number):
    if number <= 1:
        return 'unlikely'
    elif 1 < number < 5:
        return 'likely'
    else:
        return 'very likely'

# Apply the function to the 'number' column and create a new column 'output'
df['response_likelihood'] = df['Count'].apply(evaluate_number)

# truncate the short description for readability in the final output
df['short_description_trunc'] = df['short_description'].apply(lambda x: x[:500])

# include the network owners name
df['contact'] = user_name

# create a column that summarizes the company information
def create_summary(row):
    company = row['company'] if pd.notna(row['company']) else ''
    short_description = row['short_description'] if pd.notna(row['short_description']) else ''
    keywords = row['keywords'] if pd.notna(row['keywords']) else ''
    industry = row['industry'] if pd.notna(row['industry']) else ''
    industries = row['industries'] if pd.notna(row['industries']) else ''
    
    # Remove any trailing commas and extra spaces
    keywords = ', '.join(word.strip() for word in keywords.split(',') if word.strip())
    industries = ', '.join(ind.strip() for ind in industries.split(',') if ind.strip())
    
    return f"{company}. {short_description} Keywords: {keywords}. Industries: {industry}, {industries}."

# Apply the function
df['summary'] = df.apply(create_summary, axis=1)

# 
df.to_csv(output_filename, index=False)

