
user_name = "tom_shapland" # this is used in file naming
user_dir = '/Users/tom/tmp/referral/' + user_name + '/'
input_filename = user_dir  + 'mbox_dicts_tom_shapland.pkl'
output_filename = user_dir + 'email_index_tom_shapland.csv'

import pickle
import csv

def load_dictionaries_from_pickle(filename='saved_data.pkl'):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# read data
data = load_dictionaries_from_pickle(filename=input_filename)
message_id_dict = data['MessageIDDict']
in_reply_to_dict = data['InReplyToDict']

print(len(message_id_dict))
print(len(in_reply_to_dict))

def filter_and_count_replies(message_id_dict, in_reply_to_dict, output_filename = output_filename):
    
    # Subset in_reply_to_dict to entries where in-reply-to ID is in message_id_dict
    filtered_dict = {key: value for key, value in in_reply_to_dict.items() if key in message_id_dict}

    # Prepare to count replies by each sender
    sender_counts = {}
    for details in filtered_dict.values():
        email = details['email']
        if email in sender_counts:
            sender_counts[email]['count'] += 1
        else:
            sender_counts[email] = {
                'first_name': details['first_name'],
                'last_name': details['last_name'],
                'count': 1
            }

    # Write results to a CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['First Name', 'Last Name', 'Email', 'Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for email, info in sender_counts.items():
            writer.writerow({
                'First Name': info['first_name'],
                'Last Name': info['last_name'],
                'Email': email,
                'Count': info['count']
            })

    print(f"Data has been written to {output_filename}")

# Call the function with your data
filter_and_count_replies(message_id_dict, in_reply_to_dict)
