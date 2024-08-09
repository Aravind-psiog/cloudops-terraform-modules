import subprocess
import os
import logging
import sys
import re
# Define the variable value you want to pass
# os.environ["TF_LOG"] = "ERROR"
# os.environ["TF_LOG_PATH"] = "/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra"

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.propagate = False
# Define the Terraform command
terraform_apply = ["terraform", "apply", "-auto-approve", "-var-file=variables.tfvars"]
terraform_init = ["terraform", "init"]
terraform_ws  = ["terraform", "workspace", "list"]

# Run the Terraform command using subprocess
def apply():
    try:
        result = subprocess.run(terraform_apply, cwd="/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra",stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            env={
                        "TF_LOG": "ERROR",
                        "TF_LOG_PATH": "/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra/terraform-error.log",
                        "PATH": "$PATH:/usr/bin",
                    },)
    except subprocess.CalledProcessError as e:
        print(f"Error running Terraform: {e}")
        with open("/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra/terraform-error.log", "r", encoding="UTF-8") as f:
                lines = f.readlines()
        for _, line in enumerate(lines):
            error_index = line.strip().find("error:")
            if error_index != -1:
                error_message = line.strip()[error_index + len("error:") :]
                logger.error(error_message)

def workspace():
    try:
        result = subprocess.run(terraform_ws, cwd="/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra",stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True)
        my_string = result.stdout.strip()
        lines = my_string.splitlines()
        my_array = []
        for line in lines:
            my_array.append(line)

        print("Resulting array:", my_array)
        for envs in my_array:
            if "*" in envs:
                print("current env is",envs)
    except subprocess.CalledProcessError as e:
        print(f"Error running Terraform: {e}")


def init():
    try:
        result = subprocess.run(terraform_init, cwd="/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra",stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True)
        apply()
    except subprocess.CalledProcessError as e:
        print(f"Error running Terraform: {e}")
    
workspace()