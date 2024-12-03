import argparse

def add_arguments(**kwargs) -> argparse.Namespace:
    """
    Adds command-line arguments for the script.

    Args:
        **kwargs: Optional keyword arguments for dynamic argument customization.

    Returns:
        argparse.Namespace: Parsed arguments containing the specified options.
    """
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Download YouTube videos using pytube-tool.")
    
    # dynamic argument
    if "version" in kwargs:
        parser.add_argument(
            "--version", "-v", 
            action="version", 
            version=f"%(prog)s {kwargs['version']}"
        )
    
    parser.add_argument(
        "--author", 
        action="store_true", 
        help="Show author information"
    )
    parser.add_argument(
        "--url", "-u", 
        type=str, 
        help="YouTube video URL to download directly without prompting."
    )
    parser.add_argument(
        "--path", "-p", 
        type=str, 
        help="Specify the download path for the videos."
    )
    parser.add_argument(
        "--batch", "-b",
        type=str,
        help="Path to a file containing a list of YouTube video URLs."
    )
    parser.add_argument(
        "--upgrade", 
        action="store_true", 
        help="Upgrade the pytube package to the latest version"
    )
    
    # Parse arguments and return
    return parser.parse_args()