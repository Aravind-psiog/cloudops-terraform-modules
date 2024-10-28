import os


def lambda_path():
    """
    Resources
    ----------------

    This function will return a set of resources to handle API Gateway routing

    Args: None

    Returns: A set of resources for API Gateway routes handling
    """
    resource_path = {
        "staging": os.environ.get("stage_path"),
        "resource": os.environ.get("resource_path"),
    }
    return resource_path


def cognito():
    """
    Resources
    ----------------

    This function will return a set of resources to handle API Gateway routing

    Args: None

    Returns: A set of resources for API Gateway routes handling
    """
    resource_path = {
        "cognito_region": os.environ.get("cognito_region"),
        "cognito_user_pool": os.environ.get("cognito_user_pool"),
        "cognito_client": os.environ.get("cognito_client"),
    }
    return resource_path
