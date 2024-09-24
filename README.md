# Cloud native - IaC ![AWS](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/readme-for-terraform/assests/aws.png?raw=true) and ![Azure](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/readme-for-terraform/assests/azure.png?raw=true)

This repository contains Infrastructure as Code (IaC) scripts written in Terraform, designed to automate the provisioning and management of cloud resources across both AWS and Azure. With a provider-agnostic approach, the repository allows you to easily manage infrastructure on multiple cloud platforms while ensuring consistency, repeatability, and scalability.

## Terraform? ![Terraform](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/main/assests/tf-icon.png?raw=true)

Terraform is an open-source IaC tool created by HashiCorp. It uses a high-level configuration language provided by HashiCorp Configuration Language and provisions, manages, and automates infrastructure. There are different flavors or modes in which Terraform can be deployed:

1. **Opensource Terraform**: Free of cost with basic features to build and manage infrastructure.
2. **Terraform Cloud**: SaaS solution for collaboration, version control, and automation tools.\
3. **Terraform Enterprise**: Host Terraform Cloud yourself for larger organizations needing advanced security, compliance, and infrastructure governance.

# Glossary

1. **Infrastructure as Code (IaC)**: Managing and provisioning computing infrastructure through machine-readable configuration files, rather than physical hardware configuration or interactive configuration tools.
2. **HCL**: HashiCorp Configuration Language. A domain-specific language that is used to write declarative configurations in Terraform.
3. **Providers**: Plugins that define the interaction of Terraform with cloud platforms, SaaS providers, and other services. Example providers include AWS, Azure, GCP.
4. **State File**: A file used by Terraform to map real-world resources to configuration and to track metadata, performance-enhancing caching, etc.
5. **Module**: A self-contained package of Terraform configuration that has well-defined inputs and outputs and can be used in other projects.
6. **Plan**: A preview of what Terraform will change in the Infrastructure - including the actions it will perform.
7. **Apply**: The command running the changes in your Terraform plan in order to create, modify, or delete infrastructure resources.

# Use cases

Terraform can be applied across a variety of use cases

1. **Cloud Infrastructure Management**: Supplies automation for cloud resource provisioning on any provider, such as AWS, Azure, and Google Cloud. Multi-Cloud
2. **Management**: Enables resource management across multiple cloud platforms through a single configuration.
3. **Resource Orchestration**: Centered around organizing the dependencies of infrastructure components or spikes between virtual machines, networks, and storage in complex environments.
4. **Infrastructure Auditing & Compliance**: Infrastructure configurations are tracked and versioned to ensure infrastructure configurations meet compliance and security standards.
5. **Disaster Recovery**: Setup of infrastructure in different regions for disaster recovery scenarios.

# Key Concepts & Components

### Providers

Terraform interacts with different infrastructure providers through plugins called **Providers**. Providers are responsible for managing API interactions with cloud services (e.g., AWS, Azure, GCP) or other services (like Kubernetes or GitHub). A configuration can include multiple providers, enabling multi-cloud setups.

Example:

```
hcl
Copy code
provider "aws" {
  region = "us-west-2"
}

```

### Resources

Resources are Terraform's fundamental building blocks. They represent infrastructure components like servers, databases, and network interfaces. Each resource belongs to a provider and is defined by a block in the configuration.

Example:

```
hcl
Copy code
resource "aws_instance" "example" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}

```

### Modules

A **Module** is a container for multiple resources that can be reused across different configurations. Modules help in organizing and abstracting infrastructure components.

Example:

```
hcl
Copy code
module "network" {
  source = "./network"
  cidr   = "10.0.0.0/16"
}

```

### State Management

Terraform tracks infrastructure using a **State File**. This file maps Terraform resources to their corresponding real-world infrastructure. It is stored locally or in remote backends like S3 for collaboration.

# Lifecycle

### Initialization (`terraform init`)

The first step in using Terraform is to initialize the working directory, download provider plugins, and set up the backend for state management.

Example:

```bash

terraform init
```

### Planning (`terraform plan`)

The **plan** command generates an execution plan, showing users what changes will be made when applying the configuration. This is a dry run that doesn’t modify any real-world resources.

Example:

```bash

terraform plan
```

### Applying Changes (`terraform apply`)

Once the plan is reviewed, the `apply` command executes the changes and provisions the resources.

Example:

```bash

terraform apply
```

### Destroying Infrastructure (`terraform destroy`)

The `destroy` command is used to remove all the resources defined in the configuration.

Example:

```bash

terraform destroy
```

## Terraform IaC for ![AWS](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/readme-for-terraform/assests/aws.png?raw=true)

### Setup

1. [Follow these steps to install terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
2. [Install AWS CLI following these steps](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. As we are goint to use of remote storage for storing the state file, [follow these steps to configure remote state](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-remote)

### Deploying

1. Clone the main repo
2. switch to the directory with the tf file.
   ```bash
   cd /infra/aws
   ```
3. update your remote organization and workspace name on `main.tf`
   ```bash
   terraform {
   backend "remote" {
   organization = "PSIOG"
   workspaces {
     name = "tutorial"
   }
   }
   ```
4. Initialize terraform by
   ```bash
   terraform init
   ```
5. Additional checks:
   ```bash
   terraform validate
   ```
6. See the plan by
   ```bash
   terraform plan
   ```
7. Apply the plan by
   ```bash
   terraform apply
   ```
8. Copy the output IP address and open it on your browser
   ![](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/readme-for-terraform/assests/tf.gif?raw=true)

## Terraform IaC for ![Azure](https://github.com/Aravind-psiog/cloudops-terraform-modules/blob/readme-for-terraform/assests/azure.png?raw=true)

1. [Install Azure CLI with the following](https://developer.hashicorp.com/terraform/tutorials/azure-get-started/azure-build)
2. Follow the same steps as mentioned above.
