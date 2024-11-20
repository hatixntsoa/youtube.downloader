import os
from dotenv import load_dotenv
from pathlib import Path

# Define the path to the .env file inside the utils directory
ENV_FILE_PATH = Path(__file__).resolve().parent / '.env'


def get_env_variable(key, default=None):
    """
    Retrieve a value from the .env file or environment variables.
    If the key is not found, return the provided default value.
    """
    load_dotenv(dotenv_path=ENV_FILE_PATH)
    return os.getenv(key, default)


def set_env_variable(key, value):
    """
    Set or update a value in the .env file located inside the utils directory.
    If the file doesn't exist, it will be created.
    """
    try:
        # Ensure the utils directory exists
        utils_dir = Path(__file__).resolve().parent
        utils_dir.mkdir(parents=True, exist_ok=True)

        # Check if the .env file exists, if not create it
        if not ENV_FILE_PATH.exists():
            ENV_FILE_PATH.touch()  # Create the .env file if it doesn't exist

        load_dotenv(dotenv_path=ENV_FILE_PATH)

        # Read the current content of the .env file
        with open(ENV_FILE_PATH, 'r') as file:
            lines = file.readlines()

        # Update the environment variable in the .env file
        found = False
        with open(ENV_FILE_PATH, 'w') as file:
            for line in lines:
                if line.startswith(f"{key}="):
                    file.write(f"{key}={value}\n")
                    found = True
                else:
                    file.write(line)
            if not found:
                file.write(f"{key}={value}\n")
    except Exception as e:
        print(f"An error occurred while setting the environment variable: {e}")
