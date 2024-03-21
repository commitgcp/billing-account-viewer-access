from pretf import workflow

def pretf_workflow():
    # Delete *.tf.json and *.tfvars.json files.
    workflow.delete_files()

    # Create *.tf.json and *.tfvars.json files
    # from *.tf.py and *.tfvars.py files.
    created = workflow.create_files()
    
    # Execute Terraform, raising an exception if it fails.
    proc = workflow.execute_terraform()

    # Clean up created files if successful.
    workflow.clean_files(created)

    return proc