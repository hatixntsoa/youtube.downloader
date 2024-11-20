import os


def prompt_download_path():
    """
    Prompts the user for a valid download directory path.
    Returns the valid path if successful, or None otherwise.
    """
    while True:
        try:
            download_path = input("Enter the directory where videos should be downloaded: ").strip()

            # Validate the path
            if os.path.isdir(download_path):
                return download_path
            else:
                print("The specified path does not exist or is not a directory. Please try again.")
        except Exception as e:
            print(f"An error occurred while validating the download path: {e}")
            return None
