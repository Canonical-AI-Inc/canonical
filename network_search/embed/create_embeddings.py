
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import pickle
import os
from openai import OpenAI
from tqdm import tqdm
import numpy as np

# Initialize
user_name = "tom_shapland"
user_dir = '/Users/tom/tmp/referral/' + user_name + '/'
input_filename = user_dir + 'email_index_enriched_cleaned.csv'
output_filename = user_dir + user_name + '_company_title_embeddings.pkl'

# Set up OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def encode(texts, model="text-embedding-ada-002"):
    embeddings = []
    for text in tqdm(texts, desc="Creating embeddings"):
        response = client.embeddings.create(input=text, model=model)
        embeddings.append(response.data[0].embedding)
    return embeddings

def main():
    # Read the dataset
    print("Reading the dataset...")
    df = pd.read_csv(input_filename)  
    
    # create user column
    df['contact'] = user_name
    
    # Handle NaN values in 'title' by replacing them
    df['title'] = df['title'].fillna('Unknown')
    
    # Create company embeddings
    print("\nCreating company embeddings...")
    company_embeddings = encode(df['summary'].tolist())
    
    # Create title embeddings
    print("\nCreating title embeddings...")
    title_embeddings = encode(df['title'].tolist())
       
    # Add embeddings to the dataframe
    df['company_embedding'] = company_embeddings
    df['title_embedding'] = title_embeddings
    
    # Convert embeddings to numpy arrays
    df['company_embedding'] = df['company_embedding'].apply(np.array)
    df['title_embedding'] = df['title_embedding'].apply(np.array)
    
    # Save combined dataframe
    print(f"\nSaving embeddings to {output_filename}...")
    with open(output_filename, 'wb') as f:
        pickle.dump(df, f)
    
    print("Combined embeddings created and saved successfully.")

if __name__ == "__main__":
    main()