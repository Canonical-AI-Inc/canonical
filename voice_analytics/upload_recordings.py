
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 14:39:30 2024
@author: tom
"""
import os
import requests
import csv
from urllib.parse import urlparse

# from dotenv import load_dotenv
# load_dotenv()
# API_KEY = os.environ["CANONICAL_API_KEY"]

# User inputs
API_KEY = ''
SLUG = '' # this is the name of the ai assistant as you want it to appear on our dashboard
input_filename = '' # this is a csv with a list of publicly-accessible urls for the audio recordings
ai_speaks_first = True

CANONICAL_API = 'https://voiceapp.canonical.chat'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Canonical-Api-Key': API_KEY
}

def extract_filename(url):
    """Extract filename from URL."""
    return os.path.basename(urlparse(url).path)

def process_url(url):
    """Process a single URL."""
    filename = extract_filename(url)
    try:
        response = requests.post(
            f"{CANONICAL_API}/api/v1/call",
            json={
                "assistant": {
                    "id": SLUG,
                    "speaksFirst": ai_speaks_first
                },
                "location": url,
                "callId": filename
            },
            headers=HEADERS
        )
        response.raise_for_status()
        print(f"Processed {filename}: {response.json()}")
    except requests.RequestException as error:
        print(f"Error processing {filename}: {str(error)}")

def main():
    with open(input_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:  # Check if the row is not empty
                url = row[0]  # Assuming URL is in the first (and only) column
                process_url(url)

if __name__ == "__main__":
    main()
    
    



