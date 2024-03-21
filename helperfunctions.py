from google.cloud import datastore
import re
from app import *

REGION = "me-west1"
PROJECT = "commit-automation"
client = datastore.Client(project="commit-automation",database="customer-billing-accounts-ids")

def get_billingaccount_names():
    key = client.key('customer-billing-accounts-ids', 'Customer Name')
    names = list(client.get(key))
    return names
    
def get_billingaccount_ids(names_list): 
    id_list = []
    key = client.key('customer-billing-accounts-ids', 'Customer Name')
    ids = dict(client.get(key))
    for name in names_list:
        id_list.append(ids[name])
    return id_list

def is_valid_email(email):
    """
    Checks if the provided string is a valid email address.

    Parameters:
    email (str): The email address to validate.

    Returns:
    bool: True if the email is valid, False otherwise.
    """

    if email is None:
        return True
    # Define the regex pattern for a valid email address
    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # Use the pattern to match the provided email address
    if pattern.match(email):
        return True
    else:
        return False
    