"""
Utility functions for NLTK data management.
"""

import ssl
import nltk


def download_nltk_data():
    """
    Download required NLTK data with SSL verification disabled.
    
    This function disables SSL verification for NLTK downloads,
    which can be helpful when there are certificate issues.
    """
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    # Download required NLTK data
    nltk.download('punkt')
    nltk.download('stopwords')
    
    print("NLTK data downloaded successfully!")


if __name__ == "__main__":
    download_nltk_data()
