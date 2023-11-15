import subprocess
import os
import logging
import sys
# Define the variable value you want to pass
# os.environ["TF_LOG"] = "ERROR"
# os.environ["TF_LOG_PATH"] = "/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra"

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.propagate = False
# Define the Terraform command
terraform_command = ["terraform", "apply", "-auto-approve", "-var-file=variables.tfvars"]

# Run the Terraform command using subprocess
try:
    result = subprocess.run(terraform_command, cwd="/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra",stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
        env={
                    "TF_LOG": "ERROR",
                    "TF_LOG_PATH": "/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra/terraform-error.log",
                    "PATH": "$PATH:/usr/bin",
                },)
    # print(result.stdout)
    # for line in result.stdout.splitlines():
    #     print(line)
    #     print("-------------------------------")

    # # Print the final return code
    # print(f"Terraform process returned: {result.returncode}")
except subprocess.CalledProcessError as e:
    print(f"Error running Terraform: {e}")
    with open("/home/aravindprabaharan/Desktop/workbench/cloudops-terraform-modules/infra/terraform-error.log", "r", encoding="UTF-8") as f:
            lines = f.readlines()
    for _, line in enumerate(lines):
        error_index = line.strip().find("error:")
        if error_index != -1:
            error_message = line.strip()[error_index + len("error:") :]
            logger.error(error_message)
