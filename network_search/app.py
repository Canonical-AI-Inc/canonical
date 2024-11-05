#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gradio as gr
import os
import pickle
from openai import OpenAI
import math
import pandas as pd
import jwt
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

#############################################
#### initialize
#############################################

load_dotenv()  # Load environment variables from .env file
JWT_SECRET = os.environ.get("JWT_SECRET")  # Make sure this matches the secret in your Flask app

# Get the directory of the current script
current_dir = os.getcwd()

# User connections dictionary
user_connections = {
    "tom_at_canonical_dot_chat": ["tom_at_canonical_dot_chat"],
    "friend_one_at_gmail_dot_com": ["tom_at_canonical_dot_chat", "friend_one_at_gmail_dot_com"],
    "friend_two_at_gmail_dot_com": ["tom_at_canonical_dot_chat", "friend_one_at_gmail_dot_com"],
}

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY']) 

data = None

#############################################
#### define functions
#############################################

def decode_jwt(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_user_info(request: gr.Request):
    query_params = parse_qs(urlparse(request.headers.get('referer', '')).query)
    token = query_params.get('token', [None])[0]
    if token:
        user_info = decode_jwt(token)
        if user_info:
            name = user_info['name']
            email = user_info['email']
            user_id = email.replace('@', '_at_').replace('.', '_dot_')
            return f"Welcome, {name}!", user_id
    return "Welcome, Guest!", None

# Global variable to store the data
data = None

def load_data(user_id=None):
    global data
    if user_id is None or user_id not in user_connections:
        user_id = "tom_at_canonical_dot_chat"  # Default user_id
    
    all_data = []
    for connected_user in user_connections[user_id]:
        current_dir = os.getcwd()
        input_filename = os.path.join(current_dir, 'data', f'{connected_user}_company_title_embeddings.pkl')
        try:
            with open(input_filename, 'rb') as f:
                user_data = pickle.load(f)
                # Add a column to identify the source user
                user_data['source_user'] = connected_user
                all_data.append(user_data)
        except FileNotFoundError:
            print(f"Data file for user {connected_user} not found.")
    
    if not all_data:
        print("No data files were found. Creating an empty DataFrame.")
        return pd.DataFrame(columns=['industry', 'industries', 'source_user'])
    
    # Combine all dataframes
    data = pd.concat(all_data, ignore_index=True)
    
    # Sort the data to group duplicates together
    data = data.sort_values(by=['First Name', 'Last Name', 'company', 'title', 'source_user'])
    
    return data

# Load the data immediately
data = load_data()

def get_unique_industries(df):
    # Combine 'industry' and 'industries' columns
    combined = pd.concat([df['industry'], df['industries']])
    
    # Split the comma-separated values in 'industries'
    split_industries = combined.str.split(',', expand=True).stack()
    
    # Remove leading/trailing whitespace
    clean_industries = split_industries.str.strip()
    
    # Remove NaN values and get unique values
    unique_industries = clean_industries.dropna().unique()
    
    # Sort alphabetically
    sorted_industries = sorted(unique_industries)
    
    return sorted_industries

def get_unique_industries_list():
    global data
    if data is None or data.empty:
        return ["All Industries"]
    unique_industries = ["All Industries"] + get_unique_industries(data)
    return unique_industries

def filter_by_industry(results, selected_industries):
    if "All Industries" in selected_industries:
        return results
    return [
        result for result in results
        if any(industry in (result.get('industry', ''), result.get('industries', '')) for industry in selected_industries)
    ]

def filter_by_response_likelihood(results, include_unlikely):
    if include_unlikely:
        return results
    return [result for result in results if result.get('response_likelihood', '').lower() != 'unlikely']

def cosine_similarity(v1, v2):
    dot_product = sum(x*y for x, y in zip(v1, v2))
    magnitude1 = math.sqrt(sum(x*x for x in v1))
    magnitude2 = math.sqrt(sum(x*x for x in v2))
    if magnitude1 * magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)

def encode(text):
    # Strip leading and trailing whitespace
    cleaned_text = text.strip()
    
    # Check if the cleaned text is a single word
    if len(cleaned_text.split()) == 1:
        enriched_text = f"companies that make {cleaned_text} or work in an industry related to the term {cleaned_text}"
    else:
        enriched_text = cleaned_text
    
    response = client.embeddings.create(input=enriched_text, model="text-embedding-ada-002")
    return response.data[0].embedding

def semantic_search(query, data, embedding_column, similarity_threshold):
    if data.empty:
        return []  # Return empty list if input data is empty

    query_vector = encode(query)
    
    # Ensure data is a DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)
    
    # Calculate cosine similarity
    similarities = [cosine_similarity(query_vector, emb) for emb in data[embedding_column]]
    
    # Create a list of results with similarities
    results = [
        {**row.to_dict(), 'similarity': similarity}
        for (_, row), similarity in zip(data.iterrows(), similarities)
        if similarity >= similarity_threshold
    ]
    
    # Sort results
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return results

