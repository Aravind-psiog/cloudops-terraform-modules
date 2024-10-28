from dotenv import load_dotenv


def load_config():
    """
    Load Config
    -----------

    Thus function loads config data from the environment

    Attributes: None

    Returns: Config data
    """
    config = load_dotenv(r"../configs/staging.env")
    return config
