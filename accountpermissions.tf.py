from pretf.api import block
from app import *

REGION = "me-west1"
PROJECT = "commit-automation"

def pretf_blocks():
    with open('list_file.txt', 'r') as file:
        names = [line.rstrip('\n') for line in file]
    id_list = get_billingaccount_ids(names)
    email_address = ""
    with open('email_file.txt', 'r') as emailtmpfile:
        # Read the first line from the file
        email_address = emailtmpfile.readline().strip()
    username_part = email_address.split('@')[0]
    username_part = username_part.replace(".", "")
    provider = yield block("provider", "google", {"project": PROJECT, "region": REGION,})
#    accounts = yield block("variable", f"{username_part}_billing_account_ids", {"default": id_list})
    for id in id_list:
        yield block("resource", "google_billing_account_iam_member", f"{username_part}_{id}_permissions", {"billing_account_id": id, "role": "roles/billing.viewer", "member": f"user:{email_address}"})