def filter_results(results, min_employees):
    def safe_int_convert(x):
        try:
            return int(float(x))
        except (ValueError, TypeError):
            return 0
    return [result for result in results if safe_int_convert(result['num_employees']) > min_employees]

def name_search(full_name, data):
    names = full_name.split(maxsplit=1)
    if len(names) == 2:
        first_name, last_name = names
        return data[(data['First Name'].str.lower() == first_name.lower()) & 
                    (data['Last Name'].str.lower() == last_name.lower())].to_dict('records')
    return None  # Return None if not exactly two names

def search(name_query=None, selected_industries=None, company_query=None, title_query=None, min_employees=None, similarity_threshold=0.8, include_unlikely=True, user_id=None):
    global data
    
    if data is None:
        data = load_data(user_id)
        if data is None:
            return []  # or raise an error
    
    # Check if all main search criteria are empty
    if not name_query and not company_query and not title_query:
        return []  # Return empty list if all main search criteria are blank
    
    # If a name query is provided, only perform name search
    if name_query:
        results = name_search(name_query, data)
        return results if results is not None else []  # Return empty list if name not found or invalid format
    
    # If no name query, proceed with other filters
    filtered_data = data.copy()
    
    if selected_industries and "All Industries" not in selected_industries:
        if isinstance(selected_industries, str):
            selected_industries = [selected_industries]
        
        industry_mask = filtered_data['industry'].isin(selected_industries) | \
                        filtered_data['industries'].fillna('').apply(lambda x: any(industry in x.split(',') for industry in selected_industries))
        filtered_data = filtered_data[industry_mask]

    if filtered_data.empty:
        return []

    results = filtered_data.to_dict('records')

    if company_query:
        results = semantic_search(query=company_query, data=pd.DataFrame(results), 
                                  embedding_column='company_embedding', 
                                  similarity_threshold=similarity_threshold)
        
    if title_query:
        results = semantic_search(query=title_query, data=pd.DataFrame(results), 
                                  embedding_column='title_embedding', 
                                  similarity_threshold=similarity_threshold)

    if min_employees is not None and min_employees != 0:
        results = filter_results(results, min_employees)

    results = filter_by_response_likelihood(results, include_unlikely)
    
    return results

def format_results(results):
    formatted = ""
    for i, result in enumerate(results, 1):
        formatted += f"  First Name: {result['First Name']}\n"
        formatted += f"  Last Name: {result['Last Name']}\n"
        formatted += f"  Title: {result['title']}\n"
        formatted += f"  Company: {result['company']}\n"
        formatted += f"  Employees: {result['num_employees']}\n"
        formatted += f"  Contact: {result['contact']}\n"
        formatted += f"  Response Likelihood: {result['response_likelihood']}\n"
        
        # Handle the case where 'similarity' might not be present
        similarity = result.get('similarity')
        if similarity is not None:
            formatted += f"  Similarity: {similarity:.2f}\n"
        else:
            formatted += "  Similarity: N/A\n"
        
        formatted += f"\n  Company Description: {result['short_description_trunc']}\n"
        formatted += "\n"
        formatted += "======================================================================\n"
        formatted += "======================================================================\n"
        formatted += "\n"
    return formatted if formatted else "No results found."

def gradio_search(name_query, company_query, title_query, selected_industries, min_employees, include_unlikely, similarity_threshold, request: gr.Request):
    user_greeting, user_id = get_user_info(request)
    global data
    data = load_data(user_id)  # Reload data for the current user
    results = search(name_query, selected_industries, company_query, title_query, min_employees, similarity_threshold, include_unlikely, user_id=user_id)
    formatted_results = format_results(results)
    return f"{user_greeting}\n\n{formatted_results}"

iface = gr.Interface(
    fn=gradio_search,
    inputs=[
        gr.Textbox(label="First and Last Name (Optional)"),
        gr.Textbox(label="Company Query (Optional. Example: companies that make interactive voice ai agents)"),
        gr.Textbox(label="Title Query (Optional. Example: cofounder)"),
        gr.Dropdown(choices=get_unique_industries_list(), 
            label="Select Industries (Optional)", 
            multiselect=True, 
            value=["All Industries"]),
        gr.Number(label="Minimum Number of Employees (Optional)", precision=0),
        gr.Checkbox(label="Include 'Unlikely' response_likelihood (Warning: some 'likely' or 'very likely' may be misclassified as 'unlikely')", value=True),
        gr.Slider(minimum=0.0, maximum=1.0, value=0.8, label="Similarity Threshold", step=0.01)
    ],
    outputs=gr.Textbox(label="Results", lines=20, autoscroll=False),
    title="Referral Search",
    description=""
)

# Launch the interface
if __name__ == "__main__":
    iface.launch(server_port=7860, server_name="0.0.0.0")