#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# go to google takeout and download your email data.
https://takeout.google.com/

# if you have a outlook account and not gmail, then first convert the outlook data to the mbox format
index/convert_pst_to_mbox

# get data from mbox file(s). This tells you which contacts you have emailed and which contacts have responded
index/extract_email_metadata.py

# aggregate the email data to count the number of times each contact has replied to you
index/count_email_exchanges.py

# for each contact, get information from Apollo about them and their company
enrich/query_apollo.py

# clean up the dataset, removing rows where apollo couldn't find the contact, etc.
enrich/post_process_enrichment.py

# embed the contact information, company information, role, etc.
embed/create_embeddings.py

# make sure output of embed/create_embeddings.py into the /data dir

# run the app
app.py
