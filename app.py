import streamlit as st
import os
from helperfunctions import *
import subprocess
import time
from googleapiclient.discovery import build

REGION = "me-west1"
PROJECT = "commit-automation"
os.environ["GCLOUD_PROJECT"] = PROJECT
os.environ["GOOGLE_CLOUD_QUOTA_PROJECT"] = PROJECT


def run_command_and_print_realtime(command):
    # Start the subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    response = ""
    # Read the command's output line by line and print in real-time
    while True:
        output_line = process.stdout.readline()
        if output_line == '' and process.poll() is not None:
            break
        if output_line:
            response = response + output_line.strip() + '\n'
    return response

def run_app():
    st.set_page_config(page_title="Billing Account Viewer Permissions App", page_icon=":robot_face:")
    st.sidebar.image("./images/logo.png")
    st.sidebar.markdown(
        """
        <a style='display: block; text-align: center;' href="https://www.comm-it.com/">Made with :heart: by Commit</a>
        """,
        unsafe_allow_html=True,
    )

    # Streamlit application starts here
    st.title('Billing Account Viewer Permissions App')

    # Initialize session state variables if they don't exist
    if 'valid_email' not in st.session_state:
        st.session_state.valid_email = False
    if 'confirmed_email' not in st.session_state:
        st.session_state.confirmed_email = None
    if 'reset_email_input' not in st.session_state:
        st.session_state.reset_email_input = False
    if 'show_confirmation' not in st.session_state:
        st.session_state.show_confirmation = None
    

    # Function to validate the email and update the session state
    def validate_email():
        if is_valid_email(st.session_state.email):
            st.success(f'Valid email address: {st.session_state.email}')
            st.session_state.valid_email = True
            st.session_state.show_confirmation = True
        else:
            st.error('Invalid email address. Please enter a valid email address.')
            st.session_state.valid_email = False
            st.session_state.show_confirmation = False

    # Function to confirm the email and save it to a variable
    def confirm_email():
        st.session_state.confirmed_email = st.session_state.email
        #st.write(f'Email {st.session_state.confirmed_email} saved for further use.')

    # Reset email input when requested
    if st.session_state.reset_email_input:
        st.session_state.email = ''
        st.session_state.reset_email_input = False

    # Create a text input for the email address, using session state to store the input
    st.text_input('Please enter the email of the employee for whom you wish to grant permissions:', key='email', on_change=validate_email)

    # If a valid email has been entered, show the confirmation button
    if st.session_state and st.session_state.show_confirmation:
        st.write('Do you want to use this email?')
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Yes'):
                confirm_email()
        with col2:
            if st.button('No'):
                # Reset the process
                st.session_state.reset_email_input = True
                st.session_state.show_confirmation = False  # Hide confirmation
                st.rerun()
                

    # Initialize a list in session state to store selected billing account IDs
    if 'selected_billing_accounts' not in st.session_state:
        st.session_state.selected_billing_accounts = []
    if 'show_accounts_confirmation' not in st.session_state:
        st.session_state.show_accounts_confirmation = False
    if 'reset_accounts_input' not in st.session_state:
        st.session_state.reset_accounts_input = False
    if 'create_terraform' not in st.session_state:
        st.session_state.create_terraform = False

    if st.session_state.reset_accounts_input:
        st.session_state.selected_billing_accounts = ''
        st.session_state.confirmed_accounts = ''
        st.session_state.reset_accounts_input = False
        st.session_state.create_terraform = False

    # Display the checklist only after the email has been confirmed
    if st.session_state.confirmed_email:
        billing_accounts = get_billingaccount_names()
        selected_accounts = st.multiselect('Select Billing Accounts:', billing_accounts, key='billing_accounts')

        if st.button('Confirm Selection'):
            st.session_state.selected_billing_accounts = selected_accounts
            #st.write('You have selected:', st.session_state.selected_billing_accounts)
            st.session_state.show_accounts_confirmation = True

    def confirm_accounts():
        st.session_state.confirmed_accounts = st.session_state.selected_billing_accounts
        st.write(f'Processing...')
        st.session_state.create_terraform = True

    if st.session_state and st.session_state.show_accounts_confirmation:
        st.write('Do you want to give permissions for these billing accounts?', st.session_state.selected_billing_accounts)
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Yes - these accounts are fine'): 
                confirm_accounts()
        with col2:
            if st.button('No - take me back'):
                # Reset the process
                st.session_state.reset_accounts_input = True
                st.session_state.show_accounts_confirmation = False  # Hide confirmation
                st.rerun()

    customer_account_names = []
    if st.session_state and st.session_state.create_terraform:
        customer_account_names = st.session_state.confirmed_accounts
        with open('list_file.txt', 'w') as tmpfile:
            for item in customer_account_names:
                tmpfile.write("%s\n" % item)
        with open('email_file.txt', 'w') as emailtmpfile:
            emailtmpfile.write("%s\n" % st.session_state.confirmed_email)
        subprocess.run(["pretf", "init"])
        st.write("Generating files... ")      
        time.sleep(5)
        completed_process = subprocess.run(['pretf', 'plan', '-out=tfplan.out', '-no-color'], capture_output=True, text=True)
        time.sleep(5)
        st.write("Confirm that you want the following changes:")
        # Get the standard output (and optionally standard error)
        pretf_output = completed_process.stdout  # If you also want to capture errors, you can append completed_process.stderr
        # Display the output in a text box
        st.text_area("Terraform Plan:", pretf_output, height=300)
        # Ask for user confirmation
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Yes - these are the changes I want!'): 
                st.write("Applying... ")
                #completed_apply = subprocess.run(["pretf", "apply", "tfplan.out"], capture_output=True, text=True)
                #applyoutput = completed_apply.stdout
                applyoutput = run_command_and_print_realtime(["pretf", "apply", '-no-color', "tfplan.out"])
                st.text_area("Apply Output:", applyoutput, height=300)
                st.markdown("Process completed - please check for errors in the text box above.")
                #if st.button('Let\'s do another!'): 
                #    st.write("Restarting... ")
                #    st.session_state.clear()
                #    st.rerun()
        with col2:
            if st.button('No - let\'s start over.'):
                # Reset the process
                st.write("Restarting... ")
                st.session_state.clear()
                st.rerun()
        

if __name__ == "__main__":
    run_app()
