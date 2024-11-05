#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pypff
from email import message_from_bytes
from mailbox import mbox

pst_files = ['/Users/tom/Downloads/inbox.pst']
output_dir = '/Users/tom/Downloads/mbox/'

def pst_to_mbox(pst_file, output_dir):
    # Open the PST file
    pst = pypff.file()
    pst.open(pst_file)
    
    # Get the root folder
    root = pst.get_root_folder()
    
    # Process all folders
    process_folder(root, output_dir)
    
    # Close the PST file
    pst.close()

def process_folder(folder, output_dir):
    for sub_folder in folder.sub_folders:
        # Create a new mbox file for each folder
        mbox_file = os.path.join(output_dir, f"{sub_folder.name}.mbox")
        mb = mbox(mbox_file)
        
        # Process all messages in the folder
        for message in sub_folder.sub_messages:
            email_data = message.get_transport_headers() + message.get_plain_text_body()
            email_message = message_from_bytes(email_data.encode('utf-8'))
            mb.add(email_message)
        
        mb.close()
        
        # Process subfolders recursively
        process_folder(sub_folder, output_dir)

if __name__ == "__main__":
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each PST file
    for pst_file in pst_files:
        pst_to_mbox(pst_file, output_dir)
    
    print("Conversion completed.")