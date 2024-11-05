#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##############################################
####### init
##############################################

user_name = "tom_shapland" # this is used in file naming
user_dir = '/Users/tom/tmp/referral/' + user_name + '/'
mbox_paths = [user_dir + 'All mail Including Spam and Trash-002.mbox']
your_emails = {'tom@tuletechnologies.com'}
skip_emails = {'mailer-daemon@googlemail.com'}
output_filename = user_dir  + 'mbox_dicts.pkl'

limit = 1000000000000 # 1000

import mailbox
import email.utils
import itertools
import pickle
import os

# Create the directory along with any necessary intermediate directories
try:
    os.makedirs(user_dir)
    print(f"Directory path '{user_dir}' created successfully")
except FileExistsError:
    print(f"Directory path '{user_dir}' already exists")
except Exception as e:
    print(f"An error occurred: {e}")




##############################################
####### define functions
##############################################

def save_dictionaries_with_pickle(data, filename='saved_data.pkl'):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def parse_name(name):
    """Split the name into first and last name. Assumes 'first last' format."""
    parts = name.split()
    first_name = parts[0] if parts else ''
    last_name = parts[1] if len(parts) > 1 else ''
    return first_name, last_name

def process_mbox(mbox_paths, your_emails, limit=10):
    # Convert your_emails to a set for faster lookup and ensure all are lower case
    your_emails = set(email.lower() for email in your_emails)

    # Initialize dictionaries
    message_id_dict = {}  # {Message-ID: sender} (only for your sent messages)
    in_reply_to_dict = {}  # {In-Reply-To: sender}

    total_processed = 0  # Counter for total processed messages

    for mbox_path in mbox_paths:
        
        # print the name of the file that's getting processed
        print('processing ' + mbox_path)
        
        # Open the mbox file
        mbox = mailbox.mbox(mbox_path)
        
        # for each mbox, try this. Once complete, close the connection
        try: 
            
        # Iterate through the first 'limit' messages in the mbox
        # debugging code: message = next(itertools.islice(mbox, 14, 15), None)
            for message in itertools.islice(mbox, limit):
                total_processed += 1  # Increment the counter
                if total_processed % 100 == 0:  # Print every 100 messages
                    print(f"Processed {total_processed} messages")
       
                try:
                    
                # skip message if it's an automatic response
                    if message['Subject']:
                        subject = str(message['Subject'])
                        if any(phrase in subject for phrase in ['Automatic reply', 'OOO', 'Out of office', 'Out of Office']):
                            continue
                
                    # Extract and clean sender email
                    from_header = str(message['From'])
                    from_parsed = email.utils.parseaddr(from_header)
                    sender_email = from_parsed[1].lower().strip()
                    sender_name = from_parsed[0].strip()
                    first_name, last_name = parse_name(sender_name)
            
                    # Extract and clean Message-ID
                    message_id = message.get('Message-ID')
                    if message_id:
                        message_id = message_id.strip('<> ')
            
                    # Extract and clean In-Reply-To
                    in_reply_to = message.get('In-Reply-To')
                    if in_reply_to:
                        in_reply_to = in_reply_to.strip('<> ')
            
                    # Store Message-ID and sender only if you're the sender
                    if message_id and sender_email in your_emails:
                        message_id_dict[message_id] = sender_email
                
                    # Store In-Reply-To and sender for all messages
                    if in_reply_to:
                        if sender_email in your_emails or sender_email in skip_emails:
                            continue
                        in_reply_to_dict[in_reply_to] = {'email': sender_email, 'first_name': first_name, 'last_name': last_name}
                    
                except Exception as e:
                    print(f"Skipped a message due to an error: {e}")
                    continue
            
        finally: 
            mbox.close()
    
    print(f"Total messages processed: {total_processed}")
    return message_id_dict, in_reply_to_dict

##############################################
####### process
##############################################

message_id_dict, in_reply_to_dict = process_mbox(mbox_paths, your_emails, limit)


# Save both dictionaries in one file
save_dictionaries_with_pickle(data = {'MessageIDDict': message_id_dict, 'InReplyToDict': in_reply_to_dict}, 
                              filename = output_filename)
